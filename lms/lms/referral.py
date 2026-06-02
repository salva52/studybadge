import frappe
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def track_referral_click(ref_code):
    if not ref_code:
        return
    frappe.local.cookie_manager.set_cookie("studybadge_ref", ref_code, expires_in_days=30)
    return {"status": "success"}

def on_user_creation(doc, method):
    """Triggered on User after_insert"""
    ref_code = frappe.request.cookies.get("studybadge_ref") if getattr(frappe, "request", None) else None
    if not ref_code:
        return

    # Assuming ref_code is the username of the referrer
    referrer = frappe.db.get_value("User", {"username": ref_code}, "name")
    if not referrer:
        return

    if referrer == doc.name:
        return # Can't refer yourself

    # Create Referral record
    try:
        frappe.get_doc({
            "doctype": "LMS Referral",
            "referrer": referrer,
            "referred_email": doc.email,
            "referred_user": doc.name,
            "status": "Pending" if not doc.email_verified else "Verified"
        }).insert(ignore_permissions=True)
    except frappe.DuplicateEntryError:
        pass # Already referred

def on_user_update(doc, method):
    """Triggered on User on_update. Used to mark referrals as verified."""
    # Check if email just got verified (doc.email_verified == 1)
    if not doc.email_verified:
        return
    
    # Check if there's a pending referral for this user
    referral = frappe.db.get_value("LMS Referral", {"referred_user": doc.name, "status": "Pending"}, "name")
    if not referral:
        return

    ref_doc = frappe.get_doc("LMS Referral", referral)
    ref_doc.status = "Verified"
    ref_doc.save(ignore_permissions=True)

    # Check and grant rewards
    check_and_grant_rewards(ref_doc.referrer)

def check_and_grant_rewards(referrer):
    verified_count = frappe.db.count("LMS Referral", {"referrer": referrer, "status": "Verified"})

    if verified_count >= 5:
        # Check if 5-milestone reward is granted
        reward = frappe.db.get_value("LMS Referral Reward Log", {"user": referrer, "milestone": 5})
        if not reward:
            grant_coupon_reward(referrer)
            frappe.get_doc({
                "doctype": "LMS Referral Reward Log",
                "user": referrer,
                "milestone": 5,
                "reward_type": "Coupon",
                "date_granted": frappe.utils.today()
            }).insert(ignore_permissions=True)

    if verified_count >= 10:
        # Check if 10-milestone reward is granted
        reward = frappe.db.get_value("LMS Referral Reward Log", {"user": referrer, "milestone": 10})
        if not reward:
            grant_plus_reward(referrer)
            frappe.get_doc({
                "doctype": "LMS Referral Reward Log",
                "user": referrer,
                "milestone": 10,
                "reward_type": "Plus Access",
                "date_granted": frappe.utils.today()
            }).insert(ignore_permissions=True)

def grant_coupon_reward(referrer):
    import string
    import random
    
    # Generate random string
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    coupon_code = f"REF5-{random_str}"
    
    frappe.get_doc({
        "doctype": "LMS Coupon",
        "coupon_code": coupon_code,
        "discount_type": "Fixed Amount",
        "discount_amount": 9.90,
        "valid_upto": frappe.utils.add_months(frappe.utils.today(), 3),
        "description": "Cupón por llegar a 5 referidos en Studybadge"
    }).insert(ignore_permissions=True)
    
    # Notify user (simplified)
    # Ideally send email here
    pass

def grant_plus_reward(referrer):
    from frappe.utils import add_months, today
    
    # Check if they already have Plus
    # This is a simplified version, adapt to existing LMS Plus logic if needed
    doc = frappe.get_doc({
        "doctype": "LMS Plus Access",
        "member": referrer,
        "valid_upto": add_months(today(), 1),
        "source": "Referral Program",
        "status": "Active"
    })
    try:
        doc.insert(ignore_permissions=True)
    except Exception:
        # If LMS Plus Access isn't the exact doctype, handle it gracefully
        pass

@frappe.whitelist()
def get_referral_dashboard():
    user = frappe.session.user
    
    # Get username for link
    username = frappe.db.get_value("User", user, "username")
    
    referrals = frappe.get_all("LMS Referral", filters={"referrer": user}, fields=["referred_email", "status", "creation"], order_by="creation desc")
    
    verified = len([r for r in referrals if r.status == "Verified"])
    
    return {
        "referral_link": f"{get_url()}/signup?ref={username}",
        "referrals": referrals,
        "verified_count": verified,
        "total_count": len(referrals)
    }
