import frappe
from frappe import _

@frappe.whitelist()
def create_group(title: str, description: str = "", group_type: str = "Private", course: str = None):
	if group_type == "Course" and not course:
		frappe.throw(_("Course is required for Course groups"))
		
	group = frappe.new_doc("StudyBadge Group")
	group.title = title
	group.description = description
	group.type = group_type
	group.course = course
	group.status = "Active"
	group.insert(ignore_permissions=True)
	
	# Add creator as Admin
	member = frappe.new_doc("StudyBadge Group Member")
	member.group = group.name
	member.user = frappe.session.user
	member.role = "Admin"
	member.status = "Accepted"
	member.insert(ignore_permissions=True)
	
	return group.name

@frappe.whitelist()
def get_groups():
	# Get groups where user is an accepted member
	memberships = frappe.get_all(
		"StudyBadge Group Member",
		filters={"user": frappe.session.user, "status": "Accepted"},
		fields=["group", "role"]
	)
	
	group_names = [m.group for m in memberships]
	if not group_names:
		return []
		
	groups = frappe.get_all(
		"StudyBadge Group",
		filters={"name": ["in", group_names], "status": "Active"},
		fields=["name", "title", "description", "type", "course"]
	)
	
	for group in groups:
		# Add user role and member count
		member_doc = next((m for m in memberships if m.group == group.name), None)
		if member_doc:
			group.role = member_doc.role
		group.member_count = frappe.db.count("StudyBadge Group Member", {"group": group.name, "status": "Accepted"})
		
	return groups

@frappe.whitelist()
def get_group_details(group: str):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "status": "Accepted"}):
		frappe.throw(_("You don't have access to this group"))
		
	group_doc = frappe.get_doc("StudyBadge Group", group).as_dict()
	
	members = frappe.get_all(
		"StudyBadge Group Member",
		filters={"group": group, "status": "Accepted"},
		fields=["user", "role"]
	)
	
	# Attach full name and image
	for member in members:
		user_details = frappe.db.get_value("User", member.user, ["full_name", "user_image"], as_dict=True)
		if user_details:
			member.update(user_details)
			
	group_doc.members = members
	return group_doc

@frappe.whitelist()
def get_pending_invitations():
	invitations = frappe.get_all(
		"StudyBadge Group Member",
		filters={"user": frappe.session.user, "status": "Pending"},
		fields=["name", "group", "role"]
	)
	
	for inv in invitations:
		group_details = frappe.db.get_value("StudyBadge Group", inv.group, ["title", "description"], as_dict=True)
		if group_details:
			inv.update(group_details)
			
	return invitations

@frappe.whitelist()
def invite_user(group: str, email: str, role: str = "Member"):
	# Verify current user is Admin
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "role": "Admin", "status": "Accepted"}):
		frappe.throw(_("Only Admins can invite users"))
		
	# Check if user exists in system
	if not frappe.db.exists("User", email):
		frappe.throw(_("User with this email does not exist in the system"))
		
	if frappe.db.exists("StudyBadge Group Member", {"group": group, "user": email}):
		frappe.throw(_("User is already a member or has a pending invitation"))
		
	member = frappe.new_doc("StudyBadge Group Member")
	member.group = group
	member.user = email
	member.role = role
	member.status = "Pending"
	member.insert()
	
	return member.name

@frappe.whitelist()
def respond_invitation(group: str, response: str):
	if response not in ["Accepted", "Rejected"]:
		frappe.throw(_("Invalid response"))
		
	member_doc = frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "status": "Pending"})
	if not member_doc:
		frappe.throw(_("No pending invitation found for this group"))
		
	frappe.db.set_value("StudyBadge Group Member", member_doc, "status", response)
	return True

@frappe.whitelist()
def send_message(group: str, content: str = "", attachment: str = None):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "status": "Accepted"}):
		frappe.throw(_("You are not a member of this group"))
		
	msg = frappe.new_doc("StudyBadge Group Message")
	msg.group = group
	msg.user = frappe.session.user
	msg.content = content
	if attachment:
		msg.attachment = attachment
	msg.insert()
	
	# Fetch full details to return
	user_details = frappe.db.get_value("User", msg.user, ["full_name", "user_image"], as_dict=True)
	response = msg.as_dict()
	response.update(user_details)
	
	return response

@frappe.whitelist()
def get_messages(group: str, limit_start: int = 0, limit_page_length: int = 50):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "status": "Accepted"}):
		frappe.throw(_("You are not a member of this group"))
		
	messages = frappe.get_all(
		"StudyBadge Group Message",
		filters={"group": group},
		fields=["name", "user", "content", "attachment", "creation"],
		order_by="creation desc",
		limit_start=limit_start,
		limit_page_length=limit_page_length
	)
	
	# Reverse to get chronological order for chat UI
	messages.reverse()
	
	# Attach user details
	users_cache = {}
	for msg in messages:
		if msg.user not in users_cache:
			users_cache[msg.user] = frappe.db.get_value("User", msg.user, ["full_name", "user_image"], as_dict=True)
		if users_cache[msg.user]:
			msg.update(users_cache[msg.user])
			
	return messages

@frappe.whitelist()
def remove_member(group: str, email: str):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "role": "Admin", "status": "Accepted"}):
		frappe.throw(_("Only Admins can remove users"))
		
	if email == frappe.session.user:
		frappe.throw(_("You cannot remove yourself"))
		
	member_doc = frappe.db.exists("StudyBadge Group Member", {"group": group, "user": email})
	if not member_doc:
		frappe.throw(_("User is not in this group"))
		
	frappe.delete_doc("StudyBadge Group Member", member_doc, ignore_permissions=True)
	return True

@frappe.whitelist()
def update_group(group: str, title: str, description: str):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "role": "Admin", "status": "Accepted"}):
		frappe.throw(_("Only Admins can edit group details"))
		
	group_doc = frappe.get_doc("StudyBadge Group", group)
	group_doc.title = title
	group_doc.description = description
	group_doc.save(ignore_permissions=True)
	
	# Since title is the ID, changing title renames the document in Frappe.
	# Wait, `StudyBadge Group` has autoname `field:title`.
	# If we change title, does `save` rename it?
	# In Frappe, changing a field used for autoname doesn't automatically rename the document unless handled specifically or if `allow_rename` is checked.
	# To be safe, if title changes, we might need to use `frappe.rename_doc`.
	# Actually, since renaming affects all linked messages and members, it's complex. Let's let them edit the description and title, but renaming the ID might fail or succeed depending on `allow_rename` and cascade.
	# Yes, allow_rename is 1. `frappe.rename_doc("StudyBadge Group", group, title, ignore_permissions=True)`
	
	if group_doc.name != title:
		frappe.rename_doc("StudyBadge Group", group, title, ignore_permissions=True)
		
	return title

@frappe.whitelist()
def delete_group(group: str):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "role": "Admin", "status": "Accepted"}):
		frappe.throw(_("Only Admins can delete the group"))
		
	frappe.db.delete("StudyBadge Group Member", {"group": group})
	frappe.db.delete("StudyBadge Group Message", {"group": group})
	frappe.delete_doc("StudyBadge Group", group, ignore_permissions=True)
	return True
