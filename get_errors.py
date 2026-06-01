import frappe

def get_errors():
    errors = frappe.get_all('Error Log', fields=['method', 'error'], limit=3, order_by='creation desc')
    for e in errors:
        print(f"Method: {e.method}")
        print(f"Error: {e.error}")
        print("-" * 50)
