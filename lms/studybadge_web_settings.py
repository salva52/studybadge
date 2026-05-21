import frappe

def run():
    ws = frappe.get_doc("Website Settings")
    ws.favicon = "/assets/lms/images/studybadge/favicon.svg"
    ws.app_name = "StudyBadge"
    ws.splash_image = "/assets/lms/images/studybadge/studybadge-logo.png"
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Website Settings actualizados correctamente para StudyBadge")

if __name__ == "__main__":
    run()
