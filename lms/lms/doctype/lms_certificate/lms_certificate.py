# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

from urllib.parse import quote

import frappe
from frappe import _
from frappe.email.doctype.email_template.email_template import get_email_template
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import nowdate
from frappe.utils.telemetry import capture


class LMSCertificate(Document):
	def validate(self):
		self.validate_criteria()
		self.validate_duplicate_certificate()

	def autoname(self):
		self.name = make_autoname("hash", self.doctype)

	def after_insert(self):
		capture("certificate_issued", "lms")
		self.send_certification_email()

	def send_certification_email(self):
		outgoing_email_account = frappe.get_cached_value(
			"Email Account", {"default_outgoing": 1, "enable_outgoing": 1}, "name"
		)
		if outgoing_email_account or frappe.conf.get("mail_login"):
			self.send_mail()

	def send_mail(self):
		subject = _("Tu certificado StudyBadge ya está listo")
		template = "certification"
		custom_template = frappe.db.get_single_value("LMS Settings", "certification_template")
		course_title = frappe.db.get_value("LMS Course", self.course, "title")
		verification_url = get_certificate_verification_url(self.name)
		certificate_url = frappe.utils.get_url(
			"/api/method/frappe.utils.print_format.download_pdf"
			f"?doctype=LMS+Certificate&name={quote(self.name)}&format={quote(self.template)}"
		)
		course_url = frappe.utils.get_url(f"/lms/courses/{self.course}/certification")

		args = {
			"member_name": self.member_name,
			"course_name": self.course,
			"course_title": course_title,
			"name": self.name,
			"template": self.template,
			"certificate_url": certificate_url,
			"verification_url": verification_url,
			"course_url": course_url,
			"issue_date": frappe.utils.format_date(self.issue_date, "long"),
		}

		if custom_template:
			email_template = get_email_template(custom_template, args)
			subject = email_template.get("subject")
			content = email_template.get("message")
		attachments = self.get_certificate_email_attachments()
		frappe.sendmail(
			recipients=self.member,
			subject=subject,
			template=template if not custom_template else None,
			content=content if custom_template else None,
			args=args,
			attachments=attachments,
			header=[subject, "blue"],
		)

	def get_certificate_email_attachments(self):
		try:
			return [
				frappe.attach_print(
					self.doctype,
					self.name,
					file_name=f"certificado-studybadge-{self.name}",
					print_format=self.template,
				)
			]
		except Exception:
			frappe.log_error(
				frappe.get_traceback(),
				f"StudyBadge Certificate PDF Attachment Failed: {self.name}",
			)
			return []

	def validate_criteria(self):
		self.validate_role_of_owner()
		if self.batch_name:
			self.validate_batch_enrollment()
		elif self.course:
			self.validate_course_enrollment()

	def validate_role_of_owner(self):
		roles = frappe.get_roles()
		is_admin = any(role in roles for role in ["Moderator", "Course Creator", "Batch Evaluator"])
		if not self.course and not self.batch_name and not is_admin:
			frappe.throw(_("Course or Batch is required to issue a certificate."))

	def validate_batch_enrollment(self):
		if self.batch_name:
			is_enrolled = frappe.db.exists(
				"LMS Batch Enrollment", {"batch": self.batch_name, "member": self.member}
			)
			if not is_enrolled:
				frappe.throw(_("Certification cannot be issued as the member is not enrolled in this batch."))

	def validate_course_enrollment(self):
		if self.course:
			is_enrolled = frappe.db.exists("LMS Enrollment", {"course": self.course, "member": self.member})
			if not is_enrolled:
				frappe.throw(
					_("Certification cannot be issued as the member is not enrolled in this course.")
				)

			certificate_enabled = frappe.db.get_value(
				"LMS Course", self.course, ["enable_certification", "paid_certificate"], as_dict=True
			)
			if certificate_enabled and (
				certificate_enabled.enable_certification or certificate_enabled.paid_certificate
			):
				progress = frappe.db.get_value(
					"LMS Enrollment", {"course": self.course, "member": self.member}, "progress"
				)
				if progress < 100:
					frappe.throw(
						_("Certification cannot be issued as the member has not completed the course.")
					)

	def validate_duplicate_certificate(self):
		self.validate_course_duplicates()
		self.validate_batch_duplicates()

	def validate_course_duplicates(self):
		if self.course:
			course_duplicates = frappe.get_all(
				"LMS Certificate",
				filters={
					"member": self.member,
					"name": ["!=", self.name],
					"course": self.course,
				},
				fields=["name", "course", "course_title"],
			)
			if len(course_duplicates):
				full_name = frappe.db.get_value("User", self.member, "full_name")
				frappe.throw(
					_("{0} is already certified for the course {1}").format(
						full_name, course_duplicates[0].course_title
					)
				)

	def validate_batch_duplicates(self):
		if self.batch_name:
			batch_duplicates = frappe.get_all(
				"LMS Certificate",
				filters={
					"member": self.member,
					"name": ["!=", self.name],
					"batch_name": self.batch_name,
				},
				fields=["name", "batch_name", "batch_title"],
			)
			if len(batch_duplicates):
				full_name = frappe.db.get_value("User", self.member, "full_name")
				frappe.throw(
					_("{0} is already certified for the batch {1}").format(
						full_name, batch_duplicates[0].batch_title
					)
				)

	def on_update(self):
		frappe.share.add_docshare(
			self.doctype,
			self.name,
			self.member,
			write=1,
			share=1,
			flags={"ignore_share_permission": True},
		)


def has_website_permission(doc, ptype, user, verbose=False):
	if ptype in ["read", "print"] and doc.published:
		return True
	if doc.member == user and ptype == "create":
		return True
	return False


def is_certified(course, member: str | None = None):
	member = member or frappe.session.user
	certificate = frappe.get_all("LMS Certificate", {"member": member, "course": course})
	if len(certificate):
		return certificate[0].name
	return


def get_certificate_verification_url(certificate_id: str):
	return frappe.utils.get_url(f"/certificate?certificate_id={quote(certificate_id or '')}")


def get_certificate_qr_svg(certificate_id: str, scale: int = 3):
	import io

	import pyqrcode

	qr = pyqrcode.create(get_certificate_verification_url(certificate_id), error="M")
	buffer = io.BytesIO()
	qr.svg(
		buffer,
		scale=scale,
		quiet_zone=1,
		xmldecl=False,
		svgns=False,
		module_color="#0a2351",
		background="#ffffff",
	)
	return buffer.getvalue().decode("utf-8")


@frappe.whitelist(allow_guest=True)
def download_public_certificate(certificate_id: str):
	certificate = frappe.db.get_value(
		"LMS Certificate",
		certificate_id,
		["name", "template"],
		as_dict=True,
	)
	if not certificate:
		frappe.throw(_("Certificate not found."), frappe.DoesNotExistError)

	attachment = frappe.attach_print(
		"LMS Certificate",
		certificate.name,
		file_name=f"certificado-studybadge-{certificate.name}",
		print_format=certificate.template,
	)
	frappe.local.response.filename = attachment["fname"]
	frappe.local.response.filecontent = attachment["fcontent"]
	frappe.local.response.type = "download"
	frappe.local.response.content_type = "application/pdf"


@frappe.whitelist()
def create_certificate(course: str):
	return create_course_certificate(course, frappe.session.user)


def create_course_certificate(course: str, member: str | None = None):
	member = member or frappe.session.user
	certificate = is_certified(course, member)
	if certificate:
		return frappe.db.get_value(
			"LMS Certificate", certificate, ["name", "course", "template", "issue_date"], as_dict=True
		)

	validate_certification_eligibility(course, member)
	default_certificate_template = get_default_certificate_template()
	certificate = frappe.get_doc(
		{
			"doctype": "LMS Certificate",
			"member": member,
			"course": course,
			"issue_date": nowdate(),
			"template": default_certificate_template,
		}
	)
	certificate.save(ignore_permissions=True)
	frappe.db.set_value(
		"LMS Enrollment",
		{"course": course, "member": member},
		"certificate",
		certificate.name,
	)
	return certificate


def get_default_certificate_template():
	default_certificate_template = frappe.db.get_value(
		"Property Setter",
		{
			"doc_type": "LMS Certificate",
			"property": "default_print_format",
		},
		"value",
	)
	if not default_certificate_template:
		default_certificate_template = frappe.db.get_value(
			"Print Format",
			{
				"doc_type": "LMS Certificate",
			},
		)

	return default_certificate_template


def validate_certification_eligibility(course, member: str | None = None):
	member = member or frappe.session.user
	enrollment = frappe.db.get_value(
		"LMS Enrollment",
		{"course": course, "member": member},
		["name", "progress", "purchased_certificate"],
		as_dict=True,
	)
	if not enrollment:
		frappe.throw(_("You are not enrolled in this course."))

	course_settings = frappe.db.get_value(
		"LMS Course",
		course,
		["enable_certification", "paid_certificate"],
		as_dict=True,
	)
	if not course_settings or not (course_settings.enable_certification or course_settings.paid_certificate):
		frappe.throw(_("Certification is not enabled for this course."))

	if course_settings.paid_certificate:
		from lms.lms.subscriptions import has_active_plus

		if not enrollment.purchased_certificate and not has_active_plus(member):
			frappe.throw(_("Please purchase this certificate or activate StudyBadge Plus first."))

	if enrollment.progress < 100:
		frappe.throw(_("You have not completed the course yet."))


def auto_issue_course_certificate(course: str, member: str | None = None):
	member = member or frappe.session.user
	try:
		return create_course_certificate(course, member)
	except Exception:
		frappe.log_error(
			frappe.get_traceback(),
			f"StudyBadge Auto Certificate Failed: {course} / {member}",
		)


def has_permission(doc, ptype="read", user=None):
	user = user or frappe.session.user
	roles = frappe.get_roles(user)
	if "Moderator" in roles or "Course Creator" in roles or "Batch Evaluator" in roles:
		return True
	if doc.owner == user:
		return True
	if ptype not in ("read", "select", "print"):
		return False
	return doc.published


def get_permission_query_conditions(user):
	user = user or frappe.session.user
	roles = frappe.get_roles(user)
	if "Moderator" in roles or "Course Creator" in roles or "Batch Evaluator" in roles:
		return None
	return """(`tabLMS Certificate`.published = 1)"""
