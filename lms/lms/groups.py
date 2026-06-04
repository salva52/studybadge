import frappe
from frappe import _

@frappe.whitelist()
def create_group(title: str, description: str = "", type: str = "Private", course: str = None):
	if type == "Course" and not course:
		frappe.throw(_("Course is required for Course groups"))
		
	group = frappe.new_doc("StudyBadge Group")
	group.title = title
	group.description = description
	group.type = type
	group.course = course
	group.status = "Active"
	group.insert()
	
	# Add creator as Admin
	member = frappe.new_doc("StudyBadge Group Member")
	member.group = group.name
	member.user = frappe.session.user
	member.role = "Admin"
	member.status = "Accepted"
	member.insert()
	
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
def send_message(group: str, content: str):
	if not frappe.db.exists("StudyBadge Group Member", {"group": group, "user": frappe.session.user, "status": "Accepted"}):
		frappe.throw(_("You are not a member of this group"))
		
	msg = frappe.new_doc("StudyBadge Group Message")
	msg.group = group
	msg.user = frappe.session.user
	msg.content = content
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
		fields=["name", "user", "content", "creation"],
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
