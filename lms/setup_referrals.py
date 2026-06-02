import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_referrals():
    create_referral_doctype()
    create_referral_reward_log_doctype()
    print("Referral Doctypes setup complete.")

def create_referral_doctype():
    if not frappe.db.exists("DocType", "LMS Referral"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "LMS Referral",
            "module": "LMS",
            "custom": 1,
            "istable": 0,
            "fields": [
                {"fieldname": "referrer", "fieldtype": "Link", "options": "User", "label": "Referrer", "reqd": 1},
                {"fieldname": "referred_email", "fieldtype": "Data", "label": "Referred Email", "reqd": 1, "unique": 1},
                {"fieldname": "referred_user", "fieldtype": "Link", "options": "User", "label": "Referred User (If Signed Up)"},
                {"fieldname": "status", "fieldtype": "Select", "options": "Pending\nSigned Up\nVerified", "label": "Status", "default": "Pending"},
                {"fieldname": "reward_granted", "fieldtype": "Check", "label": "Reward Granted", "default": "0"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Created LMS Referral Doctype")
    else:
        print("LMS Referral Doctype already exists")

def create_referral_reward_log_doctype():
    if not frappe.db.exists("DocType", "LMS Referral Reward Log"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "LMS Referral Reward Log",
            "module": "LMS",
            "custom": 1,
            "istable": 0,
            "fields": [
                {"fieldname": "user", "fieldtype": "Link", "options": "User", "label": "User", "reqd": 1},
                {"fieldname": "milestone", "fieldtype": "Int", "label": "Milestone (e.g. 5 or 10)", "reqd": 1},
                {"fieldname": "reward_type", "fieldtype": "Data", "label": "Reward Type (Coupon or Plus)"},
                {"fieldname": "date_granted", "fieldtype": "Date", "label": "Date Granted"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Created LMS Referral Reward Log Doctype")
    else:
        print("LMS Referral Reward Log Doctype already exists")

if __name__ == "__main__":
    setup_referrals()
