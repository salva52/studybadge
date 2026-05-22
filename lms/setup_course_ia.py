import os
import sys

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
    def create_lesson(chap_name, title, body):
        existing = frappe.get_all("Course Lesson", filters={"title": title, "chapter": chap_name})
        if existing:
            return existing[0].name
        doc = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": title,
            "chapter": chap_name,
            "body": body
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
                "title": "Quiz Módulo 3",
                "questions": [
                    ("¿Para qué sirve la IA en Instagram?", ["Dar likes automáticos", "Generar ideas de guiones y copys para posts", "Crear la cuenta sola", "Grabar el video"], 1),
                    ("¿Qué es la fórmula AIDA?", ["Una bebida", "Atención, Interés, Deseo, Acción", "Algoritmo de IA para Datos Activos", "Un software"], 1),
                    ("Al pedirle a ChatGPT un mensaje de WhatsApp para clientes, debes...", ["Pedirle que sea muy largo", "Pedirle que use tono cercano y persuasivo", "Usar lenguaje súper formal y aburrido", "Dejar que escriba 5 páginas"], 1),
                    ("¿Puede la IA crear mi calendario de contenido?", ["No", "Sí, si le das los pilares de contenido", "Sólo si le pagas extra", "Depende del día"], 1),
                    ("La mejor manera de conseguir ideas de contenido es...", ["Decirle 'dame ideas'", "Explicarle quién es tu cliente ideal, sus dolores y pedir ideas", "No usar IA", "Copiar a la competencia"], 1)
                ]
            }
        },
        {
            "title": "Módulo 4: Automatización básica y proyecto final",
            "lessons": [
                {
                    "title": "7. Flujos de trabajo con IA",
                    "body": "### Integrando IA en tu día a día\nNo se trata de usarla una vez, sino de tener la pestaña siempre abierta y delegar: revisión de ortografía, ideación de campañas, respuestas a clientes.\n\n**Actividad:** Diseña un pequeño flujo de 3 pasos para tu próxima promoción."
                },
                {
                    "title": "8. Proyecto Final",
                    "body": "### Instrucciones del Proyecto\nEn la siguiente sección encontrarás la Tarea (Assignment) para subir tu proyecto final y obtener tu certificado. Sigue las instrucciones allí indicadas."
                }
            ]
        }
    ]

    course_chapter_names = []

    for mod in modules:
        c_name = create_chapter(mod["title"])
        course_chapter_names.append(c_name)
        
        chapter_doc = frappe.get_doc("Course Chapter", c_name)
        chapter_doc.set("lessons", [])
        
        lesson_names = []
        for les in mod["lessons"]:
            l_name = create_lesson(c_name, les["title"], les["body"])
            chapter_doc.append("lessons", {"lesson": l_name})
            lesson_names.append(l_name)
        
        chapter_doc.save(ignore_permissions=True)
        
        # Quizzes
        if "quiz" in mod:
            q_names = []
            for q_data in mod["quiz"]["questions"]:
                q_names.append(create_question(q_data[0], q_data[1], q_data[2]))
            
            create_quiz(mod["quiz"]["title"], lesson_names[-1], q_names)
            
    course.reload()
    course.set("chapters", [])
    for c_name in course_chapter_names:
        course.append("chapters", {"chapter": c_name})
        
    course.save(ignore_permissions=True)
            
    # Assignment
    assignment_title = "Propuesta Final: Flujo de IA"
    if not frappe.db.exists("LMS Assignment", {"title": assignment_title, "course": course_name}):
        doc = frappe.get_doc({
            "doctype": "LMS Assignment",
            "title": assignment_title,
            "type": "Document",
            "course": course_name,
            "question": "Escribe en un documento PDF o de Word un manual de 1 página explicando 2 tareas que automatizarás con IA en un negocio real o ficticio, y escribe el Prompt Maestro que utilizarías. Sube el documento aquí."
        })
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
    
    frappe.db.commit()
    print("¡Curso IA para Negocios desde Cero importado con éxito!")

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    frappe.init(site=site)
    frappe.connect()
    run()
