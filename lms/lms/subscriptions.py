import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone
from urllib.parse import quote

import frappe
import requests
from frappe import _
from frappe.utils import cint, flt, format_datetime, now_datetime

from lms.lms.utils import get_lms_path, get_preferred_payment_currency

MERCADOPAGO_API_BASE = "https://api.mercadopago.com"
PLUS_ACTIVE_STATUSES = {"authorized", "active", "trialing"}
KNOWN_SUBSCRIPTION_STATUSES = {
	"pending",
	"authorized",
	"active",
	"trialing",
	"past_due",
	"paused",
	"cancelled",
	"canceled",
	"expired",
	"rejected",
	"unknown",
}


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


def _get_access_token(settings=None) -> str:
	settings = settings or _get_settings()
	access_token = _get_password(settings, "access_token")
	if not access_token:
		frappe.throw(_("Mercado Pago access token is missing in StudyBadge Plus Settings."))
	return access_token


def _get_webhook_secret(settings=None) -> str:
	settings = settings or _get_settings()
	webhook_secret = _get_password(settings, "webhook_secret")
	if not webhook_secret:
		frappe.throw(_("Mercado Pago webhook secret is missing in StudyBadge Plus Settings."))
	return webhook_secret


def _get_public_base_url(settings) -> str:
	return (settings.public_base_url or frappe.utils.get_url()).rstrip("/")


def _get_plus_plan(settings=None) -> dict:
	settings = settings or _get_settings()
	amount_pen = flt(getattr(settings, "plus_amount_pen", 0) or settings.amount or 29.9)
	amount_usd = flt(getattr(settings, "plus_amount_usd", 0) or 9.9)
	return {
		"enabled": bool(settings.enabled),
		"plan_name": settings.plan_name,
		"amount": amount_pen,
		"currency": "PEN",
		"amount_pen": amount_pen,
		"amount_usd": amount_usd,
		"frequency": settings.frequency or 1,
		"frequency_type": settings.frequency_type or "months",
	}


def _get_plus_plan_for_currency(currency: str | None = None, settings=None) -> dict:
	plan = _get_plus_plan(settings)
	currency = (currency or "PEN").upper()
	if currency == "USD":
		plan["amount"] = plan["amount_usd"]
		plan["currency"] = "USD"
	else:
		plan["amount"] = plan["amount_pen"]
		plan["currency"] = "PEN"
	return plan


def _headers(settings=None) -> dict:
	return {
		"Authorization": f"Bearer {_get_access_token(settings)}",
		"Content-Type": "application/json",
	}


def _request(method: str, path: str, settings=None, **kwargs) -> dict:
	response = requests.request(
		method,
		f"{MERCADOPAGO_API_BASE}{path}",
		headers=_headers(settings),
		timeout=20,
		**kwargs,
	)
	try:
		payload = response.json()
	except ValueError:
		payload = {"message": response.text}

	if response.status_code >= 400:
		frappe.log_error(
			json.dumps(payload, indent=2, default=str),
			"StudyBadge Plus Mercado Pago Error",
		)
		frappe.throw(_("Mercado Pago rejected the subscription request. Please try again later."))

	return payload


def _normalize_status(status: str | None) -> str:
	status = (status or "unknown").lower()
	return status if status in KNOWN_SUBSCRIPTION_STATUSES else "unknown"


def _safe_json(data: dict | list | None) -> str:
	return json.dumps(data or {}, indent=2, sort_keys=True, default=str)


def _clean(value):
	return value if value not in ("", None) else None


def _get_payment_status(payment: dict) -> str | None:
	if isinstance(payment.get("payment"), dict):
		return payment.get("payment", {}).get("status") or payment.get("status")
	return payment.get("status")


def _get_payment_status_detail(payment: dict) -> str | None:
	if isinstance(payment.get("payment"), dict):
		return payment.get("payment", {}).get("status_detail") or payment.get("status_detail")
	return payment.get("status_detail")


def _get_payment_id(payment: dict) -> str | None:
	nested_payment = payment.get("payment") if isinstance(payment.get("payment"), dict) else {}
	payment_id = _clean(nested_payment.get("id") or payment.get("payment_id") or payment.get("payment"))
	return str(payment_id) if payment_id else None


def _receipt_number(payment: dict) -> str:
	identifier = str(payment.get("id") or _get_payment_id(payment) or uuid.uuid4().hex)
	date_value = _parse_mp_datetime(payment.get("debit_date") or payment.get("date_created"))
	date_part = str(date_value or now_datetime().date()).replace("-", "")[:8]
	return f"SBP-{date_part}-{identifier[-8:]}"


def _parse_mp_datetime(value: str | None):
	if not value:
		return None

	try:
		parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
		if parsed.tzinfo:
			parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
		return parsed.strftime("%Y-%m-%d %H:%M:%S")
	except ValueError:
		return value


def _get_latest_subscription(member: str):
	subscription = frappe.get_all(
		"StudyBadge Plus Subscription",
		{"member": member},
		["name"],
		order_by="modified desc",
		limit=1,
	)
	if subscription:
		return frappe.get_doc("StudyBadge Plus Subscription", subscription[0].name)


def _get_pending_subscription(member: str):
	subscription = frappe.get_all(
		"StudyBadge Plus Subscription",
		{
			"member": member,
			"status": "pending",
			"init_point": ["is", "set"],
		},
		["name"],
		order_by="modified desc",
		limit=1,
	)
	if subscription:
		return frappe.get_doc("StudyBadge Plus Subscription", subscription[0].name)


def _find_subscription(mp_subscription: dict):
	mp_preapproval_id = mp_subscription.get("id")
	external_reference = mp_subscription.get("external_reference")

	for filters in (
		{"mp_preapproval_id": mp_preapproval_id} if mp_preapproval_id else None,
		{"external_reference": external_reference} if external_reference else None,
	):
		if not filters:
			continue
		name = frappe.db.exists("StudyBadge Plus Subscription", filters)
		if name:
			return frappe.get_doc("StudyBadge Plus Subscription", name)

	payer_email = mp_subscription.get("payer_email")
	if payer_email and frappe.db.exists("User", payer_email):
		return frappe.new_doc("StudyBadge Plus Subscription")


def _get_card_details(mp_subscription: dict) -> dict:
	card = mp_subscription.get("card") if isinstance(mp_subscription.get("card"), dict) else {}
	payment_method = (
		mp_subscription.get("payment_method")
		if isinstance(mp_subscription.get("payment_method"), dict)
		else {}
	)
	payment_method_id = (
		mp_subscription.get("payment_method_id")
		or card.get("payment_method_id")
		or payment_method.get("id")
	)
	return {
		"payment_method_id": payment_method_id,
		"payment_method_name": payment_method.get("name") or payment_method_id,
		"card_last_four": card.get("last_four_digits") or card.get("last_four"),
		"card_brand": card.get("payment_method_id") or payment_method_id,
	}


def _send_plus_welcome_email(subscription, settings=None):
	if cint(getattr(subscription, "welcome_email_sent", 0)):
		return
	if subscription.status not in PLUS_ACTIVE_STATUSES:
		return

	settings = settings or _get_settings()
	member_name = frappe.db.get_value("User", subscription.member, "full_name") or subscription.member
	next_payment = (
		format_datetime(subscription.next_payment_date) if subscription.next_payment_date else _("pending")
	)
	try:
		frappe.sendmail(
			recipients=[subscription.member],
			subject=_("Welcome to StudyBadge Plus"),
			message=frappe.render_template(
				"""
				<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f8fafc; padding: 20px; border-radius: 8px;">
					<div style="background-color: #ffffff; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border-top: 5px solid #2563eb;">
						<h2 style="color: #1e293b; margin-top: 0; font-size: 24px; font-weight: 700;">¡Hola {{ member_name }}! 👋</h2>
						
						<p style="color: #475569; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
							¡Excelente noticia! Tu suscripción a <strong style="color: #2563eb;">{{ plan_name }}</strong> ya está 100% activa.
						</p>

						<div style="background-color: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
							<p style="margin: 0; color: #0369a1; font-size: 15px; font-weight: 600;">
								✨ Nuevos beneficios desbloqueados:
							</p>
							<ul style="margin: 12px 0 0 0; color: #0c4a6e; font-size: 15px; line-height: 1.6; padding-left: 20px;">
								<li><strong>Certificados verificables</strong> para tus cursos.</li>
								<li>Acceso a <strong>TutorIA</strong> sin restricciones.</li>
								<li><strong>Insignia exclusiva</strong> Plus/PRO en tu perfil público.</li>
							</ul>
						</div>

						<div style="border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; padding: 16px 0; margin-bottom: 24px;">
							<p style="margin: 0; color: #64748b; font-size: 14px;">Próximo cobro programado:</p>
							<p style="margin: 4px 0 0 0; color: #0f172a; font-size: 18px; font-weight: 600;">{{ next_payment }}</p>
						</div>
						
						<div style="text-align: center; margin: 32px 0;">
							<a href="{{ billing_url }}" style="background-color: #2563eb; color: #ffffff; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 16px; display: inline-block;">Gestionar mi plan</a>
						</div>

						<p style="color: #64748b; font-size: 15px; line-height: 1.6; margin-bottom: 0;">
							Gracias por seguir aprendiendo con nosotros y ser parte fundamental de nuestra comunidad.<br><br>
							Saludos,<br>
							<strong>El equipo de StudyBadge</strong>
						</p>
					</div>
				</div>
				""",
				{
					"member_name": member_name,
					"plan_name": settings.plan_name or "StudyBadge Plus",
					"next_payment": next_payment,
					"billing_url": f"{get_lms_path_url(settings)}/plus",
				},
			),
			now=True,
		)
		subscription.welcome_email_sent = 1
		subscription.welcome_email_sent_at = now_datetime()
		subscription.save(ignore_permissions=True)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "StudyBadge Plus Welcome Email Failed")


def _sync_subscription(mp_subscription: dict):
	doc = _find_subscription(mp_subscription)
	if not doc:
		frappe.log_error(
			_safe_json(mp_subscription),
			"StudyBadge Plus Subscription Not Found",
		)
		return None

	auto_recurring = mp_subscription.get("auto_recurring") or {}
	payer_email = mp_subscription.get("payer_email")
	if doc.is_new():
		doc.member = payer_email

	status = _normalize_status(mp_subscription.get("status"))
	card_details = _get_card_details(mp_subscription)
	doc.update(
		{
			"status": status,
			"payment_gateway": "Mercado Pago",
			"mp_preapproval_id": mp_subscription.get("id"),
			"external_reference": mp_subscription.get("external_reference"),
			"init_point": mp_subscription.get("init_point"),
			"amount": auto_recurring.get("transaction_amount"),
			"currency": auto_recurring.get("currency_id"),
			"payment_method_id": card_details.get("payment_method_id"),
			"payment_method_name": card_details.get("payment_method_name"),
			"card_last_four": card_details.get("card_last_four"),
			"card_brand": card_details.get("card_brand"),
			"next_payment_date": _parse_mp_datetime(mp_subscription.get("next_payment_date")),
			"date_created": _parse_mp_datetime(mp_subscription.get("date_created")),
			"last_modified": _parse_mp_datetime(mp_subscription.get("last_modified")),
			"last_synced_at": now_datetime(),
			"raw_response": _safe_json(mp_subscription),
		}
	)
	if status in {"cancelled", "canceled", "expired", "rejected"}:
		doc.cancel_at_period_end = 0
	doc.save(ignore_permissions=True)
	_send_plus_welcome_email(doc)
	return doc


def _refresh_subscription_from_mercadopago(subscription, settings=None):
	if not subscription or not subscription.mp_preapproval_id:
		return subscription
	settings = settings or _get_settings()
	try:
		mp_subscription = _fetch_mp_subscription(subscription.mp_preapproval_id, settings=settings)
		return _sync_subscription(mp_subscription) or subscription
	except Exception:
		frappe.log_error(
			frappe.get_traceback(),
			f"StudyBadge Plus Subscription Refresh Failed: {subscription.name}",
		)
		return subscription


def has_active_plus(user: str | None = None) -> bool:
	user = user or frappe.session.user
	if not user or user == "Guest":
		return False

	return bool(
		frappe.db.exists(
			"StudyBadge Plus Subscription",
			{
				"member": user,
				"status": ["in", list(PLUS_ACTIVE_STATUSES)],
			},
		)
	)


@frappe.whitelist()
def get_plus_status() -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to view your Plus status."), frappe.AuthenticationError)

	preferred_currency = get_preferred_payment_currency()
	plan = _get_plus_plan_for_currency(preferred_currency)
	subscription = _get_latest_subscription(frappe.session.user)
	if subscription and getattr(subscription, "mp_preapproval_id", None):
		subscription = _refresh_subscription_from_mercadopago(subscription)
	elif subscription and getattr(subscription, "paddle_subscription_id", None):
		try:
			from lms.lms.paddle import fetch_subscription, sync_paddle_subscription

			subscription = sync_paddle_subscription(fetch_subscription(subscription.paddle_subscription_id)) or subscription
		except Exception:
			frappe.log_error(frappe.get_traceback(), "StudyBadge Plus Paddle Refresh Failed")
	data = {
		"active": has_active_plus(),
		"plan": plan,
		"plans": {
			"PEN": _get_plus_plan_for_currency("PEN"),
			"USD": _get_plus_plan_for_currency("USD"),
		},
		"preferred_payment_currency": preferred_currency,
		"subscription": None,
	}

	if subscription:
		data["subscription"] = _serialize_subscription(subscription)

	return data


@frappe.whitelist()
def create_plus_checkout(currency: str | None = "PEN") -> str:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)

	settings = _get_settings()
	currency = (currency or "PEN").upper()
	if currency == "USD":
		frappe.throw(_("Use PayPal checkout for USD Plus subscriptions."))
	if has_active_plus():
		return f"{get_lms_path_url(settings)}/plus?status=active"

	pending = _get_pending_subscription(frappe.session.user)
	if pending and pending.init_point:
		pending = _refresh_subscription_from_mercadopago(pending, settings=settings)
		if pending.status in PLUS_ACTIVE_STATUSES:
			return f"{get_lms_path_url(settings)}/plus?status=active"
		return pending.init_point

	base_url = _get_public_base_url(settings)
	external_reference = f"studybadge-plus::{frappe.session.user}::{uuid.uuid4().hex}"
	notification_url = (
		f"{base_url}/api/method/lms.lms.subscriptions.mercadopago_webhook"
		"?source_news=webhooks"
	)
	payload = {
		"reason": settings.plan_name or "StudyBadge Plus",
		"external_reference": external_reference,
		"payer_email": frappe.session.user,
		"back_url": f"{base_url}/{get_lms_path()}/plus?checkout=return",
		"notification_url": notification_url,
		"auto_recurring": {
			"frequency": settings.frequency or 1,
			"frequency_type": settings.frequency_type or "months",
			"transaction_amount": flt(getattr(settings, "plus_amount_pen", 0) or settings.amount or 29.9),
			"currency_id": "PEN",
		},
		"status": "pending",
	}

	response = _request("POST", "/preapproval", settings=settings, data=json.dumps(payload))
	subscription = frappe.new_doc("StudyBadge Plus Subscription")
	subscription.update(
		{
			"member": frappe.session.user,
			"status": _normalize_status(response.get("status")),
			"payment_gateway": "Mercado Pago",
			"mp_preapproval_id": response.get("id"),
			"external_reference": response.get("external_reference") or external_reference,
			"init_point": response.get("init_point"),
			"amount": flt(getattr(settings, "plus_amount_pen", 0) or settings.amount or 29.9),
			"currency": "PEN",
			"next_payment_date": _parse_mp_datetime(response.get("next_payment_date")),
			"date_created": _parse_mp_datetime(response.get("date_created")),
			"last_modified": _parse_mp_datetime(response.get("last_modified")),
			"last_synced_at": now_datetime(),
			"raw_response": _safe_json(response),
		}
	)
	subscription.save(ignore_permissions=True)

	if not subscription.init_point:
		frappe.throw(_("Mercado Pago did not return a checkout URL."))

	return subscription.init_point


@frappe.whitelist()
def create_paypal_plus_subscription(currency: str = "USD") -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)
	if has_active_plus():
		return {"active": True, "redirect_url": f"{get_lms_path_url()}/plus?status=active"}

	from lms.lms.paypal import create_pending_plus_subscription

	return create_pending_plus_subscription(currency=currency)


@frappe.whitelist()
def sync_paypal_plus_subscription(subscription_id: str, subscription: str | None = None) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)
	if not subscription_id:
		frappe.throw(_("PayPal did not return a subscription ID."))

	from lms.lms.paypal import fetch_subscription, sync_plus_subscription

	doc = sync_plus_subscription(fetch_subscription(subscription_id), local_subscription=subscription)
	if doc and doc.member != frappe.session.user:
		frappe.throw(_("You cannot activate this subscription."), frappe.PermissionError)
	return get_plus_billing()


def get_lms_path_url(settings=None) -> str:
	settings = settings or _get_settings()
	return f"{_get_public_base_url(settings)}/{get_lms_path()}"


def _get_support_email() -> str:
	try:
		meta = frappe.get_meta("Website Settings")
		for fieldname in ("contact_email", "email"):
			if not meta.has_field(fieldname):
				continue
			value = frappe.db.get_single_value("Website Settings", fieldname)
			if value:
				return value
	except Exception:
		pass
	return frappe.conf.get("admin_email") or "soporte@studybadge.com"


def _serialize_subscription(subscription) -> dict | None:
	if not subscription:
		return None

	return {
		"name": subscription.name,
		"status": subscription.status,
		"payment_gateway": getattr(subscription, "payment_gateway", None) or "Mercado Pago",
		"init_point": subscription.init_point,
		"next_payment_date": subscription.next_payment_date,
		"last_synced_at": subscription.last_synced_at,
		"cancel_at_period_end": cint(getattr(subscription, "cancel_at_period_end", 0)),
		"cancel_requested_at": getattr(subscription, "cancel_requested_at", None),
		"cancel_scheduled_for": getattr(subscription, "cancel_scheduled_for", None),
		"payment_method": {
			"id": getattr(subscription, "payment_method_id", None),
			"name": getattr(subscription, "payment_method_name", None),
			"card_last_four": getattr(subscription, "card_last_four", None),
			"card_brand": getattr(subscription, "card_brand", None),
		},
		"paypal": {
			"subscription_id": getattr(subscription, "paypal_subscription_id", None),
			"plan_id": getattr(subscription, "paypal_plan_id", None),
		},
		"paddle": {
			"customer_id": getattr(subscription, "paddle_customer_id", None),
			"subscription_id": getattr(subscription, "paddle_subscription_id", None),
			"price_id": getattr(subscription, "paddle_price_id", None),
			"transaction_id": getattr(subscription, "paddle_transaction_id", None),
		},
	}


def _get_receipt_filters(subscription) -> dict:
	return {
		"member": subscription.member,
		"subscription": subscription.name,
	}


def _serialize_receipts(subscription) -> list[dict]:
	if not subscription:
		return []

	receipts = frappe.get_all(
		"StudyBadge Plus Receipt",
		_get_receipt_filters(subscription),
		[
			"name",
			"receipt_number",
			"status",
			"status_detail",
			"payment_gateway",
			"mp_authorized_payment_id",
			"mp_payment_id",
			"paypal_capture_id",
			"paypal_subscription_id",
			"paddle_transaction_id",
			"paddle_subscription_id",
			"paddle_customer_id",
			"amount",
			"currency",
			"paid_at",
			"date_created",
		],
		order_by="paid_at desc, creation desc",
		limit=24,
	)
	for receipt in receipts:
		receipt["download_url"] = (
			"/api/method/lms.lms.subscriptions.download_plus_receipt"
			f"?receipt={quote(str(receipt.name))}"
		)
	return receipts


def _sync_receipt(payment: dict, subscription):
	authorized_payment_id = str(payment.get("id")) if payment.get("id") else None
	payment_id = _get_payment_id(payment)
	filters = None
	if authorized_payment_id:
		filters = {"mp_authorized_payment_id": authorized_payment_id}
	elif payment_id:
		filters = {"mp_payment_id": payment_id, "subscription": subscription.name}

	receipt_name = frappe.db.exists("StudyBadge Plus Receipt", filters) if filters else None
	if receipt_name:
		receipt = frappe.get_doc("StudyBadge Plus Receipt", receipt_name)
	else:
		receipt = frappe.new_doc("StudyBadge Plus Receipt")
		receipt.member = subscription.member
		receipt.subscription = subscription.name

	receipt.update(
		{
			"receipt_number": receipt.receipt_number or _receipt_number(payment),
			"status": _get_payment_status(payment),
			"status_detail": _get_payment_status_detail(payment),
			"payment_gateway": "Mercado Pago",
			"mp_authorized_payment_id": authorized_payment_id,
			"mp_payment_id": payment_id,
			"mp_preapproval_id": payment.get("preapproval_id") or subscription.mp_preapproval_id,
			"amount": payment.get("transaction_amount"),
			"currency": payment.get("currency_id") or subscription.currency,
			"paid_at": _parse_mp_datetime(payment.get("debit_date") or payment.get("date_created")),
			"date_created": _parse_mp_datetime(payment.get("date_created")),
			"last_modified": _parse_mp_datetime(payment.get("last_modified")),
			"raw_response": _safe_json(payment),
		}
	)
	receipt.save(ignore_permissions=True)
	return receipt


def _search_authorized_payments(params: dict, settings=None) -> list[dict]:
	payload = _request(
		"GET",
		"/authorized_payments/search",
		settings=settings,
		params={key: value for key, value in params.items() if value},
	)
	return payload.get("results") or []


def _sync_subscription_receipts(subscription, settings=None, raise_errors=False) -> list:
	if not subscription or not subscription.mp_preapproval_id:
		return []

	try:
		payments = _search_authorized_payments(
			{"preapproval_id": subscription.mp_preapproval_id, "limit": 20},
			settings=settings,
		)
	except Exception:
		if raise_errors:
			raise
		frappe.log_error(frappe.get_traceback(), "StudyBadge Plus Receipt Sync Failed")
		return []

	receipts = [_sync_receipt(payment, subscription) for payment in payments]
	subscription.last_invoice_sync_at = now_datetime()
	subscription.save(ignore_permissions=True)
	return receipts


def _sync_authorized_payment_event(data_id: str | None, settings=None):
	if not data_id:
		return None, None

	payments = []
	for params in ({"id": data_id}, {"payment_id": data_id}):
		try:
			payments = _search_authorized_payments(params, settings=settings)
		except Exception:
			frappe.log_error(
				frappe.get_traceback(),
				"StudyBadge Plus Authorized Payment Lookup Failed",
			)
			continue
		if payments:
			break
	if not payments:
		return None, None

	payment = payments[0]
	preapproval_id = payment.get("preapproval_id")
	subscription = None
	subscription_name = preapproval_id and frappe.db.exists(
		"StudyBadge Plus Subscription", {"mp_preapproval_id": preapproval_id}
	)
	if subscription_name:
		subscription = frappe.get_doc("StudyBadge Plus Subscription", subscription_name)
	if not subscription:
		return None, None

	return subscription, _sync_receipt(payment, subscription)


def _is_authorized_payment_topic(topic: str | None, payload: dict) -> bool:
	resource = _get_resource(payload) or ""
	topic = topic or ""
	return "authorized_payment" in topic or "authorized_payments" in str(resource)


def _is_payment_topic(topic: str | None, payload: dict) -> bool:
	resource = _get_resource(payload) or ""
	topic = topic or ""
	return topic == "payment" or topic.startswith("payment.") or "/v1/payments/" in str(resource)


def _sync_certificate_payment_event(data_id: str | None, settings=None):
	if not data_id:
		return None

	from lms.lms.payments import _mp_request, process_mercadopago_certificate_payment

	mp_payment = _mp_request("GET", f"/v1/payments/{data_id}", settings=settings)
	return process_mercadopago_certificate_payment(mp_payment)


@frappe.whitelist()
def get_plus_billing() -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to view your Plus billing."), frappe.AuthenticationError)

	settings = _get_settings()
	subscription = _get_latest_subscription(frappe.session.user)
	if subscription:
		if getattr(subscription, "mp_preapproval_id", None):
			subscription = _refresh_subscription_from_mercadopago(subscription, settings=settings)
			_sync_subscription_receipts(subscription, settings=settings)
		elif getattr(subscription, "paddle_subscription_id", None):
			try:
				from lms.lms.paddle import fetch_subscription, sync_paddle_subscription

				subscription = sync_paddle_subscription(
					fetch_subscription(subscription.paddle_subscription_id, settings=settings)
				) or subscription
			except Exception:
				frappe.log_error(frappe.get_traceback(), "StudyBadge Plus Paddle Refresh Failed")

	preferred_currency = get_preferred_payment_currency()
	return {
		"active": has_active_plus(),
		"plan": _get_plus_plan_for_currency(preferred_currency, settings),
		"plans": {
			"PEN": _get_plus_plan_for_currency("PEN", settings),
			"USD": _get_plus_plan_for_currency("USD", settings),
		},
		"preferred_payment_currency": preferred_currency,
		"public_key": settings.public_key,
		"paypal": {
			"enabled": bool(getattr(settings, "paypal_enabled", 0)),
			"mode": getattr(settings, "paypal_mode", None) or "sandbox",
			"client_id": getattr(settings, "paypal_client_id", None),
			"plan_id_usd": getattr(settings, "paypal_plus_plan_id_usd", None),
		},
		"paddle": {
			"enabled": bool(getattr(settings, "paddle_enabled", 0)),
			"mode": getattr(settings, "paddle_mode", None) or "sandbox",
			"price_id": getattr(settings, "paddle_plus_price_id", None),
		},
		"support_email": _get_support_email(),
		"subscription": _serialize_subscription(subscription),
		"receipts": _serialize_receipts(subscription),
	}


def _get_manageable_subscription():
	subscription = _get_latest_subscription(frappe.session.user)
	if not subscription:
		frappe.throw(_("You do not have a StudyBadge Plus subscription yet."))
	if subscription.status not in PLUS_ACTIVE_STATUSES:
		frappe.throw(_("Your StudyBadge Plus subscription is not active."))
	if not subscription.mp_preapproval_id and not getattr(subscription, "paypal_subscription_id", None) and not getattr(subscription, "paddle_subscription_id", None):
		frappe.throw(_("This subscription is missing its payment gateway ID."))
	return subscription


@frappe.whitelist()
def request_plus_cancellation() -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to manage your Plus subscription."), frappe.AuthenticationError)

	subscription = _get_manageable_subscription()
	if getattr(subscription, "payment_gateway", None) == "PayPal":
		from lms.lms.paypal import cancel_subscription

		cancel_subscription(subscription.paypal_subscription_id)
		subscription.status = "cancelled"
		subscription.cancel_at_period_end = 0
		subscription.cancel_requested_at = now_datetime()
		subscription.save(ignore_permissions=True)
		frappe.db.commit()
		return get_plus_billing()

	if getattr(subscription, "payment_gateway", None) == "Paddle":
		from lms.lms.paddle import cancel_subscription

		cancel_subscription(subscription.paddle_subscription_id)
		frappe.db.commit()
		return get_plus_billing()

	if not subscription.next_payment_date:
		frappe.throw(_("We could not find your next billing date. Please contact support."))

	subscription.cancel_at_period_end = 1
	subscription.cancel_requested_at = now_datetime()
	subscription.cancel_scheduled_for = subscription.next_payment_date
	subscription.save(ignore_permissions=True)
	frappe.db.commit()
	return get_plus_billing()


@frappe.whitelist()
def reactivate_plus_subscription() -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to manage your Plus subscription."), frappe.AuthenticationError)

	subscription = _get_manageable_subscription()
	if getattr(subscription, "payment_gateway", None) == "Paddle":
		if not subscription.cancel_at_period_end:
			frappe.throw(_("This Paddle subscription is not scheduled to cancel."))
		from lms.lms.paddle import reactivate_subscription

		reactivate_subscription(subscription.paddle_subscription_id)
		frappe.db.commit()
		return get_plus_billing()
	subscription.cancel_at_period_end = 0
	subscription.cancel_requested_at = None
	subscription.cancel_scheduled_for = None
	subscription.save(ignore_permissions=True)
	frappe.db.commit()
	return get_plus_billing()


@frappe.whitelist()
def update_plus_payment_method(card_token_id: str) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to manage your Plus subscription."), frappe.AuthenticationError)
	if not card_token_id:
		frappe.throw(_("Mercado Pago did not return a card token."))

	settings = _get_settings()
	subscription = _get_manageable_subscription()
	response = _request(
		"PUT",
		f"/preapproval/{subscription.mp_preapproval_id}",
		settings=settings,
		data=json.dumps({"card_token_id": card_token_id}),
	)
	_sync_subscription(response)
	return get_plus_billing()


def _cancel_subscription_now(subscription, settings=None):
	settings = settings or _get_settings()
	response = _request(
		"PUT",
		f"/preapproval/{subscription.mp_preapproval_id}",
		settings=settings,
		data=json.dumps({"status": "canceled"}),
	)
	return _sync_subscription(response)


def process_plus_cancellations():
	try:
		settings = _get_settings()
	except Exception:
		return
	due = frappe.get_all(
		"StudyBadge Plus Subscription",
		{
			"cancel_at_period_end": 1,
			"status": ["in", list(PLUS_ACTIVE_STATUSES)],
			"cancel_scheduled_for": ["<=", now_datetime()],
		},
		["name"],
	)
	for row in due:
		try:
			subscription = frappe.get_doc("StudyBadge Plus Subscription", row.name)
			if getattr(subscription, "payment_gateway", None) == "Paddle":
				continue
			_cancel_subscription_now(subscription, settings=settings)
			frappe.db.commit()
		except Exception:
			frappe.log_error(
				frappe.get_traceback(),
				f"StudyBadge Plus Cancellation Failed: {row.name}",
			)


def _render_receipt_html(receipt, subscription) -> str:
	member_name = frappe.db.get_value("User", receipt.member, "full_name") or receipt.member
	brand_name = frappe.db.get_single_value("Website Settings", "app_name") or "StudyBadge"
	paid_at = format_datetime(receipt.paid_at or receipt.date_created) if (
		receipt.paid_at or receipt.date_created
	) else ""
	next_payment = (
		format_datetime(subscription.next_payment_date) if subscription.next_payment_date else ""
	)
	amount = f"{receipt.currency or subscription.currency or 'PEN'} {flt(receipt.amount):.2f}"
	return frappe.render_template(
		"""
		<meta name="pdfkit-page-size" content="A4">
		<meta name="pdfkit-margin-top" content="12mm">
		<meta name="pdfkit-margin-bottom" content="12mm">
		<meta name="pdfkit-margin-left" content="12mm">
		<meta name="pdfkit-margin-right" content="12mm">
		<style>
			body { font-family: Inter, Arial, sans-serif; color: #111827; }
			.receipt { border: 1px solid #d1d5db; border-radius: 12px; overflow: hidden; }
			.header { background: #0f172a; color: white; padding: 28px; }
			.brand { font-size: 24px; font-weight: 800; }
			.badge { display: inline-block; margin-top: 10px; padding: 6px 10px; border-radius: 999px; background: #f59e0b; color: #111827; font-weight: 700; }
			.content { padding: 28px; }
			.grid { width: 100%; border-collapse: collapse; margin-top: 24px; }
			.grid td { padding: 12px; border-bottom: 1px solid #e5e7eb; }
			.label { color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }
			.value { font-size: 15px; font-weight: 650; }
			.total { margin-top: 24px; padding: 18px; border-radius: 10px; background: #f8fafc; text-align: right; }
			.total .amount { font-size: 30px; font-weight: 800; color: #0f172a; }
			.footer { padding: 20px 28px; background: #f9fafb; color: #6b7280; font-size: 12px; }
		</style>
		<div class="receipt">
			<div class="header">
				<div class="brand">{{ brand_name }}</div>
				<div class="badge">StudyBadge Plus</div>
			</div>
			<div class="content">
				<h1>Recibo de pago</h1>
				<p>Gracias por ser parte de StudyBadge Plus. Este recibo confirma el pago registrado por Mercado Pago.</p>
				<table class="grid">
					<tr><td><div class="label">Recibo</div><div class="value">{{ receipt.receipt_number }}</div></td><td><div class="label">Fecha de pago</div><div class="value">{{ paid_at }}</div></td></tr>
					<tr><td><div class="label">Miembro</div><div class="value">{{ member_name }}</div></td><td><div class="label">Estado</div><div class="value">{{ receipt.status or "" }}</div></td></tr>
					<tr><td><div class="label">Pago Mercado Pago</div><div class="value">{{ receipt.mp_payment_id or receipt.mp_authorized_payment_id }}</div></td><td><div class="label">Próxima facturación</div><div class="value">{{ next_payment }}</div></td></tr>
				</table>
				<div class="total">
					<div class="label">Total pagado</div>
					<div class="amount">{{ amount }}</div>
				</div>
			</div>
			<div class="footer">
				Este documento es un recibo comercial de StudyBadge basado en la información del pago procesado por Mercado Pago. No reemplaza una factura tributaria.
			</div>
		</div>
		""",
		{
			"receipt": receipt,
			"subscription": subscription,
			"brand_name": brand_name,
			"member_name": member_name,
			"paid_at": paid_at,
			"next_payment": next_payment,
			"amount": amount,
		},
	)


@frappe.whitelist()
def download_plus_receipt(receipt: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to download receipts."), frappe.AuthenticationError)

	doc = frappe.get_doc("StudyBadge Plus Receipt", receipt)
	if doc.member != frappe.session.user:
		frappe.throw(_("You cannot download this receipt."), frappe.PermissionError)

	subscription = frappe.get_doc("StudyBadge Plus Subscription", doc.subscription)
	from frappe.utils.pdf import get_pdf

	pdf = get_pdf(_render_receipt_html(doc, subscription))
	frappe.local.response.filename = f"{doc.receipt_number or doc.name}.pdf"
	frappe.local.response.filecontent = pdf
	frappe.local.response.type = "download"
	frappe.local.response.content_type = "application/pdf"


def _get_request_json() -> dict:
	try:
		return frappe.request.get_json(silent=True) or {}
	except Exception:
		try:
			return json.loads(frappe.request.get_data(as_text=True) or "{}")
		except Exception:
			return {}


def _get_data_id(payload: dict) -> str | None:
	data_id = (
		frappe.request.args.get("data.id")
		or frappe.request.args.get("id")
		or frappe.form_dict.get("data.id")
		or frappe.form_dict.get("id")
	)
	if data_id:
		return str(data_id)

	data = payload.get("data")
	if isinstance(data, dict) and data.get("id"):
		return str(data.get("id"))

	resource = payload.get("resource") or frappe.form_dict.get("resource")
	if resource and "/" in str(resource):
		return str(resource).rstrip("/").split("/")[-1]

	return None


def _get_topic(payload: dict) -> str | None:
	return (
		frappe.request.args.get("topic")
		or frappe.request.args.get("type")
		or frappe.form_dict.get("topic")
		or frappe.form_dict.get("type")
		or payload.get("topic")
		or payload.get("type")
	)


def _get_resource(payload: dict) -> str | None:
	return frappe.form_dict.get("resource") or payload.get("resource")


def _parse_signature(signature_header: str) -> dict:
	parts = {}
	for part in (signature_header or "").split(","):
		if "=" not in part:
			continue
		key, value = part.split("=", 1)
		parts[key.strip()] = value.strip()
	return parts


def _verify_webhook_signature(data_id: str | None, settings=None):
	x_signature = frappe.request.headers.get("x-signature")
	x_request_id = frappe.request.headers.get("x-request-id")
	signature_parts = _parse_signature(x_signature)
	timestamp = signature_parts.get("ts")
	signature = signature_parts.get("v1")
	if not (x_signature and x_request_id and timestamp and signature):
		frappe.throw(_("Invalid Mercado Pago webhook signature."), frappe.PermissionError)

	manifest = ""
	if data_id:
		manifest += f"id:{data_id.lower()};"
	manifest += f"request-id:{x_request_id};ts:{timestamp};"
	manifests = [manifest]
	if data_id:
		manifests.append(f"request-id:{x_request_id};ts:{timestamp};")

	secret = _get_webhook_secret(settings).encode()
	valid = any(
		hmac.compare_digest(
			hmac.new(secret, msg=candidate.encode(), digestmod=hashlib.sha256).hexdigest(),
			signature,
		)
		for candidate in manifests
	)
	if not valid:
		frappe.throw(_("Invalid Mercado Pago webhook signature."), frappe.PermissionError)


def _existing_processed_event(x_request_id: str | None, data_id: str | None, topic: str | None):
	if not (x_request_id or data_id):
		return None

	filters = {}
	if x_request_id:
		filters["x_request_id"] = x_request_id
	if data_id:
		filters["data_id"] = data_id
	if topic:
		filters["topic"] = topic

	name = frappe.db.exists("StudyBadge MercadoPago Event", filters)
	if name:
		return frappe.get_doc("StudyBadge MercadoPago Event", name)


def _record_event(payload: dict, data_id: str | None, topic: str | None):
	x_request_id = frappe.request.headers.get("x-request-id")
	existing = _existing_processed_event(x_request_id, data_id, topic)
	if existing:
		return existing, bool(existing.processed)

	event = frappe.new_doc("StudyBadge MercadoPago Event")
	event.update(
		{
			"x_request_id": x_request_id,
			"data_id": data_id,
			"topic": topic,
			"event_type": payload.get("action") or payload.get("type"),
			"resource": _get_resource(payload),
			"payload": _safe_json(payload or dict(frappe.form_dict)),
		}
	)
	event.save(ignore_permissions=True)
	return event, False


def _get_mp_subscription_id(payload: dict, data_id: str | None, topic: str | None) -> str | None:
	resource = _get_resource(payload)
	if resource and "/preapproval/" in str(resource):
		return str(resource).rstrip("/").split("/")[-1]

	if topic in {"subscription_preapproval", "preapproval"}:
		return data_id

	if data_id and frappe.db.exists("StudyBadge Plus Subscription", {"mp_preapproval_id": data_id}):
		return data_id

	return data_id


def _fetch_mp_subscription(preapproval_id: str, settings=None) -> dict:
	return _request("GET", f"/preapproval/{preapproval_id}", settings=settings)


@frappe.whitelist(allow_guest=True)
def mercadopago_webhook():
	settings = _get_settings()
	payload = _get_request_json()
	data_id = _get_data_id(payload)
	topic = _get_topic(payload)
	_verify_webhook_signature(data_id, settings)

	event, already_processed = _record_event(payload, data_id, topic)
	if already_processed:
		return {"status": "ok", "duplicate": True}

	if _is_authorized_payment_topic(topic, payload):
		subscription, receipt = _sync_authorized_payment_event(data_id, settings=settings)
		if subscription:
			event.subscription = subscription.name
		event.processed = 1
		event.save(ignore_permissions=True)
		return {"status": "ok", "receipt": receipt.name if receipt else None}

	if _is_payment_topic(topic, payload):
		payment = _sync_certificate_payment_event(data_id, settings=settings)
		event.processed = 1
		event.save(ignore_permissions=True)
		return {"status": "ok", "payment": payment.name if payment else None}

	preapproval_id = _get_mp_subscription_id(payload, data_id, topic)
	if not preapproval_id:
		frappe.throw(_("Mercado Pago webhook did not include a subscription ID."))

	mp_subscription = _fetch_mp_subscription(preapproval_id, settings=settings)
	subscription = _sync_subscription(mp_subscription)
	if subscription:
		_sync_subscription_receipts(subscription, settings=settings)
		event.subscription = subscription.name
	event.processed = 1
	event.save(ignore_permissions=True)

	return {"status": "ok"}
