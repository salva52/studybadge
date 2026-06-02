# -*- coding: utf-8 -*-
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

import frappe

courses_to_delete = [
    "aplicaci-n-de-ia-en-educaci-n-y-docencia",
    "b-squeda-de-empleo-y-marca-personal-con-ia",
    "ia-para-educadores-menos-preparaci-n-m-s-inspiraci-n",
    "an-lisis-de-datos-empresariales-con-ia-y-herramientas-no-code"
]

def run():
    frappe.set_user("Administrator")
    print("=======================================")
    print("INICIANDO ELIMINACIÓN DE CURSOS...")
    print("=======================================")
    
    for course_name in courses_to_delete:
        try:
            # Eliminar Lecciones asociadas al curso
            lessons = frappe.get_all("Course Lesson", filters={"course": course_name})
            for l in lessons:
                frappe.delete_doc("Course Lesson", l.name, force=1, ignore_permissions=True)
            
            # Eliminar Capítulos asociados al curso
            chapters = frappe.get_all("Course Chapter", filters={"course": course_name})
            for c in chapters:
                frappe.delete_doc("Course Chapter", c.name, force=1, ignore_permissions=True)
            
            # Eliminar Curso
            if frappe.db.exists("LMS Course", course_name):
                frappe.delete_doc("LMS Course", course_name, force=1, ignore_permissions=True)
                print(f"[EXITO] Curso eliminado: {course_name}")
            else:
                print(f"[INFO] Curso no encontrado: {course_name}")
                
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el curso {course_name}: {e}")

    frappe.db.commit()
    print("=======================================")
    print("PROCESO TERMINADO")
    print("=======================================")

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    try:
        frappe.init(site=site)
        frappe.connect()
        run()
    except Exception as e:
        print("Error de conexion:", e)
    finally:
        frappe.destroy()
