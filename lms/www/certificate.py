from urllib.parse import quote

import frappe

no_cache = 1


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	context.certificate_id = (frappe.form_dict.get("certificate_id") or "").strip()
	context.brand_name = frappe.db.get_single_value("Website Settings", "app_name") or "StudyBadge"
	context.logo = "/assets/lms/images/studybadge/studybadge-logo.png"
	context.title = "Verificar certificado | StudyBadge"

	if not context.certificate_id:
		context.verified = None
		return context

	certificate = frappe.db.get_value(
		"LMS Certificate",
		context.certificate_id,
		[
			"name",
			"member",
			"member_name",
			"course",
			"course_title",
			"batch_name",
			"batch_title",
			"issue_date",
			"expiry_date",
			"template",
		],
		as_dict=True,
	)
	if not certificate:
		context.verified = False
		return context

	course = None
	if certificate.course:
		course = frappe.db.get_value(
			"LMS Course",
			certificate.course,
			["title", "image"],
			as_dict=True,
		)

	context.verified = True
	context.certificate = certificate
	context.course = course
	context.learner_name = certificate.member_name or frappe.db.get_value(
		"User", certificate.member, "full_name"
	)
	context.program_title = certificate.course_title or certificate.batch_title
	context.download_url = (
		"/api/method/lms.lms.doctype.lms_certificate.lms_certificate.download_public_certificate"
		f"?certificate_id={quote(certificate.name)}"
	)
	return context
