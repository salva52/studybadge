import hmac
import json
import time
import uuid
from datetime import datetime, timezone
from hashlib import sha256

import frappe
import requests
from frappe import _
from frappe.utils import cint, flt, now_datetime

from lms.lms.payments import (
	_make_payment_external_reference,
	_payment_for_label,
	_validate_paypal_payment_access,
	get_redirect_url,
	record_payment,
)
from lms.lms.subscriptions import (
	PLUS_ACTIVE_STATUSES,
	_get_plus_plan_for_currency,
	_get_public_base_url,
	_get_settings,
	_get_support_email,
	_safe_json,
	get_lms_path_url,
	has_active_plus,
)
from lms.lms.utils import (
	adjust_amount_for_coupon,
	complete_enrollment,
	get_lms_route,
	get_order_summary,
)

PADDLE_API_BASES = {
	"sandbox": "https://sandbox-api.paddle.com",
	"live": "https://api.paddle.com",
}
PADDLE_ACTIVE_SUBSCRIPTION_STATUSES = {"active", "trialing"}
PADDLE_TERMINAL_SUBSCRIPTION_STATUSES = {"canceled", "paused", "past_due"}
PADDLE_PAID_TRANSACTION_STATUSES = {"completed", "paid", "billed"}

COUNTRY_CODES = {
	"argentina": "AR",
	"bolivia": "BO",
	"brazil": "BR",
	"brasil": "BR",
	"canada": "CA",
	"chile": "CL",
	"colombia": "CO",
	"costa rica": "CR",
	"ecuador": "EC",
	"el salvador": "SV",
	"españa": "ES",
	"spain": "ES",
	"mexico": "MX",
	"méxico": "MX",
	"panama": "PA",
	"panamá": "PA",
	"paraguay": "PY",
	"peru": "PE",
	"perú": "PE",
	"united kingdom": "GB",
	"united states": "US",
	"uruguay": "UY",
	"venezuela": "VE",
}


def _get_password(settings, fieldname: str) -> str | None:
	try:
		from frappe.utils.password import get_decrypted_password

		try:
			return get_decrypted_password(
				"StudyBadge Plus Settings",
				"StudyBadge Plus Settings",
				fieldname,
				raise_exception=False,
			)
		except TypeError:
			return get_decrypted_password(
				"StudyBadge Plus Settings",
				"StudyBadge Plus Settings",
				fieldname,
			)
	except Exception:
		if hasattr(settings, "get_password"):
			try:
				return settings.get_password(fieldname)
			except Exception:
				return None
	return None


def _ensure_enabled(settings=None):
	settings = settings or _get_settings()
	if not getattr(settings, "paddle_enabled", 0):
		frappe.throw(_("Paddle is not enabled in StudyBadge Plus Settings."))
	return settings


def _api_base(settings=None) -> str:
	settings = settings or _get_settings()
	mode = (getattr(settings, "paddle_mode", None) or "sandbox").lower()
	return PADDLE_API_BASES.get(mode, PADDLE_API_BASES["sandbox"])


def _client_token(settings=None) -> str:
	settings = _ensure_enabled(settings)
	token = _get_password(settings, "paddle_client_token") or getattr(settings, "paddle_client_token", None)
	if not token:
		frappe.throw(_("Paddle client-side token is missing in StudyBadge Plus Settings."))
	return token


def _api_key(settings=None) -> str:
	settings = _ensure_enabled(settings)
	api_key = _get_password(settings, "paddle_api_key") or getattr(settings, "paddle_api_key", None)
	if not api_key:
		frappe.throw(_("Paddle API key is missing in StudyBadge Plus Settings."))
	return api_key


def _webhook_secret(settings=None) -> str:
	settings = _ensure_enabled(settings)
	secret = _get_password(settings, "paddle_webhook_secret") or getattr(settings, "paddle_webhook_secret", None)
	if not secret:
		frappe.throw(_("Paddle webhook secret is missing in StudyBadge Plus Settings."))
	return secret


def _headers(settings=None) -> dict:
	return {
		"Authorization": f"Bearer {_api_key(settings)}",
		"Content-Type": "application/json",
	}


def _request(method: str, path: str, settings=None, **kwargs) -> dict:
	settings = _ensure_enabled(settings)
	response = requests.request(
		method,
		f"{_api_base(settings)}{path}",
		headers=_headers(settings),
		timeout=20,
		**kwargs,
	)
	try:
		payload = response.json()
	except ValueError:
		payload = {"message": response.text}
	if response.status_code >= 400:
		frappe.log_error(json.dumps(payload, indent=2, default=str), "StudyBadge Paddle Error")
		frappe.throw(_("Paddle could not process this payment. Please try again."))
	return payload


def _paddle_log(message: str, data: dict | None = None):
	try:
		safe_payload = json.dumps(data or {}, default=str, sort_keys=True, indent=2)
		frappe.logger("studybadge_paddle").info(f"{message}: {safe_payload}")
		frappe.log_error(safe_payload, f"StudyBadge Paddle Debug: {message}")
	except Exception:
		pass


def _parse_paddle_datetime(value: str | None):
	if not value:
		return None
	try:
		parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
		if parsed.tzinfo:
			parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
		return parsed.strftime("%Y-%m-%d %H:%M:%S")
	except ValueError:
		return value


def _country_code(country: str | None) -> str | None:
	if not country:
		return None
	country = str(country).strip()
	if len(country) == 2:
		return country.upper()
	return COUNTRY_CODES.get(country.lower())


def _get_user_country(user: str | None = None) -> str | None:
	user = user or frappe.session.user
	if not user or user == "Guest":
		return None
	return (
		frappe.db.get_value("Address", {"email_id": user}, "country")
		or frappe.db.get_value("User", user, "country")
	)


def _normalize_status(status: str | None) -> str:
	status = (status or "unknown").lower()
	if status == "cancelled":
		return "canceled"
	return status


def _checkout_payload(settings, price_id: str, custom_data: dict, success_url: str, country: str | None = None):
	payload = {
		"enabled": bool(getattr(settings, "paddle_enabled", 0)),
		"mode": getattr(settings, "paddle_mode", None) or "sandbox",
		"client_token": _client_token(settings),
		"price_id": price_id,
		"items": [{"priceId": price_id, "quantity": 1}],
		"custom_data": custom_data,
		"success_url": success_url,
		"customer": {"email": frappe.session.user},
		"support_email": _get_support_email(),
	}
	country_code = _country_code(country)
	if country_code:
		payload["customer"]["address"] = {"countryCode": country_code}
	return payload


def _checkout_payload_for_transaction(
	settings,
	transaction: dict,
	custom_data: dict,
	success_url: str,
	country: str | None = None,
):
	payload = {
		"enabled": bool(getattr(settings, "paddle_enabled", 0)),
		"mode": getattr(settings, "paddle_mode", None) or "sandbox",
		"client_token": _client_token(settings),
		"transaction_id": transaction.get("id"),
		"custom_data": custom_data,
		"success_url": success_url,
		"customer": {"email": frappe.session.user},
		"support_email": _get_support_email(),
	}
	country_code = _country_code(country)
	if country_code:
		payload["customer"]["address"] = {"countryCode": country_code}
	return payload


def _minor_units(amount: float, currency: str = "USD") -> str:
	zero_decimal = {"JPY", "KRW", "VND"}
	multiplier = 1 if (currency or "").upper() in zero_decimal else 100
	return str(int(round(flt(amount) * multiplier)))


def _custom_product_payload(title: str, description: str | None = None) -> dict:
	return {
		"name": (title or "StudyBadge").strip()[:200],
		"description": (description or title or "StudyBadge digital product").strip()[:2048],
		"type": "custom",
		"tax_category": "digital-goods",
	}


def _custom_price_payload(title: str, amount: float, currency: str = "USD", description: str | None = None):
	return {
		"description": f"StudyBadge checkout: {title}"[:500],
		"name": (title or "StudyBadge")[:150],
		"type": "custom",
		"billing_cycle": None,
		"trial_period": None,
		"tax_mode": "account_setting",
		"unit_price": {
			"amount": _minor_units(amount, currency),
			"currency_code": currency,
		},
		"product": _custom_product_payload(title, description),
	}


def _create_checkout_transaction(details: dict, custom_data: dict, checkout_url: str, settings=None) -> dict:
	title = details.get("title") or "StudyBadge"
	payload = {
		"items": [
			{
				"quantity": 1,
				"price": _custom_price_payload(
					title,
					details.total_amount,
					details.currency or "USD",
					details.get("short_introduction") or details.get("description"),
				),
			}
		],
		"collection_mode": "automatic",
		"currency_code": details.currency or "USD",
		"custom_data": custom_data,
		"checkout": {"url": checkout_url},
	}
	_paddle_log(
		"Creating Paddle transaction",
		{
			"title": title,
			"currency": payload.get("currency_code"),
			"amount_minor": payload["items"][0]["price"]["unit_price"]["amount"],
			"checkout_url": checkout_url,
			"custom_data": custom_data,
		},
	)
	response = _request("POST", "/transactions", settings=settings, data=json.dumps(payload))
	transaction = response.get("data") or response
	_paddle_log(
		"Created Paddle transaction",
		{
			"id": transaction.get("id"),
			"status": transaction.get("status"),
			"checkout_url": (transaction.get("checkout") or {}).get("url"),
			"custom_data": transaction.get("custom_data"),
		},
	)
	return transaction


def _get_paddle_discount(coupon_code: str | None, doctype: str, docname: str):
	if not coupon_code:
		return None, None

	from lms.lms.utils import apply_coupon

	# Validate expiry, usage limit, and applicability against the LMS coupon rules.
	apply_coupon(doctype, docname, coupon_code, 1)
	coupon = frappe.db.get_value(
		"LMS Coupon",
		{"code": coupon_code, "enabled": 1},
		["name", "paddle_discount_id", "paddle_discount_code"],
		as_dict=True,
	)
	if not coupon or not (coupon.paddle_discount_id or coupon.paddle_discount_code):
		frappe.throw(
			_("This coupon is not configured for Paddle yet. Please use Mercado Pago or PayPal for this coupon.")
		)
	return coupon.name, {
		"discountId": coupon.paddle_discount_id,
		"discountCode": coupon.paddle_discount_code,
	}


@frappe.whitelist()
def get_checkout_config(country: str | None = None) -> dict:
	settings = _ensure_enabled()
	payload = {
		"enabled": bool(getattr(settings, "paddle_enabled", 0)),
		"mode": getattr(settings, "paddle_mode", None) or "sandbox",
		"client_token": _client_token(settings),
	}
	country_code = _country_code(country)
	if country_code:
		payload["country_code"] = country_code
	return payload


@frappe.whitelist()
def create_paddle_checkout(
	doctype: str,
	docname: str,
	address: dict,
	payment_for_certificate: int = 0,
	coupon_code: str | None = None,
	country: str | None = None,
):
	_validate_paypal_payment_access(doctype, docname, payment_for_certificate)
	settings = _ensure_enabled()
	address = frappe._dict(address)
	coupon, paddle_discount = _get_paddle_discount(coupon_code, doctype, docname)
	details = frappe._dict(
		get_order_summary(doctype, docname, coupon=coupon_code, country=country, currency="USD")
	)

	amount = details.original_amount - details.get("discount_amount", 0)
	total_amount = details.amount
	redirect_to = get_redirect_url(doctype, docname, payment_for_certificate)
	payment = record_payment(
		address,
		doctype,
		docname,
		amount,
		details.original_amount,
		"USD",
		total_amount if details.get("gst_applied") else 0,
		details.get("discount_amount", 0),
		payment_for_certificate,
		coupon_code,
		coupon or details.get("coupon"),
	)
	payment.payment_gateway = "Paddle"
	payment.payment_status = "created"
	payment.external_reference = _make_payment_external_reference(
		payment.name,
		_payment_for_label(payment_for_certificate, doctype),
	)
	payment.save(ignore_permissions=True)

	if flt(details.total_amount) <= 0:
		frappe.db.set_value("LMS Payment", payment.name, "payment_received", 1)
		complete_enrollment(payment.name, doctype, docname)
		return {
			"status": "completed",
			"redirect_url": redirect_to,
			"payment": payment.name,
		}

	custom_data = {
		"gateway": "paddle",
		"lms_payment": payment.name,
		"external_reference": payment.external_reference,
		"member": frappe.session.user,
		"doctype": doctype,
		"docname": docname,
		"payment_for": _payment_for_label(payment_for_certificate, doctype),
	}
	billing_slug = "certificate" if int(payment_for_certificate) else ("course" if doctype == "LMS Course" else "batch")
	checkout_url = f"{_get_public_base_url(settings)}{get_lms_route(f'billing/{billing_slug}/{docname}')}"
	transaction = _create_checkout_transaction(details, custom_data, checkout_url, settings=settings)
	payment.paddle_transaction_id = transaction.get("id")
	payment.order_id = transaction.get("id")
	payment.raw_response = _safe_json({"transaction": transaction})
	payment.save(ignore_permissions=True)

	_paddle_log(
		"Returning Paddle checkout",
		{
			"payment": payment.name,
			"transaction_id": transaction.get("id"),
			"member": payment.member,
			"doctype": doctype,
			"docname": docname,
			"payment_for_certificate": int(payment_for_certificate),
			"success_url": f"{_get_public_base_url(settings)}{redirect_to}",
		},
	)
	checkout = _checkout_payload_for_transaction(
		settings,
		transaction,
		custom_data,
		f"{_get_public_base_url(settings)}{redirect_to}",
		country or address.get("country"),
	)
	if paddle_discount:
		checkout["discount"] = {
			key: value for key, value in paddle_discount.items() if value
		}
	return {
		**checkout,
		"payment": payment.name,
		"transaction_id": transaction.get("id"),
		"amount": flt(details.total_amount),
		"currency": "USD",
		"title": details.title,
		"status": "created",
		"redirect_url": redirect_to,
	}


@frappe.whitelist()
def get_paddle_payment_status(payment: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to view payment status."), frappe.AuthenticationError)

	payment_doc = frappe.get_doc("LMS Payment", payment)
	if payment_doc.member != frappe.session.user:
		frappe.throw(_("You cannot view this payment."), frappe.PermissionError)

	return {
		"payment": payment_doc.name,
		"status": payment_doc.payment_status or ("completed" if payment_doc.payment_received else "pending"),
		"payment_received": bool(payment_doc.payment_received),
		"redirect_url": get_redirect_url(
			payment_doc.payment_for_document_type,
			payment_doc.payment_for_document,
			payment_doc.payment_for_certificate,
		),
	}


@frappe.whitelist()
def create_paddle_plus_checkout(country: str | None = None) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)
	if has_active_plus():
		return {"active": True, "redirect_url": f"{get_lms_path_url()}/plus?status=active"}

	settings = _ensure_enabled()
	price_id = getattr(settings, "paddle_plus_price_id", None)
	if not price_id:
		frappe.throw(_("Paddle Plus price ID is missing in StudyBadge Plus Settings."))

	plan = _get_plus_plan_for_currency("USD", settings)
	external_reference = f"studybadge-plus-paddle::{frappe.session.user}::{uuid.uuid4().hex}"
	_paddle_log(
		"Creating Paddle Plus checkout",
		{
			"member": frappe.session.user,
			"mode": getattr(settings, "paddle_mode", None) or "sandbox",
			"price_id": price_id,
			"country": country or _get_user_country(),
			"success_url": f"{get_lms_path_url(settings)}/plus?checkout=return&gateway=paddle",
		},
	)
	subscription = frappe.new_doc("StudyBadge Plus Subscription")
	subscription.update(
		{
			"member": frappe.session.user,
			"status": "pending",
			"payment_gateway": "Paddle",
			"external_reference": external_reference,
			"paddle_price_id": price_id,
			"amount": plan.get("amount"),
			"currency": "USD",
			"last_synced_at": now_datetime(),
		}
	)
	subscription.save(ignore_permissions=True)

	custom_data = {
		"gateway": "paddle",
		"payment_for": "plus",
		"member": frappe.session.user,
		"subscription": subscription.name,
		"external_reference": external_reference,
	}
	checkout = {
		**_checkout_payload(
			settings,
			price_id,
			custom_data,
			f"{get_lms_path_url(settings)}/plus?checkout=return&gateway=paddle",
			country or _get_user_country(),
		),
		"subscription": subscription.name,
		"external_reference": external_reference,
		"plan": plan,
	}
	_paddle_log(
		"Returning Paddle Plus checkout",
		{
			"member": frappe.session.user,
			"subscription": subscription.name,
			"mode": checkout.get("mode"),
			"price_id": checkout.get("price_id"),
			"customer": checkout.get("customer"),
			"success_url": checkout.get("success_url"),
			"custom_data": checkout.get("custom_data"),
		},
	)
	return checkout


def _get_payment_from_transaction(transaction: dict):
	custom_data = transaction.get("custom_data") if isinstance(transaction.get("custom_data"), dict) else {}
	payment_name = custom_data.get("lms_payment")
	if payment_name and frappe.db.exists("LMS Payment", payment_name):
		return frappe.get_doc("LMS Payment", payment_name)

	transaction_id = transaction.get("id")
	if transaction_id and frappe.db.exists("LMS Payment", {"paddle_transaction_id": transaction_id}):
		return frappe.get_doc(
			"LMS Payment",
			frappe.db.exists("LMS Payment", {"paddle_transaction_id": transaction_id}),
		)

	external_reference = custom_data.get("external_reference")
	if external_reference and frappe.db.exists("LMS Payment", {"external_reference": external_reference}):
		return frappe.get_doc(
			"LMS Payment",
			frappe.db.exists("LMS Payment", {"external_reference": external_reference}),
		)


def _money_from_transaction(transaction: dict):
	totals = transaction.get("details", {}).get("totals") if isinstance(transaction.get("details"), dict) else {}
	total = totals.get("total")
	currency = transaction.get("currency_code") or totals.get("currency_code")
	try:
		amount = flt(total) / 100 if total is not None else None
	except Exception:
		amount = None
	return amount, currency


def process_paddle_transaction(transaction: dict):
	payment_doc = _get_payment_from_transaction(transaction)
	if not payment_doc:
		return None

	transaction_id = transaction.get("id")
	status = _normalize_status(transaction.get("status"))
	already_received = bool(payment_doc.payment_received)
	payment_doc.update(
		{
			"payment_gateway": "Paddle",
			"payment_status": status,
			"payment_id": transaction_id or payment_doc.payment_id,
			"paddle_transaction_id": transaction_id or payment_doc.paddle_transaction_id,
			"raw_response": _safe_json(transaction),
		}
	)
	if status in PADDLE_PAID_TRANSACTION_STATUSES:
		payment_doc.payment_received = 1
	payment_doc.save(ignore_permissions=True)

	if payment_doc.payment_received and not already_received:
		complete_enrollment(
			payment_doc.name,
			payment_doc.payment_for_document_type,
			payment_doc.payment_for_document,
		)
		if payment_doc.payment_for_certificate:
			from lms.lms.doctype.lms_certificate.lms_certificate import auto_issue_course_certificate

			auto_issue_course_certificate(payment_doc.payment_for_document, payment_doc.member)
	return payment_doc


def _find_paddle_subscription(subscription: dict):
	custom_data = subscription.get("custom_data") if isinstance(subscription.get("custom_data"), dict) else {}
	local_subscription = custom_data.get("subscription")
	if local_subscription and frappe.db.exists("StudyBadge Plus Subscription", local_subscription):
		return frappe.get_doc("StudyBadge Plus Subscription", local_subscription)

	subscription_id = subscription.get("id")
	if subscription_id and frappe.db.exists("StudyBadge Plus Subscription", {"paddle_subscription_id": subscription_id}):
		return frappe.get_doc(
			"StudyBadge Plus Subscription",
			frappe.db.exists("StudyBadge Plus Subscription", {"paddle_subscription_id": subscription_id}),
		)

	external_reference = custom_data.get("external_reference")
	if external_reference and frappe.db.exists("StudyBadge Plus Subscription", {"external_reference": external_reference}):
		return frappe.get_doc(
			"StudyBadge Plus Subscription",
			frappe.db.exists("StudyBadge Plus Subscription", {"external_reference": external_reference}),
		)

	member = custom_data.get("member")
	if member and frappe.db.exists("User", member):
		doc = frappe.new_doc("StudyBadge Plus Subscription")
		doc.member = member
		return doc


def sync_paddle_subscription(subscription: dict):
	doc = _find_paddle_subscription(subscription)
	if not doc:
		frappe.log_error(_safe_json(subscription), "StudyBadge Paddle Subscription Not Found")
		return None

	custom_data = subscription.get("custom_data") if isinstance(subscription.get("custom_data"), dict) else {}
	items = subscription.get("items") or []
	price = ((items[0] or {}).get("price") if items else {}) or {}
	recurring_transaction = subscription.get("recurring_transaction_details") or {}
	totals = recurring_transaction.get("totals") or {}
	billing_period = subscription.get("current_billing_period") or {}
	scheduled_change = subscription.get("scheduled_change") or {}
	status = _normalize_status(subscription.get("status"))

	if doc.is_new() and custom_data.get("member"):
		doc.member = custom_data.get("member")

	doc.update(
		{
			"status": status,
			"payment_gateway": "Paddle",
			"paddle_customer_id": subscription.get("customer_id") or doc.paddle_customer_id,
			"paddle_subscription_id": subscription.get("id") or doc.paddle_subscription_id,
			"paddle_price_id": price.get("id") or doc.paddle_price_id,
			"paddle_transaction_id": subscription.get("first_billed_transaction_id")
			or doc.paddle_transaction_id,
			"external_reference": custom_data.get("external_reference") or doc.external_reference,
			"amount": flt(totals.get("total") or 0) / 100 if totals.get("total") else doc.amount,
			"currency": subscription.get("currency_code") or doc.currency or "USD",
			"next_payment_date": _parse_paddle_datetime(subscription.get("next_billed_at")),
			"date_created": _parse_paddle_datetime(subscription.get("created_at")),
			"last_modified": _parse_paddle_datetime(subscription.get("updated_at")),
			"last_synced_at": now_datetime(),
			"cancel_at_period_end": 1 if scheduled_change.get("action") == "cancel" else 0,
			"cancel_scheduled_for": _parse_paddle_datetime(scheduled_change.get("effective_at")),
			"raw_response": _safe_json(subscription),
		}
	)
	if not doc.next_payment_date and billing_period.get("ends_at"):
		doc.next_payment_date = _parse_paddle_datetime(billing_period.get("ends_at"))
	if status in PADDLE_TERMINAL_SUBSCRIPTION_STATUSES and status != "active":
		doc.cancel_at_period_end = 0
	doc.save(ignore_permissions=True)

	if status in PADDLE_ACTIVE_SUBSCRIPTION_STATUSES:
		from lms.lms.subscriptions import _send_plus_welcome_email

		_send_plus_welcome_email(doc)
	return doc


def _find_subscription_for_transaction(transaction: dict):
	subscription_id = transaction.get("subscription_id")
	if subscription_id and frappe.db.exists("StudyBadge Plus Subscription", {"paddle_subscription_id": subscription_id}):
		return frappe.get_doc(
			"StudyBadge Plus Subscription",
			frappe.db.exists("StudyBadge Plus Subscription", {"paddle_subscription_id": subscription_id}),
		)

	custom_data = transaction.get("custom_data") if isinstance(transaction.get("custom_data"), dict) else {}
	local_subscription = custom_data.get("subscription")
	if local_subscription and frappe.db.exists("StudyBadge Plus Subscription", local_subscription):
		return frappe.get_doc("StudyBadge Plus Subscription", local_subscription)


def _receipt_number(transaction: dict) -> str:
	identifier = str(transaction.get("id") or uuid.uuid4().hex)
	paid_at = _parse_paddle_datetime(transaction.get("billed_at") or transaction.get("created_at"))
	date_part = str(paid_at or now_datetime().date()).replace("-", "")[:8]
	return f"SBP-{date_part}-{identifier[-8:]}"


def sync_paddle_receipt(transaction: dict, subscription=None):
	transaction_id = transaction.get("id")
	if not transaction_id:
		return None

	subscription = subscription or _find_subscription_for_transaction(transaction)
	if not subscription:
		return None

	receipt_name = frappe.db.exists("StudyBadge Plus Receipt", {"paddle_transaction_id": transaction_id})
	if receipt_name:
		receipt = frappe.get_doc("StudyBadge Plus Receipt", receipt_name)
	else:
		receipt = frappe.new_doc("StudyBadge Plus Receipt")
		receipt.member = subscription.member
		receipt.subscription = subscription.name

	amount, currency = _money_from_transaction(transaction)
	receipt.update(
		{
			"receipt_number": receipt.receipt_number or _receipt_number(transaction),
			"status": _normalize_status(transaction.get("status")),
			"payment_gateway": "Paddle",
			"paddle_transaction_id": transaction_id,
			"paddle_subscription_id": transaction.get("subscription_id") or subscription.paddle_subscription_id,
			"paddle_customer_id": transaction.get("customer_id") or subscription.paddle_customer_id,
			"amount": amount or subscription.amount,
			"currency": currency or subscription.currency,
			"paid_at": _parse_paddle_datetime(transaction.get("billed_at") or transaction.get("created_at")),
			"date_created": _parse_paddle_datetime(transaction.get("created_at")),
			"last_modified": _parse_paddle_datetime(transaction.get("updated_at")),
			"raw_response": _safe_json(transaction),
		}
	)
	receipt.save(ignore_permissions=True)
	return receipt


def fetch_subscription(subscription_id: str, settings=None) -> dict:
	response = _request("GET", f"/subscriptions/{subscription_id}", settings=settings)
	return response.get("data") or response


def fetch_transaction(transaction_id: str, settings=None) -> dict:
	response = _request("GET", f"/transactions/{transaction_id}", settings=settings)
	return response.get("data") or response


def _maybe_sync_subscription_from_transaction(transaction: dict):
	subscription_id = transaction.get("subscription_id")
	if not subscription_id:
		return None
	try:
		subscription = fetch_subscription(subscription_id)
		return sync_paddle_subscription(subscription)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "StudyBadge Paddle Subscription Fetch Failed")
		return None


def _get_checkout_local_subscription(subscription_name: str | None, transaction: dict | None = None):
	transaction = transaction or {}
	custom_data = transaction.get("custom_data") if isinstance(transaction.get("custom_data"), dict) else {}
	candidates = [subscription_name, custom_data.get("subscription")]
	for candidate in candidates:
		if candidate and frappe.db.exists("StudyBadge Plus Subscription", candidate):
			doc = frappe.get_doc("StudyBadge Plus Subscription", candidate)
			if doc.member != frappe.session.user:
				frappe.throw(_("You cannot activate this subscription."), frappe.PermissionError)
			return doc

	member = custom_data.get("member")
	if member and member != frappe.session.user:
		frappe.throw(_("You cannot activate this subscription."), frappe.PermissionError)
	return None


def _transaction_has_price(transaction: dict, price_id: str | None) -> bool:
	if not price_id:
		return True
	for item in transaction.get("items") or []:
		price = item.get("price") if isinstance(item, dict) else {}
		item_price_id = item.get("price_id") or (price or {}).get("id")
		if item_price_id == price_id:
			return True
	return False


def _validate_plus_checkout_transaction(transaction: dict, local_subscription, settings):
	custom_data = transaction.get("custom_data") if isinstance(transaction.get("custom_data"), dict) else {}
	if not _transaction_has_price(transaction, getattr(settings, "paddle_plus_price_id", None)):
		frappe.throw(_("This Paddle transaction does not match the StudyBadge Plus price."))
	if custom_data.get("payment_for") and custom_data.get("payment_for") != "plus":
		frappe.throw(_("This Paddle transaction is not for StudyBadge Plus."))
	if custom_data.get("member") and custom_data.get("member") != frappe.session.user:
		frappe.throw(_("You cannot activate this subscription."), frappe.PermissionError)
	if (
		local_subscription
		and custom_data.get("subscription")
		and custom_data.get("subscription") != local_subscription.name
	):
		frappe.throw(_("This Paddle transaction does not match your subscription."))
	if not custom_data.get("member") and not custom_data.get("subscription"):
		frappe.throw(_("This Paddle transaction is missing StudyBadge checkout data."))


def _provision_plus_from_paid_transaction(transaction: dict, local_subscription=None):
	status = _normalize_status(transaction.get("status"))
	if status not in PADDLE_PAID_TRANSACTION_STATUSES:
		return local_subscription

	local_subscription = local_subscription or _find_subscription_for_transaction(transaction)
	if not local_subscription:
		return None

	local_subscription.update(
		{
			"status": "active",
			"payment_gateway": "Paddle",
			"paddle_customer_id": transaction.get("customer_id") or local_subscription.paddle_customer_id,
			"paddle_subscription_id": transaction.get("subscription_id")
			or local_subscription.paddle_subscription_id,
			"paddle_transaction_id": transaction.get("id") or local_subscription.paddle_transaction_id,
			"last_synced_at": now_datetime(),
			"raw_response": _safe_json(transaction),
		}
	)
	amount, currency = _money_from_transaction(transaction)
	if amount:
		local_subscription.amount = amount
	if currency:
		local_subscription.currency = currency
	local_subscription.save(ignore_permissions=True)
	sync_paddle_receipt(transaction, local_subscription)
	return local_subscription


@frappe.whitelist()
def sync_paddle_plus_checkout(transaction_id: str | None = None, subscription: str | None = None) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)
	if not transaction_id:
		from lms.lms.subscriptions import get_plus_billing

		return get_plus_billing()

	settings = _ensure_enabled()
	local_subscription = None
	transaction = None
	synced_subscription = None
	for attempt in range(4):
		transaction = fetch_transaction(transaction_id, settings=settings)
		local_subscription = _get_checkout_local_subscription(subscription, transaction)
		_validate_plus_checkout_transaction(transaction, local_subscription, settings)
		_paddle_log(
			"Syncing Paddle Plus checkout",
			{
				"attempt": attempt + 1,
				"member": frappe.session.user,
				"transaction_id": transaction.get("id"),
				"transaction_status": transaction.get("status"),
				"subscription_id": transaction.get("subscription_id"),
				"local_subscription": local_subscription.name if local_subscription else None,
			},
		)
		synced_subscription = _maybe_sync_subscription_from_transaction(transaction)
		if synced_subscription:
			sync_paddle_receipt(transaction, synced_subscription)
			break
		if transaction.get("subscription_id"):
			break
		if attempt < 3:
			time.sleep(1)

	if not synced_subscription and transaction:
		synced_subscription = _provision_plus_from_paid_transaction(transaction, local_subscription)

	frappe.db.commit()
	from lms.lms.subscriptions import get_plus_billing

	return get_plus_billing()


def _parse_signature(header: str | None) -> dict:
	parts = {}
	for part in (header or "").split(";"):
		if "=" not in part:
			continue
		key, value = part.split("=", 1)
		parts[key.strip()] = value.strip()
	return parts


def _verify_webhook_signature(raw_body: str, header: str | None, settings=None):
	signature = _parse_signature(header)
	timestamp = signature.get("ts")
	received_hash = signature.get("h1")
	if not timestamp or not received_hash:
		frappe.throw(_("Paddle webhook signature is missing."), frappe.PermissionError)

	try:
		if abs(datetime.now(timezone.utc).timestamp() - int(timestamp)) > 300:
			frappe.throw(_("Paddle webhook signature is too old."), frappe.PermissionError)
	except ValueError:
		frappe.throw(_("Paddle webhook signature timestamp is invalid."), frappe.PermissionError)

	signed_payload = f"{timestamp}:{raw_body}".encode()
	expected_hash = hmac.new(_webhook_secret(settings).encode(), signed_payload, sha256).hexdigest()
	if not hmac.compare_digest(expected_hash, received_hash):
		frappe.throw(_("Paddle webhook signature is invalid."), frappe.PermissionError)


@frappe.whitelist(allow_guest=True)
def paddle_webhook():
	settings = _ensure_enabled()
	raw_body = frappe.request.get_data(as_text=True)
	_verify_webhook_signature(raw_body, frappe.get_request_header("Paddle-Signature"), settings=settings)
	payload = json.loads(raw_body or "{}")
	event_type = payload.get("event_type") or payload.get("eventType")
	data = payload.get("data") or {}

	if event_type in {"transaction.completed", "transaction.paid"}:
		payment = process_paddle_transaction(data)
		subscription = _maybe_sync_subscription_from_transaction(data)
		if subscription:
			sync_paddle_receipt(data, subscription)
		frappe.db.commit()
		return {"ok": True, "payment": payment.name if payment else None, "subscription": subscription.name if subscription else None}

	if event_type == "transaction.payment_failed":
		payment = process_paddle_transaction(data)
		frappe.db.commit()
		return {"ok": True, "payment": payment.name if payment else None}

	if event_type in {"subscription.created", "subscription.updated", "subscription.canceled"}:
		subscription = sync_paddle_subscription(data)
		frappe.db.commit()
		return {"ok": True, "subscription": subscription.name if subscription else None}

	return {"ok": True, "ignored": event_type}


@frappe.whitelist()
def create_customer_portal_session(action: str | None = None) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to manage your Plus subscription."), frappe.AuthenticationError)

	subscription_rows = frappe.get_all(
		"StudyBadge Plus Subscription",
		{"member": frappe.session.user, "payment_gateway": "Paddle"},
		["name"],
		order_by="modified desc",
		limit=1,
	)
	subscription = frappe.get_doc("StudyBadge Plus Subscription", subscription_rows[0].name) if subscription_rows else None
	if not subscription or not subscription.paddle_customer_id:
		frappe.throw(_("This subscription is missing its Paddle customer ID."))
	if not subscription.paddle_subscription_id:
		frappe.throw(_("This subscription is missing its Paddle subscription ID."))

	response = _request(
		"POST",
		f"/customers/{subscription.paddle_customer_id}/portal-sessions",
		data=json.dumps({"subscription_ids": [subscription.paddle_subscription_id]}),
	)
	data = response.get("data") or response
	urls = data.get("urls") or {}
	subscription_urls = urls.get("subscriptions") or []
	subscription_links = subscription_urls[0] if subscription_urls else {}
	return {
		"overview_url": (urls.get("general") or {}).get("overview"),
		"cancel_url": subscription_links.get("cancel_subscription"),
		"payment_method_url": subscription_links.get("update_subscription_payment_method"),
		"url": (
			subscription_links.get("cancel_subscription")
			if action == "cancel"
			else subscription_links.get("update_subscription_payment_method")
			if action == "payment_method"
			else (urls.get("general") or {}).get("overview")
		),
	}


def cancel_subscription(subscription_id: str, immediately: bool = False):
	payload = {"effective_from": "immediately" if immediately else "next_billing_period"}
	response = _request("POST", f"/subscriptions/{subscription_id}/cancel", data=json.dumps(payload))
	return sync_paddle_subscription(response.get("data") or response)
