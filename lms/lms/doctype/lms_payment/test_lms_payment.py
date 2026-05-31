# Copyright (c) 2023, Frappe and Contributors
# See license.txt

import frappe

from lms.lms.payments import process_mercadopago_certificate_payment
from lms.lms.test_helpers import BaseTestUtils


class TestLMSPayment(BaseTestUtils):
	def setUp(self):
		super().setUp()
		self.student = self._create_user(
			"certificate-student@example.com",
			"Certificate",
			"Student",
			["LMS Student"],
		)
		self.course = self._create_course(
			title="Certificate Payment Course",
			instructor="Administrator",
		)
		self.enrollment = self._create_enrollment(self.student.name, self.course.name)
		frappe.db.set_value(
			"LMS Course",
			self.course.name,
			{"paid_certificate": 1, "course_price": 25, "currency": "PEN"},
		)
		frappe.db.set_value("LMS Enrollment", self.enrollment.name, "progress", 100)
		self.enrollment.reload()

	def test_approved_mercadopago_certificate_payment_unlocks_enrollment_member(self):
		payment = frappe.new_doc("LMS Payment")
		payment.update(
			{
				"member": self.student.name,
				"billing_name": "Certificate Student",
				"amount": 25,
				"currency": "PEN",
				"payment_for_document_type": "LMS Course",
				"payment_for_document": self.course.name,
				"payment_for_certificate": 1,
				"external_reference": "studybadge-certificate::test-payment",
			}
		)
		payment.save(ignore_permissions=True, ignore_mandatory=True)
		self.cleanup_items.append(("LMS Payment", payment.name))

		process_mercadopago_certificate_payment(
			{
				"id": "123456789",
				"status": "approved",
				"status_detail": "accredited",
				"external_reference": payment.external_reference,
				"metadata": {"lms_payment": payment.name},
			}
		)

		payment.reload()
		self.enrollment.reload()
		self.assertTrue(payment.payment_received)
		self.assertEqual(payment.payment_status, "approved")
		self.assertEqual(self.enrollment.purchased_certificate, 1)
		self.assertEqual(self.enrollment.payment, payment.name)
		self.assertTrue(self.enrollment.certificate)

		process_mercadopago_certificate_payment(
			{
				"id": "123456789",
				"status": "approved",
				"status_detail": "accredited",
				"external_reference": payment.external_reference,
				"metadata": {"lms_payment": payment.name},
			}
		)
		self.enrollment.reload()
		self.assertEqual(self.enrollment.payment, payment.name)
