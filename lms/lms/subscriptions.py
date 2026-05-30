import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone

import frappe
import requests
from frappe import _
from frappe.utils import flt, now_datetime

from lms.lms.utils import get_lms_path

MERCADOPAGO_API_BASE = "https://api.mercadopago.com"
PLUS_ACTIVE_STATUSES = {"authorized", "active"}
KNOWN_SUBSCRIPTION_STATUSES = {
	"pending",
	"authorized",
	"active",
	"paused",
	"cancelled",
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
	return {
		"enabled": bool(settings.enabled),
		"plan_name": settings.plan_name,
		"amount": flt(settings.amount),
		"currency": settings.currency,
		"frequency": settings.frequency or 1,
		"frequency_type": settings.frequency_type or "months",
	}


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

	doc.update(
		{
			"status": _normalize_status(mp_subscription.get("status")),
			"mp_preapproval_id": mp_subscription.get("id"),
			"external_reference": mp_subscription.get("external_reference"),
			"init_point": mp_subscription.get("init_point"),
			"amount": auto_recurring.get("transaction_amount"),
			"currency": auto_recurring.get("currency_id"),
			"next_payment_date": _parse_mp_datetime(mp_subscription.get("next_payment_date")),
			"date_created": _parse_mp_datetime(mp_subscription.get("date_created")),
			"last_modified": _parse_mp_datetime(mp_subscription.get("last_modified")),
			"last_synced_at": now_datetime(),
			"raw_response": _safe_json(mp_subscription),
		}
	)
	doc.save(ignore_permissions=True)
	return doc


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

	plan = _get_plus_plan()
	subscription = _get_latest_subscription(frappe.session.user)
	data = {
		"active": has_active_plus(),
		"plan": plan,
		"subscription": None,
	}

	if subscription:
		data["subscription"] = {
			"name": subscription.name,
			"status": subscription.status,
			"init_point": subscription.init_point,
			"next_payment_date": subscription.next_payment_date,
			"last_synced_at": subscription.last_synced_at,
		}

	return data


@frappe.whitelist()
def create_plus_checkout() -> str:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to activate StudyBadge Plus."), frappe.AuthenticationError)

	settings = _get_settings()
	if has_active_plus():
		return f"{get_lms_path_url(settings)}/plus?status=active"

	pending = _get_pending_subscription(frappe.session.user)
	if pending and pending.init_point:
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
			"transaction_amount": flt(settings.amount),
			"currency_id": settings.currency,
		},
		"status": "pending",
	}

	response = _request("POST", "/preapproval", settings=settings, data=json.dumps(payload))
	subscription = frappe.new_doc("StudyBadge Plus Subscription")
	subscription.update(
		{
			"member": frappe.session.user,
			"status": _normalize_status(response.get("status")),
			"mp_preapproval_id": response.get("id"),
			"external_reference": response.get("external_reference") or external_reference,
			"init_point": response.get("init_point"),
			"amount": flt(settings.amount),
			"currency": settings.currency,
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


def get_lms_path_url(settings=None) -> str:
	settings = settings or _get_settings()
	return f"{_get_public_base_url(settings)}/{get_lms_path()}"


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

	preapproval_id = _get_mp_subscription_id(payload, data_id, topic)
	if not preapproval_id:
		frappe.throw(_("Mercado Pago webhook did not include a subscription ID."))

	mp_subscription = _fetch_mp_subscription(preapproval_id, settings=settings)
	subscription = _sync_subscription(mp_subscription)
	if subscription:
		event.subscription = subscription.name
	event.processed = 1
	event.save(ignore_permissions=True)

	return {"status": "ok"}
