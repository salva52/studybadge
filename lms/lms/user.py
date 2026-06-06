import frappe
from frappe import _
from frappe.model.naming import append_number_if_name_exists
from frappe.utils import cint, escape_html, random_string
from frappe.website.utils import cleanup_page_name, is_signup_disabled

from lms.lms.utils import get_country_code, get_lms_route


def validate_username_duplicates(doc, method):
	while not doc.username or doc.username_exists():
		doc.username = append_number_if_name_exists(
			doc.doctype, cleanup_page_name(doc.full_name), fieldname="username"
		)
	if " " in doc.username:
		doc.username = doc.username.replace(" ", "")

	if len(doc.username) < 4:
		doc.username = doc.email.replace("@", "").replace(".", "")


def add_lms_student_role(doc, method):
	doc.append_roles("LMS Student")


@frappe.whitelist(allow_guest=True)  # nosemgrep: frappe-semgrep-rules.rules.security.guest-whitelisted-method
def sign_up(email: str, full_name: str, verify_terms: bool, user_category: str, ref_code: str = None, captcha_token: str = None):
	try:
		from studybadge_ai.keys import verify_recaptcha
		if not verify_recaptcha(captcha_token, "sign_up"):
			frappe.throw(_("Fallo en verificación reCAPTCHA. Eres un bot?"), _("Not Allowed"))
	except ImportError:
		pass  # studybadge_ai not installed

	if ref_code:
		frappe.local.flags.studybadge_ref = ref_code

	if is_signup_disabled():
		frappe.throw(_("Sign Up is disabled"), _("Not Allowed"))

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		max_signups_allowed_per_hour = cint(frappe.get_system_settings("max_signups_allowed_per_hour") or 300)
		users_created_past_hour = frappe.db.get_creation_count("User", 60)
		if users_created_past_hour >= max_signups_allowed_per_hour:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

	import random
	import time
	otp = str(random.randint(100000, 999999))

	cache_key = f"signup_data:{email}"
	signup_data = {
		"email": email,
		"full_name": full_name,
		"verify_terms": verify_terms,
		"user_category": user_category,
		"ref_code": ref_code,
		"otp": otp,
		"expires_at": time.time() + 600
	}
	frappe.cache().set_value(cache_key, signup_data, expires_in_sec=600)

	message = f"""
	<div style="padding: 20px; font-family: sans-serif; text-align: center; color: #171717;">
		<h2>Código de Verificación</h2>
		<p>Hola {escape_html(full_name)}, usa este código para completar tu registro:</p>
		<h1 style="font-size: 32px; letter-spacing: 5px; color: #0a2251; padding: 10px 20px; background: #f3f6fb; display: inline-block; border-radius: 8px;">{otp}</h1>
		<p>Este código expirará en 10 minutos.</p>
	</div>
	"""
	
	try:
		frappe.sendmail(
			recipients=email,
			subject=_("Tu código de verificación"),
			message=message,
			now=True
		)
	except Exception as e:
		frappe.log_error(title="OTP Email Error", message=frappe.get_traceback())
		frappe.throw(_("Error al enviar el correo de verificación. Inténtalo de nuevo."))

	return {"status": "success"}


@frappe.whitelist(allow_guest=True)
def verify_otp_only(**kwargs):
	"""Step 1: Just verify the OTP code is correct, don't create the account yet."""
	email = kwargs.get("email")
	otp = kwargs.get("otp")
	if not email or not otp:
		return {"status": "error", "message": "Faltan datos."}
	import time

	# Rate limit: max 5 attempts per email
	attempts_key = f"otp_attempts:{email}"
	attempts = cint(frappe.cache().get_value(attempts_key) or 0)
	if attempts >= 5:
		return {"status": "error", "message": "Demasiados intentos. Solicita un nuevo código."}

	frappe.cache().set_value(attempts_key, attempts + 1, expires_in_sec=600)

	cache_key = f"signup_data:{email}"
	data = frappe.cache().get_value(cache_key)

	if not data:
		return {"status": "error", "message": "El código ha expirado. Solicita uno nuevo."}

	if str(data.get("otp")) != str(otp):
		remaining = 5 - (attempts + 1)
		return {"status": "error", "message": f"Código incorrecto. Te quedan {remaining} intentos."}

	# Mark as verified in cache
	data["otp_verified"] = True
	data["verified_at"] = time.time()
	frappe.cache().set_value(cache_key, data, expires_in_sec=600)
	# Reset attempts on success
	frappe.cache().delete_value(attempts_key)

	return {"status": "success"}


@frappe.whitelist(allow_guest=True)
def verify_signup_otp(**kwargs):
	"""Step 2: Create the account after OTP was verified."""
	email = kwargs.get("email")
	otp = kwargs.get("otp")
	password = kwargs.get("password")
	if not email or not otp or not password:
		return {"status": "error", "message": "Faltan datos."}
	cache_key = f"signup_data:{email}"
	data = frappe.cache().get_value(cache_key)

	if not data:
		return {"status": "error", "message": "La sesión ha expirado. Regístrate de nuevo."}

	# Accept if OTP was pre-verified OR if it matches now
	if not data.get("otp_verified") and str(data.get("otp")) != str(otp):
		return {"status": "error", "message": "Código de verificación incorrecto."}

	if data.get("ref_code"):
		frappe.local.flags.studybadge_ref = data.get("ref_code")

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": escape_html(data.get("full_name")),
			"verify_terms": data.get("verify_terms"),
			"user_category": data.get("user_category"),
			"country": "",
			"enabled": 1,
			"new_password": password,
			"user_type": "Website User",
			"send_welcome_email": 0,
			"email_verified": 1,
		}
	)
	user.flags.ignore_permissions = True
	user.flags.ignore_password_policy = True
	frappe.flags.mute_messages = True

	try:
		user.insert()
	except Exception as e:
		frappe.log_error(title="Signup Error", message=frappe.get_traceback())
		return {"status": "error", "message": f"Error al crear la cuenta: {str(e)}"}

	default_role = frappe.db.get_single_value("Portal Settings", "default_role")
	if default_role:
		user.add_roles(default_role)

	user.add_roles("LMS Student")
	set_country_from_ip(None, user.name)

	frappe.cache().delete_value(cache_key)
	frappe.local.login_manager.login_as(email)

	return {"status": "success"}


@frappe.whitelist(allow_guest=True)
def resend_signup_otp(**kwargs):
	email = kwargs.get("email")
	if not email:
		return {"status": "error", "message": "Falta el correo."}
	"""Resend OTP with rate limiting: max 3 resends, 60s cooldown."""
	import random
	import time

	# Rate limit: cooldown
	cooldown_key = f"otp_cooldown:{email}"
	last_sent = frappe.cache().get_value(cooldown_key)
	if last_sent:
		elapsed = time.time() - float(last_sent)
		if elapsed < 60:
			wait = int(60 - elapsed)
			return {"status": "error", "message": f"Espera {wait} segundos antes de solicitar otro código."}

	# Rate limit: max resends
	resend_key = f"otp_resends:{email}"
	resends = cint(frappe.cache().get_value(resend_key) or 0)
	if resends >= 3:
		return {"status": "error", "message": "Has alcanzado el límite de reenvíos. Intenta registrarte de nuevo en 10 minutos."}

	cache_key = f"signup_data:{email}"
	data = frappe.cache().get_value(cache_key)

	if not data:
		return {"status": "error", "message": "La sesión ha expirado. Regístrate de nuevo."}

	# Generate new OTP
	new_otp = str(random.randint(100000, 999999))
	data["otp"] = new_otp
	data["otp_verified"] = False
	data["expires_at"] = time.time() + 600
	frappe.cache().set_value(cache_key, data, expires_in_sec=600)

	# Reset attempt counter for new OTP
	frappe.cache().delete_value(f"otp_attempts:{email}")

	# Track resends and cooldown
	frappe.cache().set_value(resend_key, resends + 1, expires_in_sec=600)
	frappe.cache().set_value(cooldown_key, str(time.time()), expires_in_sec=60)

	full_name = data.get("full_name", "")
	message = f"""
	<div style="padding: 20px; font-family: sans-serif; text-align: center; color: #171717;">
		<h2>Código de Verificación</h2>
		<p>Hola {escape_html(full_name)}, aquí tienes tu nuevo código:</p>
		<h1 style="font-size: 32px; letter-spacing: 5px; color: #0a2251; padding: 10px 20px; background: #f3f6fb; display: inline-block; border-radius: 8px;">{new_otp}</h1>
		<p>Este código expirará en 10 minutos.</p>
	</div>
	"""

	try:
		frappe.sendmail(
			recipients=email,
			subject=_("Tu nuevo código de verificación"),
			message=message,
			now=True
		)
	except Exception:
		frappe.log_error(title="OTP Resend Email Error", message=frappe.get_traceback())
		return {"status": "error", "message": "Error al enviar el correo. Inténtalo de nuevo."}

	return {"status": "success", "message": "Nuevo código enviado a tu correo."}


def set_country_from_ip(login_manager: object = None, user: str = None):
	if not user and login_manager:
		user = login_manager.user
	user_country = frappe.db.get_value("User", user, "country")
	if user_country:
		return
	frappe.db.set_value("User", user, "country", get_country_code())
	return


def on_login(login_manager):
	default_app = frappe.db.get_single_value("System Settings", "default_app")
	if default_app == "lms":
		frappe.local.response["home_page"] = get_lms_route()


def notify_admin_new_user(doc, method):
	try:
		frappe.sendmail(
			recipients=["salvaalca52@gmail.com"],
			subject="¡Nuevo usuario en StudyBadge!",
			message=f"Se ha registrado un nuevo usuario en StudyBadge.<br><br>Nombre: {doc.full_name}<br>Email: {doc.email}<br>Usuario: {doc.username}",
			delayed=True
		)
	except Exception as e:
		frappe.log_error(title="Error sending admin notification", message=str(e))
