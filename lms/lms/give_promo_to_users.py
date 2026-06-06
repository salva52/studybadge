import sys
import frappe

def give_promo_to_all_recent_users():
    # Obtener usuarios creados recientemente (ej. últimos 7 días) que no tengan suscripción
    recent_users = frappe.get_all("User", filters={"creation": [">", frappe.utils.add_days(frappe.utils.today(), -30)]}, fields=["name", "creation"])
    
    count = 0
    for u in recent_users:
        # Verificar si ya tiene suscripción Plus
        has_sub = frappe.db.exists("StudyBadge Plus Subscription", {"member": u.name})
        if not has_sub:
            try:
                frappe.get_doc({
                    "doctype": "StudyBadge Plus Subscription",
                    "member": u.name,
                    "status": "active",
                    "amount": 0.0,
                    "payment_gateway": "Launch Promo Retroactive",
                    "next_payment_date": frappe.utils.add_months(frappe.utils.today(), 1),
                    "date_created": frappe.utils.now_datetime()
                }).insert(ignore_permissions=True)
                count += 1
                print(f"Suscripción otorgada a: {u.name}")
            except Exception as e:
                print(f"Error con {u.name}: {e}")
                
    print(f"\nSe otorgó StudyBadge Plus a {count} usuarios.")

def give_promo_to_single_user(email):
    if not frappe.db.exists("User", email):
        print(f"Error: El usuario {email} no existe en el sistema.")
        return

    has_sub = frappe.db.exists("StudyBadge Plus Subscription", {"member": email})
    if not has_sub:
        try:
            frappe.get_doc({
                "doctype": "StudyBadge Plus Subscription",
                "member": email,
                "status": "active",
                "amount": 0.0,
                "payment_gateway": "Manual Promo",
                "next_payment_date": frappe.utils.add_months(frappe.utils.today(), 12),
                "date_created": frappe.utils.now_datetime()
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"Suscripción otorgada exitosamente a: {email}")
        except Exception as e:
            print(f"Error al otorgar suscripción a {email}: {e}")
    else:
        print(f"El usuario {email} ya tiene una suscripción Plus activa.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: bench --site [tu-sitio] execute give_promo_to_users.give_promo_to_all_recent_users")
    else:
        # Esto es solo si se ejecuta como script independiente, pero en frappe se usa bench execute
        frappe.init(site=sys.argv[1])
        frappe.connect()
        give_promo_to_all_recent_users()
        frappe.db.commit()
