import os
import sys
import frappe

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)
apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

def run():
    frappe.set_user("Administrator")
    print("Iniciando borrado de cursos...")
    from lms.lms.api import delete_course
    
    courses_to_delete = [
        "Trading Institucional y Pruebas de Fondeo",
        "Desarrollo Avanzado y Scripting en Roblox",
        "Composición de Trap y Reggaetón",
        "Creación de Bots en Discord con Python",
        "Matemáticas Aplicadas para Negocios",
        "Lanzamiento de Marcas Digitales",
        "Redacción y Argumentación Universitaria",
        "Trigonometría Básica y Geometría Espacial",
        "Productividad y Gestión de Proyectos Tech",
        "Desarrollo Web Ágil y Landing Pages"
    ]
    
    for title in courses_to_delete:
        course_name = frappe.db.get_value("LMS Course", {"title": title})
        if course_name:
            print(f"Borrando {title} ({course_name})...")
            try:
                delete_course(course_name)
            except Exception as e:
                print(f"Error borrando con API: {e}")
            
            # Borrado forzado por si acaso
            frappe.db.delete("LMS Assignment", {"course": course_name})
            frappe.db.delete("Course Chapter", {"course": course_name})
            frappe.db.delete("Course Lesson", {"course": course_name})
            
            if frappe.db.exists("LMS Course", course_name):
                frappe.db.delete("LMS Course", {"name": course_name})
            print(f"-> ¡{title} eliminado!")
        else:
            print(f"-> {title} no encontrado. Omitiendo.")
            
    frappe.db.commit()
    print("Todos los cursos han sido borrados con éxito.")

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    frappe.init(site=site)
    frappe.connect()
    run()
