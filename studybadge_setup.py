"""
StudyBadge - Custom Field Setup Script
Run this with: bench --site studybadge.localhost execute studybadge_setup.create_custom_field
Or manually via bench console.

This adds a 'custom_recommended_by_studybadge' checkbox to LMS Course doctype.
"""
import frappe

def create_custom_field():
    """Create the 'Recommended by StudyBadge' custom field on LMS Course"""
    if not frappe.db.exists("Custom Field", "LMS Course-custom_recommended_by_studybadge"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "LMS Course",
            "fieldname": "custom_recommended_by_studybadge",
            "fieldtype": "Check",
            "label": "Recommended by StudyBadge",
            "insert_after": "featured",
            "description": "Si está activo, el curso mostrará el badge 'Recomendado por StudyBadge' en la tarjeta del curso.",
            "default": "0",
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Custom Field 'custom_recommended_by_studybadge' created on LMS Course")
    else:
        print("ℹ️ Custom Field already exists")

if __name__ == "__main__":
    create_custom_field()
