import os
import sys
import json

# Fix sys.path to avoid shadowing when executing the script directly
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)
apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

import frappe

def run():
    frappe.set_user("Administrator")
    print("Iniciando creación del curso...")

    # Instructor
    instructor_name = "Administrator"

    # Category
    cat_name = "Tecnología y Negocios"
    if not frappe.db.exists("LMS Category", {"category": cat_name}):
        frappe.get_doc({"doctype": "LMS Category", "category": cat_name}).insert(ignore_permissions=True, ignore_mandatory=True)
    
    cat = frappe.get_all("LMS Category", filters={"category": cat_name})
    cat_id = cat[0].name if cat else cat_name

    # Course
    course_title = "IA para Negocios desde Cero"
    if frappe.db.exists("LMS Course", {"title": course_title}):
        course = frappe.get_doc("LMS Course", {"title": course_title})
        print("El curso ya existe. Usando el curso existente.")
    else:
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": course_title,
            "short_introduction": "Aprende a usar la Inteligencia Artificial para resolver problemas de negocio, automatizar tareas y aumentar tus ventas sin conocimientos técnicos.",
            "description": "<p>Bienvenido al curso definitivo de IA para no-programadores. Descubre cómo usar ChatGPT para vender más y trabajar menos.</p>",
            "published": 1,
            "category": cat_id,
            "card_gradient": "Blue",
            "enable_certification": 1
        })
        if instructor_name:
            course.append("instructors", {"instructor": instructor_name})
        course.insert(ignore_permissions=True, ignore_mandatory=True)
        frappe.db.commit()
        print("Curso creado:", course.name)

    course_name = course.name

    # Helper function for chapters
    def create_chapter(title):
        existing = frappe.get_all("Course Chapter", filters={"title": title, "course": course_name})
        if existing:
            return existing[0].name
        doc = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": title,
            "course": course_name
        })
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name

    # Helper function for lessons
    def create_lesson(chap_name, title, body, content=None):
        existing = frappe.get_all("Course Lesson", filters={"title": title, "chapter": chap_name})
        if existing:
            doc = frappe.get_doc("Course Lesson", existing[0].name)
            if content:
                doc.content = content
                doc.body = ""
                doc.save(ignore_permissions=True)
            return existing[0].name
        
        doc = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": title,
            "chapter": chap_name,
            "course": course_name,
            "body": body,
            "content": content
        })
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name

    # Helper function for questions
    def create_question(q_text, opts, explanation_idx):
        existing = frappe.get_all("LMS Question", filters={"question": q_text})
        if existing:
            return existing[0].name
        
        doc = frappe.get_doc({
            "doctype": "LMS Question",
            "question": q_text,
            "type": "Choices",
            "option_1": opts[0], "is_correct_1": 1 if explanation_idx == 0 else 0,
            "option_2": opts[1], "is_correct_2": 1 if explanation_idx == 1 else 0,
            "option_3": opts[2], "is_correct_3": 1 if explanation_idx == 2 else 0,
            "option_4": opts[3], "is_correct_4": 1 if explanation_idx == 3 else 0,
            f"explanation_{explanation_idx+1}": "Esta es la respuesta correcta basada en los principios del curso."
        })
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name

    # Helper function for quizzes
    def create_quiz(title, lesson_name, question_names):
        existing = frappe.get_all("LMS Quiz", filters={"title": title, "lesson": lesson_name})
        if existing:
            return existing[0].name
        doc = frappe.get_doc({
            "doctype": "LMS Quiz",
            "title": title,
            "lesson": lesson_name,
            "passing_percentage": 80,
            "show_answers": 1
        })
        for q in question_names:
            doc.append("questions", {
                "question": q,
                "marks": 1
            })
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        
        # update lesson with quiz_id
        frappe.db.set_value("Course Lesson", lesson_name, "quiz_id", doc.name)
        
        return doc.name

    # Data Structure
    modules = [
        {
            "title": "Módulo 1: Introducción a la IA para negocios",
            "lessons": [
                {
                    "title": "1. Qué es la IA y por qué importa",
                    "body": "### La Inteligencia Artificial hoy\nLa IA generativa (como ChatGPT) no piensa, sino que predice patrones. Es como un superasistente.\n\n**Actividad:** Crea tu cuenta en OpenAI y envíale tu primer mensaje pidiéndole que explique un tema que te guste."
                },
                {
                    "title": "2. Cómo se usa la IA en negocios reales",
                    "body": "### Ejemplos Prácticos\n1. Resumir PDFs largos.\n2. Crear ideas para posts.\n3. Redactar correos difíciles.\n\n**Actividad:** Dile a ChatGPT: 'Tengo un negocio de [tu negocio]. Dime 3 formas en las que puedes ahorrarme tiempo hoy.'"
                }
            ],
            "quiz": {
                "title": "Quiz Módulo 1",
                "questions": [
                    ("¿Qué es la IA generativa?", ["Robots físicos", "Modelos que crean texto/imagen", "Una base de datos de Excel", "Una calculadora"], 1),
                    ("¿Cuál es el mejor uso de ChatGPT en un negocio pequeño?", ["Dejar que atienda el teléfono", "Reemplazar al dueño", "Automatizar redacción y generar ideas", "Lavar los platos"], 2),
                    ("¿ChatGPT 'entiende' o 'adivina' las palabras?", ["Adivina la siguiente palabra más probable", "Entiende todo como un humano", "Busca la respuesta exacta en Google", "Ninguna"], 0),
                    ("¿Cuál es un riesgo de la IA?", ["Que tome el control del mundo mañana", "Que a veces inventa datos (alucinaciones)", "Que no sabe sumar 2+2", "Que es muy cara"], 1),
                    ("¿Para qué NO sirve ChatGPT directamente?", ["Generar ideas", "Hacer café", "Redactar correos", "Traducir textos"], 1)
                ]
            }
        },
        {
            "title": "Módulo 2: Uso de ChatGPT para productividad",
            "lessons": [
                {
                    "title": "3. Qué es un prompt y cómo escribirlo bien",
                    "body": "### La anatomía de un buen Prompt\nRol + Contexto + Tarea + Formato.\nEjemplo: 'Actúa como experto en marketing. Tengo una pizzería (Contexto). Redacta 3 ideas de posts (Tarea) en formato de lista (Formato).'\n\n**Actividad:** Escribe tu primer prompt usando esta fórmula."
                },
                {
                    "title": "4. Prompts para estudiar, vender y organizar",
                    "body": "### Prompts Maestros\nPara estudiar: 'Explícame [tema] como si tuviera 10 años'.\nPara organizar: 'Tengo estas 10 tareas desordenadas. Créame un horario de 9 a 5 priorizando las más urgentes.'\n\n**Actividad:** Pídele a ChatGPT que organice tu día de mañana."
                }
            ],
            "quiz": {
                "title": "Quiz Módulo 2",
                "questions": [
                    ("¿Qué es un prompt?", ["Un virus", "La instrucción o texto que le damos a la IA", "Una marca de computadoras", "Un lenguaje de programación"], 1),
                    ("¿Cuál es la fórmula ideal de un prompt?", ["Rol + Contexto + Tarea + Formato", "Tarea + Por favor + Gracias", "Una palabra clave larga", "Contexto + Saludo + Tarea"], 0),
                    ("Si le digo a ChatGPT 'Actúa como abogado', le estoy dando un...", ["Formato", "Contexto", "Rol", "Tarea"], 2),
                    ("Si ChatGPT me da una mala respuesta, ¿qué debo hacer?", ["Mejorar mi prompt dándole más contexto", "Cerrar la cuenta", "Buscar en Google", "Rendirme"], 0),
                    ("¿En qué formato le puedo pedir resultados a ChatGPT?", ["Tabla", "Lista con viñetas", "Texto continuo", "Todas las anteriores"], 3)
                ]
            }
        },
        {
            "title": "Módulo 3: IA para ventas y marketing",
            "lessons": [
                {
                    "title": "5. Crear ideas de contenido con IA",
                    "body": "### Lluvia de ideas infinita\nPuedes usar IA para que te genere 30 ideas de contenido para redes sociales en 1 minuto. Dile a tu IA quién es tu cliente ideal y pídele problemas frecuentes.\n\n**Actividad:** Pide a la IA 'Dime los 5 problemas más comunes que tiene un comprador de zapatos deportivos'."
                },
                {
                    "title": "6. Mensajes de venta para WhatsApp e Instagram",
                    "body": "### Copywriting persuasivo\nUsa fórmulas como AIDA (Atención, Interés, Deseo, Acción). Pídele a ChatGPT: 'Usa la fórmula AIDA para vender una limpieza dental en WhatsApp.'\n\n**Actividad:** Haz que ChatGPT te escriba un mensaje para recuperar un cliente perdido por WhatsApp."
                }
            ],
            "quiz": {
                    "title": "5. Creando copys persuasivos",
                    "body": "### Fórmula PAS (Problema, Agitación, Solución)\nPídele a la IA que escriba un anuncio usando esta fórmula para tu producto.\n\n**Actividad:** Genera 3 copys para tu negocio.",
                    "assign_type": "Document",
                    "assign_question": "Sube un archivo de texto o Word con los 3 copys que generaste."
                },
                {
                    "title": "6. Cuestionario Módulo 2 y 3",
                    "body": "{{ Quiz(\"Evaluación M2 y M3: Prompts y Ventas\") }}",
                    "quiz": {
                        "title": "Evaluación M2 y M3: Prompts y Ventas",
                        "questions": [
                            {"q": "¿Cuál es la fórmula ideal de un prompt?", "opts": ["Rol + Contexto + Tarea + Formato", "Tarea + Por favor + Gracias", "Contexto + Saludo + Tarea"], "ans": 0},
                            {"q": "¿Qué significa PAS en marketing?", "opts": ["Problema, Agitación, Solución", "Producto, Atención, Servicio", "Precio, Anuncio, Venta"], "ans": 0}
                        ]
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Automatización básica y proyecto final",
            "lessons": [
                {
                    "title": "7. Flujos de trabajo con IA",
                    "body": "### Integrando IA en tu día a día\nNo se trata de usarla una vez, sino de tener la pestaña siempre abierta y delegar: revisión de ortografía, ideación de campañas, respuestas a clientes.\n\n**Actividad:** Diseña un pequeño flujo de 3 pasos para tu próxima promoción.",
                    "assign_type": "Text",
                    "assign_question": "Escribe los 3 pasos de tu flujo de trabajo aquí."
                },
                {
                    "title": "8. Proyecto Final",
                    "body": "### Instrucciones del Proyecto\nSube el documento con tu proyecto final para obtener el certificado.\nInstrucciones: Escribe en un documento PDF o de Word un manual de 1 página explicando 2 tareas que automatizarás con IA en un negocio real o ficticio, y escribe el Prompt Maestro que utilizarías.",
                    "assign_type": "Document",
                    "assign_question": "Sube el documento de tu proyecto final aquí en formato PDF o Word."
                }
            ]
        }
    ]

    # Create Course
    if not frappe.db.exists("LMS Course", course_name):
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "name": course_name,
            "title": course_title,
            "short_introduction": "Aprende a usar la Inteligencia Artificial para resolver problemas de negocio, automatizar tareas y aumentar tus ventas sin conocimientos técnicos.",
            "description": "Bienvenido al curso definitivo de IA para no-programadores. Descubre cómo usar ChatGPT para vender más y trabajar menos.",
            "published": 1,
            "category": category_name
        })
        course.insert(ignore_permissions=True, ignore_mandatory=True)
        course.reload()
    else:
        print("El curso ya existe. Usando el curso existente.")
        course = frappe.get_doc("LMS Course", course_name)
    
    # Verify Instructor is added
    instructor_exists = False
    for i in course.get("instructors"):
        if i.instructor == instructor_name:
            instructor_exists = True
    
    if not instructor_exists:
        course.append("instructors", {"instructor": instructor_name})
        course.save(ignore_permissions=True)

    # Process modules
    course_chapter_names = []
    
    for idx, mod in enumerate(modules, 1):
        c_title = mod["title"]
        
        # Build quizzes if needed
        for les in mod["lessons"]:
            if "quiz" in les:
                les["quiz_name"] = create_quiz(les["quiz"]["title"], les["quiz"]["questions"])

        if frappe.db.exists("Course Chapter", {"title": c_title, "course": course_name}):
            chapter_doc = frappe.get_doc("Course Chapter", {"title": c_title, "course": course_name})
        else:
            chapter_doc = frappe.get_doc({
                "doctype": "Course Chapter",
                "title": c_title,
                "course": course_name,
            })
            chapter_doc.insert(ignore_permissions=True, ignore_mandatory=True)
        
        # Clear existing lessons in the chapter object before rebuilding to avoid duplicates
        chapter_doc.set("lessons", [])
        
        lesson_names = []
        for les in mod["lessons"]:
            l_name = create_lesson(
                chapter_doc.name, 
                les["title"], 
                les["body"], 
                assignment_type=les.get("assign_type"), 
                question=les.get("assign_question", "")
            )
            chapter_doc.append("lessons", {"lesson": l_name})
            lesson_names.append(l_name)
        
        chapter_doc.save(ignore_permissions=True)
        course_chapter_names.append(chapter_doc.name)

    course.reload()
    
    # Clear existing chapters in the course to avoid duplicates
    course.set("chapters", [])
    for c_name in course_chapter_names:
        course.append("chapters", {"chapter": c_name})
        
    course.save(ignore_permissions=True)
            
    frappe.db.commit()
    print("¡Curso IA para Negocios desde Cero importado con éxito!")

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    frappe.init(site=site)
    frappe.connect()
    run()
