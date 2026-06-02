import hashlib
import json
import uuid

import frappe
import requests
from frappe import _
from frappe.utils import flt

from lms.lms.utils import (
	adjust_amount_for_coupon,
	complete_enrollment,
	get_gst_details,
	get_lms_route,
	get_order_summary,
	set_checkout_currency,
)
from lms.lms.subscriptions import (
	MERCADOPAGO_API_BASE,
	_get_access_token,
	_get_public_base_url,
	_get_settings,
)


def get_payment_gateway():
	return frappe.db.get_single_value("LMS Settings", "payment_gateway")


def _mp_headers(settings=None, idempotency_key: str | None = None) -> dict:
	headers = {
		"Authorization": f"Bearer {_get_access_token(settings)}",
		"Content-Type": "application/json",
	}
	if idempotency_key:
		headers["X-Idempotency-Key"] = idempotency_key
	return headers


def _mp_request(method: str, path: str, settings=None, idempotency_key: str | None = None, **kwargs) -> dict:
	response = requests.request(
		method,
		f"{MERCADOPAGO_API_BASE}{path}",
		headers=_mp_headers(settings, idempotency_key=idempotency_key),
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
			"StudyBadge Certificate Mercado Pago Error",
		)
		frappe.throw(_("Mercado Pago could not process this certificate payment. Please try again."))

	return payload


def _safe_json(data: dict | list | None) -> str:
	return json.dumps(data or {}, indent=2, sort_keys=True, default=str)


def _certificate_redirect(course: str) -> str:
	return get_lms_route(f"courses/{course}/certification")


def _validate_certificate_payment_access(course: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to continue with payment."), frappe.AuthenticationError)

	from lms.lms.api import verify_billing_access

	access, message = verify_billing_access("LMS Course", course, "certificate")
	if not access:
		frappe.throw(message)

	enrollment = frappe.db.get_value(
		"LMS Enrollment",
		{"member": frappe.session.user, "course": course},
		["name", "purchased_certificate"],
		as_dict=True,
	)
	if not enrollment:
		frappe.throw(_("You must be enrolled in this course before buying the certificate."))

	paid_certificate = frappe.db.get_value("LMS Course", course, "paid_certificate")
	if not paid_certificate:
		frappe.throw(_("This course does not require a paid certificate checkout."))

	return enrollment


def _get_certificate_payment_total(course: str, coupon_code: str | None = None, country: str | None = None):
	details = frappe.db.get_value(
		"LMS Course",
		course,
		["title", "name", "paid_certificate", "course_price as amount", "currency", "amount_usd"],
		as_dict=True,
	)
	if not details or not details.paid_certificate:
		frappe.throw(_("This course does not require a paid certificate checkout."))

	details = frappe._dict(details)
	set_checkout_currency(details, "PEN")
	details.original_amount = details.amount
	adjust_amount_for_coupon(details, coupon_code, "LMS Course", course)
	get_gst_details(details, country)
	details.total_amount = details.amount
	return details


def _make_certificate_external_reference(payment_name: str) -> str:
	return f"studybadge-certificate::{payment_name}"


def _notification_url(settings=None) -> str:
	settings = settings or _get_settings()
	return (
		f"{_get_public_base_url(settings)}/api/method/"
		"lms.lms.subscriptions.mercadopago_webhook?source_news=webhooks"
	)


def _create_mp_preference(payment_doc, details, settings=None) -> dict:
	settings = settings or _get_settings()
	base_url = _get_public_base_url(settings)
	redirect_url = f"{base_url}{get_redirect_url(payment_doc.payment_for_document_type, payment_doc.payment_for_document, payment_doc.payment_for_certificate)}"
	
	if payment_doc.payment_for_certificate:
		title = _("Certificate for {0}").format(details.title)
		description = _("StudyBadge course certificate")
		failure_url = f"{base_url}{get_lms_route(f'billing/certificate/{payment_doc.payment_for_document}')}"
	else:
		title = _("Payment for {0}").format(details.title)
		description = _("StudyBadge course enrollment")
		doctype_slug = "course" if payment_doc.payment_for_document_type == "LMS Course" else "batch"
		failure_url = f"{base_url}{get_lms_route(f'billing/{doctype_slug}/{payment_doc.payment_for_document}')}"

	payload = {
		"items": [
			{
				"id": payment_doc.payment_for_document,
				"title": title,
				"description": description,
				"quantity": 1,
				"unit_price": flt(details.total_amount),
				"currency_id": details.currency,
			}
		],
		"payer": {"email": payment_doc.member, "name": payment_doc.billing_name},
		"external_reference": payment_doc.external_reference,
		"notification_url": _notification_url(settings),
		"back_urls": {
			"success": redirect_url,
			"pending": redirect_url,
			"failure": failure_url,
		},
		"metadata": {
			"lms_payment": payment_doc.name,
			"course": payment_doc.payment_for_document,
			"member": payment_doc.member,
			"payment_for": "certificate" if payment_doc.payment_for_certificate else "course",
		},
	}
	return _mp_request("POST", "/checkout/preferences", settings=settings, data=json.dumps(payload))


@frappe.whitelist()
def create_mp_brick_checkout(
	doctype: str,
	docname: str,
	address: dict,
	payment_for_certificate: int = 0,
	coupon_code: str | None = None,
	country: str | None = None,
):
	_validate_paypal_payment_access(doctype, docname, payment_for_certificate)
	settings = _get_settings()
	if not settings.public_key:
		frappe.throw(_("Mercado Pago public key is missing in StudyBadge Plus Settings."))

	address = frappe._dict(address)
	
	if int(payment_for_certificate):
		details = _get_certificate_payment_total(docname, coupon_code=coupon_code, country=country)
		if details.currency != "PEN":
			frappe.throw(_("Certificate payments through Mercado Pago must be configured in PEN."))
		amount = details.original_amount - details.get("discount_amount", 0)
		total_amount = amount + details.get("gst_applied", 0)
	else:
		details = frappe._dict(get_order_summary(doctype, docname, coupon=coupon_code, country=country, currency="PEN"))
		if details.currency != "PEN":
			frappe.throw(_("Mercado Pago payments must be configured in PEN."))
		amount = details.original_amount - details.get("discount_amount", 0)
		total_amount = details.amount

	payment = record_payment(
		address,
		doctype,
		docname,
		amount,
		details.original_amount,
		details.currency,
		total_amount if details.get("gst_applied") else 0,
		details.get("discount_amount", 0),
		payment_for_certificate,
		coupon_code,
		details.get("coupon"),
	)
	payment.external_reference = _make_payment_external_reference(
		payment.name,
		_payment_for_label(payment_for_certificate, doctype),
	)
	payment.payment_gateway = "Mercado Pago"
	payment.payment_status = "pending"
	payment.save(ignore_permissions=True)

	redirect_to = get_redirect_url(doctype, docname, payment_for_certificate)

	if flt(details.total_amount) <= 0:
		frappe.db.set_value("LMS Payment", payment.name, "payment_received", 1)
		complete_enrollment(payment.name, doctype, docname)
		return {
			"status": "approved",
			"redirect_url": redirect_to,
			"payment": payment.name,
		}

	preference = _create_mp_preference(payment, details, settings=settings)
	frappe.db.set_value(
		"LMS Payment",
		payment.name,
		{
			"order_id": preference.get("id"),
			"raw_response": _safe_json({"preference": preference}),
		},
	)

	return {
		"payment": payment.name,
		"preference_id": preference.get("id"),
		"public_key": settings.public_key,
		"amount": flt(details.total_amount),
		"currency": details.currency,
		"title": details.title,
		"status": "pending",
		"redirect_url": redirect_to,
	}


def _coerce_form_data(form_data):
	if isinstance(form_data, str):
		return json.loads(form_data or "{}")
	return form_data or {}


def _get_payment_by_external_reference(external_reference: str | None):
	if not external_reference:
		return None
	payment_name = frappe.db.exists("LMS Payment", {"external_reference": external_reference})
	return frappe.get_doc("LMS Payment", payment_name) if payment_name else None


def _get_payment_from_mp_payload(mp_payment: dict):
	payment_name = (mp_payment.get("metadata") or {}).get("lms_payment")
	if payment_name and frappe.db.exists("LMS Payment", payment_name):
		return frappe.get_doc("LMS Payment", payment_name)
	return _get_payment_by_external_reference(mp_payment.get("external_reference"))


def _update_lms_payment_from_mp(payment_doc, mp_payment: dict):
	status = mp_payment.get("status")
	payment_doc.update(
		{
			"payment_gateway": "Mercado Pago",
			"payment_status": status,
			"payment_status_detail": mp_payment.get("status_detail"),
			"payment_id": str(mp_payment.get("id")) if mp_payment.get("id") else payment_doc.payment_id,
			"raw_response": _safe_json(mp_payment),
		}
	)
	if status == "approved":
		payment_doc.payment_received = 1
	payment_doc.save(ignore_permissions=True)
	return payment_doc


def _send_certificate_receipt_email(payment_doc, mp_payment: dict):
	course_title = frappe.db.get_value("LMS Course", payment_doc.payment_for_document, "title")
	member_name = frappe.db.get_value("User", payment_doc.member, "full_name") or payment_doc.member
	amount = payment_doc.amount_with_gst or payment_doc.amount
	payment_id = mp_payment.get("id") or payment_doc.payment_id or payment_doc.name
	try:
		frappe.sendmail(
			recipients=[payment_doc.member],
			subject=_("Recibo de pago de certificado StudyBadge"),
			message=frappe.render_template(
				"""
				<p>Hola {{ member_name }},</p>
				<p>Hemos confirmado tu pago del certificado del curso <strong>{{ course_title }}</strong>.</p>
				<table style="border-collapse:collapse;margin:16px 0;width:100%;max-width:560px">
					<tr>
						<td style="padding:10px;border:1px solid #e5e7eb;color:#6b7280">Recibo</td>
						<td style="padding:10px;border:1px solid #e5e7eb"><strong>{{ payment_name }}</strong></td>
					</tr>
					<tr>
						<td style="padding:10px;border:1px solid #e5e7eb;color:#6b7280">Pago Mercado Pago</td>
						<td style="padding:10px;border:1px solid #e5e7eb">{{ payment_id }}</td>
					</tr>
					<tr>
						<td style="padding:10px;border:1px solid #e5e7eb;color:#6b7280">Total pagado</td>
						<td style="padding:10px;border:1px solid #e5e7eb"><strong>S/ {{ amount }}</strong></td>
					</tr>
				</table>
				<p>Tu certificado ya esta desbloqueado. Puedes continuar desde StudyBadge para agendar o completar tu certificacion.</p>
				<p>Gracias por aprender con StudyBadge.</p>
				""",
				{
					"member_name": member_name,
					"course_title": course_title,
					"payment_name": payment_doc.name,
					"payment_id": payment_id,
					"amount": f"{flt(amount):.2f}",
				},
			),
			now=True,
		)
	except Exception:
		frappe.log_error(frappe.get_traceback(), f"StudyBadge Certificate Receipt Email Failed: {payment_doc.name}")


def process_mercadopago_payment(mp_payment: dict):
	payment_doc = _get_payment_from_mp_payload(mp_payment)
	if not payment_doc:
		frappe.log_error(_safe_json(mp_payment), "StudyBadge Mercado Pago Payment Not Found")
		return None

	already_received = bool(payment_doc.payment_received)
	payment_doc = _update_lms_payment_from_mp(payment_doc, mp_payment)
	if payment_doc.payment_received and not already_received:
		complete_enrollment(
			payment_doc.name,
			payment_doc.payment_for_document_type,
			payment_doc.payment_for_document,
		)
		if payment_doc.payment_for_certificate:
			from lms.lms.doctype.lms_certificate.lms_certificate import auto_issue_course_certificate
			auto_issue_course_certificate(payment_doc.payment_for_document, payment_doc.member)
			_send_certificate_receipt_email(payment_doc, mp_payment)
	return payment_doc


@frappe.whitelist()
def process_mp_brick_payment(payment: str, form_data: dict | str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to continue with payment."), frappe.AuthenticationError)

	payment_doc = frappe.get_doc("LMS Payment", payment)
	if payment_doc.member != frappe.session.user:
		frappe.throw(_("You cannot pay this checkout."), frappe.PermissionError)
		
	redirect_to = get_redirect_url(payment_doc.payment_for_document_type, payment_doc.payment_for_document, payment_doc.payment_for_certificate)
	if payment_doc.payment_received:
		return {"status": "approved", "redirect_url": redirect_to}

	data = _coerce_form_data(form_data)
	payer = data.get("payer") if isinstance(data.get("payer"), dict) else {}
	payer["email"] = payer.get("email") or frappe.session.user
	
	if payment_doc.payment_for_certificate:
		description = _("Certificate payment for {0}").format(frappe.db.get_value("LMS Course", payment_doc.payment_for_document, "title"))
	else:
		description = _("Payment for {0}").format(frappe.db.get_value(payment_doc.payment_for_document_type, payment_doc.payment_for_document, "title"))

	payload = {
		**data,
		"transaction_amount": flt(payment_doc.amount_with_gst or payment_doc.amount),
		"description": description,
		"external_reference": payment_doc.external_reference,
		"notification_url": _notification_url(),
		"payer": payer,
		"metadata": {
			**(data.get("metadata") or {}),
			"lms_payment": payment_doc.name,
			"course": payment_doc.payment_for_document,
			"member": payment_doc.member,
			"payment_for": "certificate" if payment_doc.payment_for_certificate else "course",
		},
	}
	payload = {key: value for key, value in payload.items() if value not in (None, "")}
	idempotency_source = data.get("token") or data.get("payment_method_id") or uuid.uuid4().hex
	idempotency_hash = hashlib.sha256(str(idempotency_source).encode()).hexdigest()[:24]
	idempotency_key = f"lms-mp-{payment_doc.name}-{idempotency_hash}"
	mp_payment = _mp_request(
		"POST",
		"/v1/payments",
		idempotency_key=idempotency_key,
		data=json.dumps(payload),
	)
	payment_doc = process_mercadopago_payment(mp_payment)
	return {
		"payment": payment_doc.name if payment_doc else payment,
		"status": mp_payment.get("status"),
		"status_detail": mp_payment.get("status_detail"),
		"payment_id": mp_payment.get("id"),
		"redirect_url": redirect_to,
	}


@frappe.whitelist()
def get_mp_payment_status(payment: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to view payment status."), frappe.AuthenticationError)

	payment_doc = frappe.get_doc("LMS Payment", payment)
	if payment_doc.member != frappe.session.user:
		frappe.throw(_("You cannot view this payment."), frappe.PermissionError)

	if payment_doc.payment_id:
		mp_payment = _mp_request("GET", f"/v1/payments/{payment_doc.payment_id}")
		payment_doc = process_mercadopago_payment(mp_payment) or payment_doc

	return {
		"payment": payment_doc.name,
		"status": payment_doc.payment_status or ("approved" if payment_doc.payment_received else "pending"),
		"status_detail": payment_doc.payment_status_detail,
		"payment_received": bool(payment_doc.payment_received),
		"redirect_url": get_redirect_url(payment_doc.payment_for_document_type, payment_doc.payment_for_document, payment_doc.payment_for_certificate),
	}


def get_controller(payment_gateway):
	if "payments" in frappe.get_installed_apps():
		from payments.utils import get_payment_gateway_controller

		return get_payment_gateway_controller(payment_gateway)


def validate_currency(payment_gateway, currency):
	controller = get_controller(payment_gateway)
	controller().validate_transaction_currency(currency)


@frappe.whitelist()
def get_payment_link(
	doctype: str,
	docname: str,
	address: dict,
	payment_for_certificate: int,
	coupon_code: str | None = None,
	country: str | None = None,
	currency: str | None = None,
):
	payment_gateway = get_payment_gateway()
	address = frappe._dict(address)
	redirect_to = get_redirect_url(doctype, docname, payment_for_certificate)

	if currency == "USD":
		return create_paypal_checkout(
			doctype,
			docname,
			address,
			payment_for_certificate,
			coupon_code=coupon_code,
			country=country,
		).get("approval_url")

	details = frappe._dict(get_order_summary(doctype, docname, coupon=coupon_code, country=country, currency=currency))
	title = details.title
	currency = details.currency
	original_amount = details.original_amount
	discount_amount = details.get("discount_amount", 0)
	gst_amount = details.get("gst_applied", 0)
	amount = original_amount - discount_amount
	amount_with_gst = get_amount_with_gst(amount, gst_amount)
	coupon = details.get("coupon")
	total_amount = amount_with_gst if amount_with_gst else amount

	payment = record_payment(
		address,
		doctype,
		docname,
		amount,
		original_amount,
		currency,
		amount_with_gst,
		discount_amount,
		payment_for_certificate,
		coupon_code,
		coupon,
	)

	if total_amount <= 0:
		frappe.db.set_value("LMS Payment", payment.name, "payment_received", 1)
		complete_enrollment(payment.name, doctype, docname)
		return redirect_to

	controller = get_controller(payment_gateway)

	payment_details = {
		"amount": total_amount,
		"title": f"Payment for {doctype} {title} {docname}",
		"description": f"{address.billing_name}'s payment for {title}",
		"reference_doctype": doctype,
		"reference_docname": docname,
		"payer_email": frappe.session.user,
		"payer_name": address.billing_name,
		"currency": currency,
		"payment_gateway": payment_gateway,
		"redirect_to": redirect_to,
		"payment": payment.name,
	}

	create_order(payment_gateway, payment_details, controller)
	url = controller.get_payment_url(**payment_details)

	return url


def _make_payment_external_reference(payment_name: str, payment_for: str) -> str:
	return f"studybadge-{payment_for}::{payment_name}"


def _payment_for_label(payment_for_certificate: int, doctype: str) -> str:
	if int(payment_for_certificate):
		return "certificate"
	return "course" if doctype == "LMS Course" else "batch"


def _validate_paypal_payment_access(doctype: str, docname: str, payment_for_certificate: int):
	if int(payment_for_certificate):
		return _validate_certificate_payment_access(docname)
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to continue with payment."), frappe.AuthenticationError)
	from lms.lms.api import verify_billing_access

	billing_type = "course" if doctype == "LMS Course" else "batch"
	access, message = verify_billing_access(doctype, docname, billing_type)
	if not access:
		frappe.throw(message)


@frappe.whitelist()
def create_paypal_checkout(
	doctype: str,
	docname: str,
	address: dict,
	payment_for_certificate: int = 0,
	coupon_code: str | None = None,
	country: str | None = None,
):
	_validate_paypal_payment_access(doctype, docname, payment_for_certificate)
	address = frappe._dict(address)
	redirect_to = get_redirect_url(doctype, docname, payment_for_certificate)
	cancel_to = get_lms_route(f"billing/{'certificate' if int(payment_for_certificate) else doctype.split(' ')[-1].lower()}/{docname}")
	details = frappe._dict(
		get_order_summary(doctype, docname, coupon=coupon_code, country=country, currency="USD")
	)

	amount = details.original_amount - details.get("discount_amount", 0)
	total_amount = details.amount
	payment = record_payment(
		address,
		doctype,
		docname,
		amount,
		details.original_amount,
		details.currency,
		total_amount if details.get("gst_applied") else 0,
		details.get("discount_amount", 0),
		payment_for_certificate,
		coupon_code,
		details.get("coupon"),
	)
	payment.payment_gateway = "PayPal"
	payment.payment_status = "CREATED"
	payment.external_reference = _make_payment_external_reference(
		payment.name,
		_payment_for_label(payment_for_certificate, doctype),
	)
	payment.save(ignore_permissions=True)

	if flt(details.total_amount) <= 0:
		frappe.db.set_value("LMS Payment", payment.name, "payment_received", 1)
		complete_enrollment(payment.name, doctype, docname)
		return {
			"status": "COMPLETED",
			"redirect_url": redirect_to,
			"payment": payment.name,
		}

	from lms.lms.paypal import create_order

	order = create_order(payment, details, redirect_to, cancel_to)
	return {
		**order,
		"payment": payment.name,
		"amount": flt(details.total_amount),
		"currency": "USD",
		"title": details.title,
		"status": "CREATED",
		"redirect_url": redirect_to,
	}


@frappe.whitelist()
def capture_paypal_checkout(payment: str, order_id: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to complete this payment."), frappe.AuthenticationError)

	payment_doc = frappe.get_doc("LMS Payment", payment)
	if payment_doc.member != frappe.session.user:
		frappe.throw(_("You cannot pay this checkout."), frappe.PermissionError)
	if payment_doc.order_id != order_id:
		frappe.throw(_("This PayPal order does not match the checkout."))
	if payment_doc.payment_received:
		return {
			"payment": payment_doc.name,
			"status": "COMPLETED",
			"redirect_url": get_redirect_url(
				payment_doc.payment_for_document_type,
				payment_doc.payment_for_document,
				payment_doc.payment_for_certificate,
			),
		}

	from lms.lms.paypal import capture_order, process_captured_order

	order = capture_order(order_id)
	payment_doc = process_captured_order(order, payment_doc) or payment_doc
	return {
		"payment": payment_doc.name,
		"status": payment_doc.payment_status,
		"payment_id": payment_doc.payment_id,
		"redirect_url": get_redirect_url(
			payment_doc.payment_for_document_type,
			payment_doc.payment_for_document,
			payment_doc.payment_for_certificate,
		),
	}


def create_order(payment_gateway: str, payment_details: dict, controller: object):
	if payment_gateway != "Razorpay":
		return

	order = controller.create_order(**payment_details)
	payment_details.update({"order_id": order.get("id")})


def get_amount_with_gst(amount: float, gst_amount: float) -> float:
	amount_with_gst = 0
	if gst_amount:
		amount_with_gst = amount + gst_amount

	return amount_with_gst


def record_payment(
	address: dict,
	doctype: str,
	docname: str,
	amount: float,
	original_amount: float,
	currency: str,
	amount_with_gst: float = 0,
	discount_amount: float = 0,
	payment_for_certificate: int = 0,
	coupon_code: str | None = None,
	coupon: str | None = None,
):
	address = frappe._dict(address)
	address_name = save_address(address)

	payment_doc = frappe.new_doc("LMS Payment")
	payment_doc.update(
		{
			"member": frappe.session.user,
			"billing_name": address.billing_name,
			"address": address_name,
			"amount": amount,
			"currency": currency,
			"discount_amount": discount_amount,
			"amount_with_gst": amount_with_gst,
			"gstin": address.gstin,
			"pan": address.pan,
			"source": address.source,
			"payment_for_document_type": doctype,
			"payment_for_document": docname,
			"payment_for_certificate": payment_for_certificate,
			"member_consent": address.member_consent,
		}
	)
	if coupon_code:
		payment_doc.update(
			{
				"coupon": coupon,
				"coupon_code": coupon_code,
				"discount_amount": discount_amount,
				"original_amount": original_amount,
			}
		)

	payment_doc.save(ignore_permissions=True)
	return payment_doc


def get_redirect_url(doctype: str, docname: str, payment_for_certificate: int) -> str:
	if int(payment_for_certificate):
		return get_lms_route(f"courses/{docname}/certification")
	elif doctype == "LMS Course":
		return get_lms_route(f"courses/{docname}")
	else:
		return get_lms_route(f"batches/{docname}")


def save_address(address: dict) -> str:
	filters = {"email_id": frappe.session.user}
	exists = frappe.db.exists("Address", filters)
	if exists:
		address_doc = frappe.get_last_doc("Address", filters=filters)
	else:
		address_doc = frappe.new_doc("Address")

	address_doc.update(address)
	address_doc.update(
		{
			"address_title": frappe.db.get_value("User", frappe.session.user, "full_name"),
			"address_type": "Billing",
			"is_primary_address": 1,
			"email_id": frappe.session.user,
		}
	)
	address_doc.save(ignore_permissions=True)
	return address_doc.name
