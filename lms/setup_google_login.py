"""
Script para configurar Google OAuth Login en StudyBadge LMS.

Uso:
  cd /home/salva-pc/frappe-bench
  bench --site studybadge.localhost execute lms.setup_google_login.setup_google_oauth

Antes de ejecutar, reemplaza CLIENT_ID y CLIENT_SECRET con los valores
de Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID

Pasos para obtener las credenciales:
1. Ve a https://console.cloud.google.com/apis/credentials?project=studybadge-f2391
2. Crea un "OAuth 2.0 Client ID" de tipo "Web Application"
3. En "Authorized redirect URIs" agrega:
   - http://studybadge.localhost:8000/api/method/frappe.integrations.oauth2_logins.login_via_google
   - (Si tienes dominio público) https://TU-DOMINIO/api/method/frappe.integrations.oauth2_logins.login_via_google
4. Copia el Client ID y Client Secret generados y pégalos abajo.
"""

import frappe


# ====================================================================
# REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE GOOGLE CLOUD CONSOLE
# ====================================================================
GOOGLE_CLIENT_ID = "748489238983-8lk28btdt5jquek232qd5sm35kg2e341.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
# ====================================================================


def setup_google_oauth():
    """Configura el Social Login Key para Google OAuth en Frappe."""

    if GOOGLE_CLIENT_ID == "TU_CLIENT_ID_AQUI" or GOOGLE_CLIENT_SECRET == "TU_CLIENT_SECRET_AQUI":
        print("=" * 60)
        print("ERROR: Debes reemplazar GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET")
        print("con los valores reales de Google Cloud Console.")
        print("")
        print("Edita el archivo: apps/lms/lms/setup_google_login.py")
        print("=" * 60)
        return

    # Verificar si ya existe
    if frappe.db.exists("Social Login Key", "google"):
        doc = frappe.get_doc("Social Login Key", "google")
        print(f"Social Login Key 'google' ya existe. Actualizando...")
    else:
        doc = frappe.new_doc("Social Login Key")
        doc.name = "google"
        print(f"Creando nuevo Social Login Key 'google'...")

    # Configurar los campos
    doc.provider_name = "Google"
    doc.client_id = GOOGLE_CLIENT_ID
    doc.client_secret = GOOGLE_CLIENT_SECRET
    doc.enable_social_login = 1

    # Estos valores los llena Frappe automáticamente para Google,
    # pero los ponemos explícitamente por si acaso:
    doc.base_url = "https://www.googleapis.com"
    doc.authorize_url = "https://accounts.google.com/o/oauth2/auth"
    doc.access_token_url = "https://accounts.google.com/o/oauth2/token"
    doc.redirect_url = "/api/method/frappe.integrations.oauth2_logins.login_via_google"
    doc.api_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"

    # Scopes necesarios
    doc.auth_url_data = frappe.as_json({
        "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    })

    # Icono
    doc.icon = "https://www.google.com/favicon.ico"

    # User ID property para mapear el email
    doc.user_id_property = "email"

    doc.save(ignore_permissions=True)
    frappe.db.commit()

    print("")
    print("=" * 60)
    print("✅ Google OAuth configurado exitosamente!")
    print(f"   Client ID: {GOOGLE_CLIENT_ID[:20]}...")
    print(f"   Provider: Google")
    print(f"   Habilitado: Sí")
    print("")
    print("Ahora reinicia el servidor con:")
    print("   bench restart")
    print("   (o Ctrl+C y bench start)")
    print("")
    print("Luego ve a /login y deberías ver 'Continuar con Google'")
    print("=" * 60)
