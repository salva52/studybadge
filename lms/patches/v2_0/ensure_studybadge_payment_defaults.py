import frappe


def execute():
	ensure_currency("PEN", "Peruvian Sol", "S/")
	ensure_currency("USD", "US Dollar", "$")
	ensure_source("StudyBadge Checkout")


def ensure_currency(code: str, currency_name: str, symbol: str):
	meta = frappe.get_meta("Currency")
	if frappe.db.exists("Currency", code):
		updates = {}
		if meta.has_field("enabled"):
			updates["enabled"] = 1
		if meta.has_field("symbol"):
			updates["symbol"] = symbol
		if updates:
			frappe.db.set_value("Currency", code, updates)
		return

	currency = frappe.new_doc("Currency")
	currency.name = code
	if meta.has_field("currency_name"):
		currency.currency_name = currency_name
	if meta.has_field("enabled"):
		currency.enabled = 1
	if meta.has_field("symbol"):
		currency.symbol = symbol
	currency.insert(ignore_permissions=True, ignore_mandatory=True)


def ensure_source(source_name: str):
	if frappe.db.exists("LMS Source", source_name):
		return
	source = frappe.new_doc("LMS Source")
	source.source = source_name
	source.insert(ignore_permissions=True)
