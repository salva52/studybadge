import json
import uuid

import frappe
import requests
from frappe import _
from frappe.utils import flt, now_datetime

from lms.lms.utils import complete_enrollment

PAYPAL_API_BASES = {
	"sandbox": "https://api-m.sandbox.paypal.com",
	"live": "https://api-m.paypal.com",
}
PAYPAL_ACTIVE_SUBSCRIPTION_STATUSES = {"ACTIVE", "APPROVAL_PENDING", "APPROVED"}


def _get_settings():
	settings = frappe.get_single("StudyBadge Plus Settings")
	if not settings.enabled:
		frappe.throw(_("StudyBadge Plus is not enabled."))
	return settings


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


def _get_public_base_url(settings) -> str:
	return (settings.public_base_url or frappe.utils.get_url()).rstrip("/")


def _api_base(settings=None) -> str:
	settings = settings or _get_settings()
	mode = (getattr(settings, "paypal_mode", None) or "sandbox").lower()
	return PAYPAL_API_BASES.get(mode, PAYPAL_API_BASES["sandbox"])


def _client_id(settings=None) -> str:
	settings = settings or _get_settings()
	client_id = getattr(settings, "paypal_client_id", None)
	if not client_id:
		frappe.throw(_("PayPal client ID is missing in StudyBadge Plus Settings."))
	return client_id


def _client_secret(settings=None) -> str:
	settings = settings or _get_settings()
	client_secret = _get_password(settings, "paypal_client_secret")
	if not client_secret:
		frappe.throw(_("PayPal client secret is missing in StudyBadge Plus Settings."))
	return client_secret


def _ensure_enabled(settings=None):
	settings = settings or _get_settings()
	if not getattr(settings, "paypal_enabled", 0):
		frappe.throw(_("PayPal is not enabled in StudyBadge Plus Settings."))
	return settings


def _access_token(settings=None) -> str:
	settings = _ensure_enabled(settings)
	response = requests.post(
		f"{_api_base(settings)}/v1/oauth2/token",
		auth=(_client_id(settings), _client_secret(settings)),
		headers={"Content-Type": "application/x-www-form-urlencoded"},
		data={"grant_type": "client_credentials"},
		timeout=20,
	)
	payload = _json_response(response)
	if response.status_code >= 400:
		_log_error(payload, "StudyBadge PayPal OAuth Error")
		frappe.throw(_("PayPal authentication failed. Please check your keys."))
	return payload.get("access_token")


def _headers(settings=None) -> dict:
	return {
		"Authorization": f"Bearer {_access_token(settings)}",
		"Content-Type": "application/json",
	}


def _json_response(response) -> dict:
	try:
		return response.json()
	except ValueError:
		return {"message": response.text}


def _log_error(payload, title):
	frappe.log_error(json.dumps(payload, indent=2, default=str), title)


def _request(method: str, path: str, settings=None, **kwargs) -> dict:
	settings = _ensure_enabled(settings)
	response = requests.request(
		method,
		f"{_api_base(settings)}{path}",
		headers=_headers(settings),
		timeout=20,
		**kwargs,
	)
	payload = _json_response(response)
	if response.status_code >= 400:
		_log_error(payload, "StudyBadge PayPal Error")
		frappe.throw(_("PayPal could not process this payment. Please try again."))
	return payload


def _safe_json(data: dict | list | None) -> str:
	return json.dumps(data or {}, indent=2, sort_keys=True, default=str)


def _approval_link(order: dict) -> str | None:
	for link in order.get("links") or []:
		if link.get("rel") == "approve":
			return link.get("href")
	return None


def _amount_value(amount) -> str:
	return f"{flt(amount):.2f}"


def get_checkout_config() -> dict:
	settings = _ensure_enabled()
	return {
		"enabled": bool(getattr(settings, "paypal_enabled", 0)),
		"mode": getattr(settings, "paypal_mode", None) or "sandbox",
		"client_id": _client_id(settings),
	}


def create_order(payment_doc, details, return_path: str, cancel_path: str) -> dict:
	if details.currency != "USD":
		frappe.throw(_("PayPal payments must be created in USD."))

	settings = _ensure_enabled()
	base_url = _get_public_base_url(settings)
	payload = {
		"intent": "CAPTURE",
		"purchase_units": [
			{
				"reference_id": payment_doc.name,
				"custom_id": payment_doc.external_reference,
				"description": f"{details.title}",
				"amount": {
					"currency_code": "USD",
					"value": _amount_value(details.total_amount),
				},
			}
		],
		"application_context": {
			"brand_name": "StudyBadge",
			"shipping_preference": "NO_SHIPPING",
			"user_action": "PAY_NOW",
			"return_url": f"{base_url}{return_path}",
			"cancel_url": f"{base_url}{cancel_path}",
		},
	}
	order = _request("POST", "/v2/checkout/orders", settings=settings, data=json.dumps(payload))
	payment_doc.order_id = order.get("id")
	payment_doc.raw_response = _safe_json({"order": order})
	payment_doc.save(ignore_permissions=True)
	return {
		"order_id": order.get("id"),
		"approval_url": _approval_link(order),
		"client_id": _client_id(settings),
	}


def capture_order(order_id: str) -> dict:
	return _request("POST", f"/v2/checkout/orders/{order_id}/capture")


def get_order(order_id: str) -> dict:
	return _request("GET", f"/v2/checkout/orders/{order_id}")


def _capture_details(order: dict) -> dict:
	purchase_units = order.get("purchase_units") or []
	payments = (purchase_units[0].get("payments") if purchase_units else {}) or {}
	captures = payments.get("captures") or []
	capture = captures[0] if captures else {}
	return {
		"capture": capture,
		"capture_id": capture.get("id"),
		"capture_status": capture.get("status"),
		"status_detail": ((capture.get("status_details") or {}).get("reason")),
	}


def process_captured_order(order: dict, payment_doc=None):
	details = _capture_details(order)
	payment_doc = payment_doc or _get_payment_from_order(order)
	if not payment_doc:
		frappe.log_error(_safe_json(order), "StudyBadge PayPal Payment Not Found")
		return None

	already_received = bool(payment_doc.payment_received)
	status = details.get("capture_status") or order.get("status")
	payment_doc.update(
		{
			"payment_gateway": "PayPal",
			"payment_status": status,
			"payment_status_detail": details.get("status_detail"),
			"payment_id": details.get("capture_id") or payment_doc.payment_id,
			"order_id": order.get("id") or payment_doc.order_id,
			"raw_response": _safe_json(order),
		}
	)
	if status == "COMPLETED":
		payment_doc.payment_received = 1
	payment_doc.save(ignore_permissions=True)

	if payment_doc.payment_received and not already_received and (
		payment_doc.payment_for_certificate or frappe.session.user != "Guest"
	):
		complete_enrollment(
			payment_doc.name,
			payment_doc.payment_for_document_type,
			payment_doc.payment_for_document,
		)
		if payment_doc.payment_for_certificate:
			from lms.lms.doctype.lms_certificate.lms_certificate import auto_issue_course_certificate

			auto_issue_course_certificate(payment_doc.payment_for_document, payment_doc.member)
	return payment_doc


def _get_payment_from_order(order: dict):
	purchase_units = order.get("purchase_units") or []
	reference_id = purchase_units[0].get("reference_id") if purchase_units else None
	custom_id = purchase_units[0].get("custom_id") if purchase_units else None
	if reference_id and frappe.db.exists("LMS Payment", reference_id):
		return frappe.get_doc("LMS Payment", reference_id)
	if custom_id and frappe.db.exists("LMS Payment", {"external_reference": custom_id}):
		return frappe.get_doc("LMS Payment", frappe.db.exists("LMS Payment", {"external_reference": custom_id}))


def create_pending_plus_subscription(currency: str = "USD") -> dict:
	settings = _ensure_enabled()
	if currency != "USD":
		frappe.throw(_("PayPal Plus subscriptions are only available in USD."))
	if not getattr(settings, "paypal_plus_plan_id_usd", None):
		frappe.throw(_("PayPal Plus plan ID for USD is missing in StudyBadge Plus Settings."))

	external_reference = f"studybadge-plus-paypal::{frappe.session.user}::{uuid.uuid4().hex}"
	subscription = frappe.new_doc("StudyBadge Plus Subscription")
	subscription.update(
		{
			"member": frappe.session.user,
			"status": "pending",
			"payment_gateway": "PayPal",
			"external_reference": external_reference,
			"paypal_plan_id": settings.paypal_plus_plan_id_usd,
			"amount": flt(getattr(settings, "plus_amount_usd", 0) or 9.9),
			"currency": "USD",
			"last_synced_at": now_datetime(),
		}
	)
	subscription.save(ignore_permissions=True)
	return {
		"subscription": subscription.name,
		"client_id": _client_id(settings),
		"plan_id": settings.paypal_plus_plan_id_usd,
		"external_reference": external_reference,
	}


def fetch_subscription(subscription_id: str) -> dict:
	return _request("GET", f"/v1/billing/subscriptions/{subscription_id}")


def cancel_subscription(subscription_id: str, reason: str | None = None):
	payload = {"reason": reason or "Cancelled from StudyBadge"}
	return _request("POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", data=json.dumps(payload))


def _normalize_subscription_status(status: str | None) -> str:
	status = (status or "unknown").lower()
	if status == "active":
		return "active"
	if status in {"approval_pending", "approved"}:
		return "authorized"
	if status in {"cancelled", "cancelled_by_payer", "expired"}:
		return "cancelled"
	if status in {"suspended"}:
		return "paused"
	return status if status in {"pending", "paused", "cancelled", "expired", "rejected"} else "unknown"


def sync_plus_subscription(paypal_subscription: dict, local_subscription: str | None = None):
	subscription_id = paypal_subscription.get("id")
	custom_id = paypal_subscription.get("custom_id")
	doc = None
	if local_subscription and frappe.db.exists("StudyBadge Plus Subscription", local_subscription):
		doc = frappe.get_doc("StudyBadge Plus Subscription", local_subscription)
	elif subscription_id and frappe.db.exists(
		"StudyBadge Plus Subscription", {"paypal_subscription_id": subscription_id}
	):
		doc = frappe.get_doc(
			"StudyBadge Plus Subscription",
			frappe.db.exists("StudyBadge Plus Subscription", {"paypal_subscription_id": subscription_id}),
		)
	elif custom_id and frappe.db.exists("StudyBadge Plus Subscription", {"external_reference": custom_id}):
		doc = frappe.get_doc(
			"StudyBadge Plus Subscription",
			frappe.db.exists("StudyBadge Plus Subscription", {"external_reference": custom_id}),
		)

	if not doc:
		frappe.log_error(_safe_json(paypal_subscription), "StudyBadge PayPal Subscription Not Found")
		return None

	billing_info = paypal_subscription.get("billing_info") or {}
	last_payment = billing_info.get("last_payment") or {}
	amount = last_payment.get("amount") or {}
	doc.update(
		{
			"status": _normalize_subscription_status(paypal_subscription.get("status")),
			"payment_gateway": "PayPal",
			"paypal_subscription_id": subscription_id,
			"paypal_plan_id": paypal_subscription.get("plan_id") or doc.paypal_plan_id,
			"external_reference": custom_id or doc.external_reference,
			"amount": flt(doc.amount or amount.get("value") or 9.9),
			"currency": doc.currency or amount.get("currency_code") or "USD",
			"next_payment_date": billing_info.get("next_billing_time"),
			"date_created": paypal_subscription.get("create_time"),
			"last_modified": paypal_subscription.get("update_time"),
			"last_synced_at": now_datetime(),
			"raw_response": _safe_json(paypal_subscription),
		}
	)
	doc.save(ignore_permissions=True)
	return doc


def _paypal_receipt_number(resource: dict) -> str:
	identifier = str(resource.get("id") or uuid.uuid4().hex)
	date_part = str(now_datetime().date()).replace("-", "")
	return f"SBP-{date_part}-{identifier[-8:]}"


def sync_plus_receipt(resource: dict):
	subscription_id = (
		resource.get("billing_agreement_id")
		or resource.get("subscription_id")
		or (resource.get("supplementary_data") or {}).get("related_ids", {}).get("subscription_id")
	)
	if not subscription_id:
		return None
	subscription_name = frappe.db.exists(
		"StudyBadge Plus Subscription",
		{"paypal_subscription_id": subscription_id},
	)
	if not subscription_name:
		return None
	subscription = frappe.get_doc("StudyBadge Plus Subscription", subscription_name)
	capture_id = resource.get("id")
	receipt_name = capture_id and frappe.db.exists(
		"StudyBadge Plus Receipt",
		{"paypal_capture_id": capture_id},
	)
	receipt = frappe.get_doc("StudyBadge Plus Receipt", receipt_name) if receipt_name else frappe.new_doc("StudyBadge Plus Receipt")
	amount = resource.get("amount") or {}
	receipt.update(
		{
			"member": subscription.member,
			"subscription": subscription.name,
			"receipt_number": receipt.receipt_number or _paypal_receipt_number(resource),
			"status": resource.get("status"),
			"status_detail": (resource.get("status_details") or {}).get("reason"),
			"payment_gateway": "PayPal",
			"paypal_capture_id": capture_id,
			"paypal_subscription_id": subscription_id,
			"amount": amount.get("value"),
			"currency": amount.get("currency_code") or subscription.currency or "USD",
			"paid_at": resource.get("create_time") or now_datetime(),
			"date_created": resource.get("create_time"),
			"last_modified": resource.get("update_time"),
			"raw_response": _safe_json(resource),
		}
	)
	receipt.save(ignore_permissions=True)
	return receipt


def verify_webhook_signature(payload: dict) -> bool:
	settings = _ensure_enabled()
	webhook_id = getattr(settings, "paypal_webhook_id", None)
	if not webhook_id:
		frappe.throw(_("PayPal webhook ID is missing in StudyBadge Plus Settings."), frappe.PermissionError)

	headers = frappe.request.headers
	verification = {
		"auth_algo": headers.get("PAYPAL-AUTH-ALGO"),
		"cert_url": headers.get("PAYPAL-CERT-URL"),
		"transmission_id": headers.get("PAYPAL-TRANSMISSION-ID"),
		"transmission_sig": headers.get("PAYPAL-TRANSMISSION-SIG"),
		"transmission_time": headers.get("PAYPAL-TRANSMISSION-TIME"),
		"webhook_id": webhook_id,
		"webhook_event": payload,
	}
	response = _request(
		"POST",
		"/v1/notifications/verify-webhook-signature",
		settings=settings,
		data=json.dumps(verification),
	)
	return response.get("verification_status") == "SUCCESS"


def _get_request_json() -> dict:
	try:
		return frappe.request.get_json(silent=True) or {}
	except Exception:
		try:
			return json.loads(frappe.request.get_data(as_text=True) or "{}")
		except Exception:
			return {}


def _record_paypal_event(payload: dict):
	event_id = payload.get("id")
	if event_id and frappe.db.exists("StudyBadge PayPal Event", {"event_id": event_id}):
		event = frappe.get_doc(
			"StudyBadge PayPal Event",
			frappe.db.exists("StudyBadge PayPal Event", {"event_id": event_id}),
		)
		return event, bool(event.processed)

	event = frappe.new_doc("StudyBadge PayPal Event")
	event.update(
		{
			"event_id": event_id,
			"event_type": payload.get("event_type"),
			"resource_id": (payload.get("resource") or {}).get("id"),
			"payload": _safe_json(payload),
		}
	)
	event.save(ignore_permissions=True)
	return event, False


@frappe.whitelist(allow_guest=True)
def paypal_webhook():
	payload = _get_request_json()
	if not verify_webhook_signature(payload):
		frappe.throw(_("Invalid PayPal webhook signature."), frappe.PermissionError)

	event, already_processed = _record_paypal_event(payload)
	if already_processed:
		return {"status": "ok", "duplicate": True}

	event_type = payload.get("event_type")
	resource = payload.get("resource") or {}
	if event_type in {"BILLING.SUBSCRIPTION.ACTIVATED", "BILLING.SUBSCRIPTION.UPDATED", "BILLING.SUBSCRIPTION.CANCELLED", "BILLING.SUBSCRIPTION.SUSPENDED"}:
		subscription = sync_plus_subscription(resource)
		if subscription:
			event.subscription = subscription.name
	elif event_type in {"BILLING.SUBSCRIPTION.PAYMENT.SUCCEEDED", "PAYMENT.SALE.COMPLETED"}:
		receipt = sync_plus_receipt(resource)
		if receipt:
			event.subscription = receipt.subscription
	elif event_type in {"CHECKOUT.ORDER.APPROVED", "PAYMENT.CAPTURE.COMPLETED"}:
		order_id = resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id") or resource.get("id")
		if order_id:
			order = get_order(order_id)
			payment = process_captured_order(order)
			if payment:
				event.payment = payment.name

	event.processed = 1
	event.save(ignore_permissions=True)
	return {"status": "ok"}
