import frappe

def create_home_folder():
    if not frappe.db.exists("File", "Home"):
        frappe.get_doc({
            "doctype": "File",
            "file_name": "Home",
            "is_folder": 1,
            "folder": "Home",
            "is_home_folder": 1
        }).insert(ignore_permissions=True, ignore_mandatory=True)
        frappe.db.commit()
        print("Home folder created!")
    else:
        print("Home folder already exists.")
