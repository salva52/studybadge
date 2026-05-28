import frappe

def force_delete_course():
    course_name = "hotmart-ai-system-automatizaci-n-de-afiliados-de-alto-rendimiento"
    
    print(f"Borrando curso: {course_name} y todas sus dependencias...")
    
    doctypes_to_clear = [
        "LMS Assignment Submission",
        "LMS Quiz Submission",
        "LMS Course Progress",
        "LMS Enrollment",
        "LMS Assignment", 
        "LMS Quiz", 
        "Course Lesson", 
        "Course Chapter"
    ]
    
    for dt in doctypes_to_clear:
        try:
            records = frappe.get_all(dt, filters={"course": course_name})
            for r in records:
                print(f"Borrando {dt} - {r.name}")
                frappe.delete_doc(dt, r.name, force=1)
        except Exception as e:
            # En caso de que algún doctype no tenga campo course o haya un error, continuamos
            pass

    try:
        frappe.delete_doc("LMS Course", course_name, force=1)
        print("¡Curso borrado con éxito!")
    except Exception as e:
        print(f"Error borrando el curso: {e}")
        
    frappe.db.commit()

if __name__ == "__main__":
    force_delete_course()
