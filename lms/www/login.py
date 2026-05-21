import frappe

no_cache = 1

def get_context(context):
	# Delegate to Frappe's login context for all the heavy lifting
	frappe.www.login.get_context(context)

	# Override branding
	context["app_name"] = "StudyBadge"
	context["title"] = "Iniciar Sesión — StudyBadge"
