import frappe


def execute():
	if frappe.db.exists("Custom Field", "User-hide_from_rankings"):
		return

	frappe.get_doc(
		{
			"doctype": "Custom Field",
			"dt": "User",
			"fieldname": "hide_from_rankings",
			"fieldtype": "Check",
			"insert_after": "cover_image",
			"label": "Hide from Rankings",
			"description": "Hide this user from StudyBadge rankings.",
			"default": "0",
			"module": "LMS",
		}
	).insert(ignore_permissions=True)
	frappe.clear_cache(doctype="User")
