# -*- coding: utf-8 -*-
"""
Curso generado para Frappe Learning / Frappe LMS por StudyBadge.

Uso desde frappe-bench:
    python apps/lms/setup_course_generated.py studybadge.localhost

Notas:
- Script idempotente: si lo ejecutas varias veces, actualiza en lugar de duplicar.
- Usa Course Lesson.content con bloques EditorJS para renderizar texto, imágenes, quizzes y assignments.
"""

import os
import sys
import json
import time
import re
import mimetypes
import traceback
from urllib.parse import urlparse

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

import frappe
import requests
from frappe.utils.file_manager import save_file

INSTRUCTOR_NAME = "Administrator"
COURSE_DATA = {
    "category": "Marketing",
    "title": "Despegue Digital: Consigue tus Primeros Clientes en 5 Pasos",
    "short_introduction": "La ruta exacta y sin rodeos técnicos para activar tu marketing digital, atraer prospectos calificados y cerrar ventas desde hoy.",
    "description": "<p>Olvídate de la teoría abrumadora y de configurar herramientas complejas. Este curso ultra práctico está diseñado para que pases a la acción de inmediato con un método directo, probado y enfocado en resultados.</p><ul><li><strong>Oferta irresistible:</strong> Diseñarás una propuesta de valor tan clara que tu cliente ideal no podrá ignorar.</li><li><strong>Canal de ventas express:</strong> Activarás un puente directo de comunicación en cuestión de minutos.</li><li><strong>Cierre de ventas natural:</strong> Aprenderás a guiar la conversación por chat para concretar ventas sin presionar.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y sumamente práctica. Prioriza la aplicación real, la claridad de la propuesta, la empatía con el cliente y la coherencia comercial antes que la perfección técnica. Valora respuestas directas, sin rodeos, con ejemplos específicos y realistas del negocio. Penaliza respuestas vacías, redundantes, incoherentes, teóricas o excesivamente genéricas (como 'público general de 18 a 99 años'). Al final, asigna una nota del 1 al 10. Escala: 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Estructura siempre tu evaluación indicando: Puntos fuertes, Aspectos a mejorar, Nota final y Estado (Aprobado si es 7 o más, Desaprobado si es menor a 7).",
    "chapters": [
        {
            "title": "Módulo 1: Tu Oferta Irresistible",
            "lessons": [
                {
                    "title": "Redacta tu propuesta de valor en una sola frase potente",
                    "objective": "Construir una propuesta de valor clara, directa y concisa que comunique qué problema resuelves y para quién, lista para usar en tus canales digitales.",
                    "sections": [
                        {
                            "heading": "El peligro de la confusión",
                            "paragraphs": [
                                "Si un cliente potencial entra a tu perfil de redes sociales o sitio web y tiene que esforzarse para entender qué vendes, se irá de inmediato con la competencia. En internet, la claridad supera al diseño y a la persuasión.",
                                "Para vender no necesitas discursos largos ni términos técnicos complejos. Necesitas que cualquier persona entienda el valor de tu negocio en menos de cinco segundos."
                            ]
                        },
                        {
                            "heading": "La fórmula de la propuesta de valor",
                            "paragraphs": [
                                "Tu propuesta de valor es el gancho que capta la atención del cliente ideal. Para construirla sin complicaciones, utilizaremos una fórmula directa:",
                                "\"Ayudo a [Cliente ideal] a conseguir [Resultado deseado] mediante [Tu método o servicio] sin tener que pasar por [Su mayor frustración].\"",
                                "Cada ingrediente tiene una función: el 'Cliente ideal' delimita a quién le hablas; el 'Resultado deseado' es el beneficio real que compra la persona; tu 'Método' es el vehículo; y el 'Sin frustración' elimina el principal obstáculo o miedo que frena la compra."
                            ]
                        },
                        {
                            "heading": "Análisis de un caso real",
                            "paragraphs": [
                                "Imagina a un entrenador personal. En lugar del típico mensaje aburrido: 'Ofrezco planes de entrenamiento y nutrición personalizados', la fórmula transforma su mensaje en algo magnético:",
                                "'Ayudo a profesionales ocupados a recuperar su energía y perder peso mediante entrenamientos de 20 minutos en casa y sin hacer dietas restrictivas'.",
                                "Este segundo mensaje habla directamente a un dolor específico (falta de tiempo, miedo a pasar hambre) y vende un destino claro, no solo el proceso."
                            ]
                        },
                        {
                            "heading": "Errores críticos a evitar",
                            "paragraphs": [
                                "El error más común es usar frases corporativas vacías como 'Ofrecemos soluciones integrales de alta calidad'. Esto no significa nada para el consumidor. La gente no busca 'soluciones integrales', busca resolver un problema específico.",
                                "Otro gran error es enfocarse en las características físicas de lo que entregas (ej. 'Curso de 15 módulos') en lugar del beneficio real (ej. 'Habla inglés con seguridad en tu próxima reunión laboral'). Recuerda: el cliente compra el destino, no el boleto de avión."
                            ]
                        },
                        {
                            "heading": "Acción inmediata",
                            "paragraphs": [
                                "Una propuesta de valor efectiva elimina la fricción y acelera la decisión de compra.",
                                "Tu tarea de hoy: Toma papel y lápiz, completa los campos de la fórmula de la lección y escribe tu propuesta en una sola línea. Mantenla simple, directa y libre de tecnicismos."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu propuesta de valor en una sola frase",
                        "questions": [
                            {
                                "question": "¿Cuál es uno de los errores más graves al presentar tu propuesta de valor?",
                                "options": [
                                    "Intentar venderle a todo el mundo usando frases vacías como 'soluciones integrales'.",
                                    "No incluir enlaces directos a todas tus redes sociales en la biografía.",
                                    "Utilizar imágenes en lugar de un texto largo y detallado.",
                                    "Ofrecer un método de pago que no sea de entrega inmediata."
                                ],
                                "answer": 0,
                                "explanation": "Las frases genéricas y vacías no resuelven problemas concretos. El cliente busca soluciones específicas a dolores específicos."
                            },
                            {
                                "question": "En la fórmula de la propuesta de valor, ¿qué representa la sección del 'sin' (sin tener que pasar por)?",
                                "options": [
                                    "La garantía de reembolso si el cliente no está satisfecho.",
                                    "La mayor frustración, miedo o pereza que tu cliente quiere evitar a toda costa.",
                                    "El coste económico que el cliente se va a ahorrar.",
                                    "Los competidores directos con los que el cliente no quiere trabajar."
                                ],
                                "answer": 1,
                                "explanation": "El 'sin' desactiva la principal objeción o dolor del cliente, reduciendo la resistencia mental para comprar."
                            },
                            {
                                "question": "Bajo la premisa de que 'la gente compra el destino, no el viaje', ¿cuál describe un beneficio real?",
                                "options": [
                                    "Un curso online estructurado en 15 módulos con PDFs.",
                                    "Aprender a hablar inglés con soltura en tus reuniones de trabajo.",
                                    "Recibir sesiones de videollamada de 60 minutos semanales.",
                                    "Un manual técnico de 100 páginas de descarga inmediata."
                                ],
                                "answer": 1,
                                "explanation": "Hablar inglés con soltura en el trabajo es el resultado final (el destino) que el cliente desea experimentar."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña tu Propuesta de Valor Irresistible",
                        "type": "Text",
                        "question": "<p>¡Es hora de pasar a la acción! Redacta la frase que definirá tu negocio y captará la atención de tus clientes en segundos. Puedes usar tu negocio real o un proyecto ficticio.</p><p>Escribe tu respuesta completando los siguientes tres pasos:</p><ol><li><strong>Paso 1: Define tus 4 ingredientes clave</strong><ul><li><strong>Cliente ideal:</strong> ¿A quién te diriges específicamente?</li><li><strong>Resultado deseado:</strong> ¿Qué beneficio tangible consiguen contigo?</li><li><strong>Tu método:</strong> ¿A través de qué vehículo o servicio lo logran?</li><li><strong>Mayor frustración:</strong> ¿Qué molestia o miedo quieren evitar a toda costa?</li></ul></li><li><strong>Paso 2: Construye tu frase final</strong><br />Une los ingredientes usando la estructura exacta: <em>\"Ayudo a [Cliente ideal] a [Resultado deseado] a través de [Tu método] sin [Mayor frustración]\".</em></li><li><strong>Paso 3: Tu autoevaluación exprés</strong><br />Explica en una sola frase por qué esta propuesta es fácil de entender y por qué el dolor que eliminas (\"sin...\") es atractivo para tu cliente.</li></ol>"
                    },
                    "image": {
                        "url": "https://images.unsplash.com/photo-1533749871411-5e21e14bcc7d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5NjQ0NzR8MHwxfHNlYXJjaHwyMHx8ZW50cmVwcmVuZXVyJTIwcGxhbm5pbmclMjBicmFuZGluZyUyMHN0cmF0ZWd5JTIwd2hpdGVib2FyZHxlbnwxfDB8fHwxNzgwMDg5Mjk5fDA&ixlib=rb-4.1.0&q=80&w=1080",
                        "local_url": "",
                        "caption": "Foto de Campaign Creators en Unsplash",
                        "alt": "man writing on whiteboard",
                        "source": "Unsplash",
                        "provider": "Unsplash API",
                        "source_url": "https://unsplash.com/photos/man-writing-on-whiteboard-8F4EX4Nw1yY",
                        "photographer": "Campaign Creators",
                        "license": "Unsplash License",
                        "image_type": "photo",
                        "query": "entrepreneur planning branding strategy whiteboard"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: Tu Cliente Ideal al Grano",
            "lessons": [
                {
                    "title": "Define el perfil de tu comprador respondiendo 3 preguntas clave",
                    "objective": "Identificar con precisión al comprador ideal de tu producto o servicio para estructurar mensajes de marketing altamente efectivos.",
                    "sections": [
                        {
                            "heading": "El error de hablarle a todos",
                            "paragraphs": [
                                "Intentar venderle a \"cualquiera\" es el camino más rápido para no venderle a nadie. En el entorno digital, el éxito no depende de presupuestos millonarios, sino de la hiper-especificidad.",
                                "Olvídate de los manuales complejos de investigación de mercados. Para arrancar hoy, solo necesitas entender los disparadores psicológicos de la persona que tiene la tarjeta en la mano lista para comprarte."
                            ]
                        },
                        {
                            "heading": "Las 3 preguntas de oro",
                            "paragraphs": [
                                "Define el perfil de tu comprador ideal respondiendo estas tres preguntas clave:",
                                "1. ¿Quién es y qué situación vive?: Ve más allá de la edad o el género. Enfócate en su estilo de vida o rol profesional. ¿Es un emprendedor solitario sobrecargado? ¿Es una madre trabajadora buscando optimizar su tiempo?",
                                "2. ¿Cuál es su mayor frustración?: Identifica qué le quita el sueño en relación con lo que vendes. Si vendes comida saludable, su dolor no es la falta de verduras, sino la culpa de comer mal por falta de tiempo para cocinar.",
                                "3. ¿Qué beneficio urgente busca?: ¿Cuál es la transformación inmediata que desea experimentar? Enfócate en el alivio, ahorro de tiempo o estatus que genera tu solución."
                            ]
                        },
                        {
                            "heading": "Caso de estudio express",
                            "paragraphs": [
                                "Supongamos que ofreces servicios de organización y limpieza profesional de hogares. En lugar de definir a tu cliente como 'dueños de casas', responde las preguntas:",
                                "- ¿Quién es?: Profesionales con mascotas que trabajan más de 10 horas al día fuera de casa.",
                                "- ¿Su mayor frustración?: Llegar agotados el viernes por la noche y pasar su único fin de semana limpiando en lugar de descansar.",
                                "- ¿Su beneficio urgente?: Disfrutar de un hogar impecable para relajarse de verdad sin mover un solo dedo.",
                                "Con este perfil, tu publicidad no dirá 'Servicio de limpieza'. Dirá: 'Recupera tus fines de semana. Nosotros limpiamos, tú descansas'."
                            ]
                        },
                        {
                            "heading": "El miedo a excluir",
                            "paragraphs": [
                                "Muchos emprendedores temen que al segmentar perderán clientes. La realidad es la opuesta: cuando intentas agradar a todos, tu comunicación se vuelve tibia, genérica y aburrida.",
                                "La especialización genera conexión. Cuando un cliente lee un mensaje que describe exactamente su situación actual, siente que el producto fue diseñado exclusivamente para él."
                            ]
                        },
                        {
                            "heading": "Acción inmediata",
                            "paragraphs": [
                                "Definir a tu comprador ideal requiere empatía, no herramientas costosas.",
                                "Tu tarea de hoy: Responde las 3 preguntas doradas para tu negocio en un párrafo corto. No te compliques con biografías largas; busca la esencia del problema que resuelves."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Define el perfil de tu comprador ideal",
                        "questions": [
                            {
                                "question": "¿Por qué es un grave error intentar venderle a 'cualquiera' en internet?",
                                "options": [
                                    "Porque tu mensaje se vuelve genérico, aburrido y diluye la efectividad de la comunicación.",
                                    "Porque las redes sociales bloquean las cuentas que no definen un público objetivo exacto.",
                                    "Porque necesitas un presupuesto millonario para poder configurar las herramientas de publicidad.",
                                    "Porque los clientes prefieren comprarle únicamente a multinacionales con estudios de mercado complejos."
                                ],
                                "answer": 0,
                                "explanation": "El mensaje genérico no resuena con nadie. La especificidad genera conexión inmediata y relevancia."
                            },
                            {
                                "question": "Al responder a la pregunta '¿Quién es y qué situación vive?', ¿cuál debe ser tu enfoque?",
                                "options": [
                                    "Únicamente en datos demográficos tradicionales como la edad, el género y la ubicación geográfica.",
                                    "En su estilo de vida, retos cotidianos y su situación actual.",
                                    "En adivinar sus gustos basándote exclusivamente en lo que a ti te gusta de tu propio producto.",
                                    "En crear una lista de todas las características técnicas del servicio que le vas a ofrecer."
                                ],
                                "answer": 1,
                                "explanation": "El estilo de vida y la situación actual determinan los hábitos de compra y los problemas reales del cliente."
                            },
                            {
                                "question": "¿Qué error provoca habitualmente el miedo a excluir a clientes potenciales?",
                                "options": [
                                    "Redactar mensajes de venta demasiado específicos que solo entiende un grupo muy pequeño de personas.",
                                    "Utilizar las propias palabras del cliente para describir sus preocupaciones cotidianas.",
                                    "Crear un mensaje de venta tan genérico que nadie se siente aludido.",
                                    "Definir el perfil del comprador en menos de 10 minutos usando una hoja de papel."
                                ],
                                "answer": 2,
                                "explanation": "Por intentar abarcar demasiado, la propuesta se vuelve invisible y pierde fuerza persuasiva."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: La Ficha de tu Cliente Ideal en 3 Preguntas",
                        "type": "Text",
                        "question": "<p>Define el perfil del comprador que estará feliz de adquirir tu solución. Copia y completa la siguiente plantilla en el cuadro de respuesta:</p><ol><li><strong>Mi producto/servicio es:</strong> [Describe brevemente qué vendes]</li><li><strong>¿Quién es y qué situación vive?:</strong> [Define su estilo de vida o situación profesional en una frase directa]</li><li><strong>¿Cuál es su mayor dolor o frustración?:</strong> [Qué molestia o preocupación real experimenta en su día a día]</li><li><strong>¿Qué beneficio urgente busca conseguir?:</strong> [Qué alivio o meta tangible quiere lograr]</li><li><strong>Mensaje de venta gancho:</strong> [Redacta una frase corta de impacto que conecte su dolor con tu solución]</li></ol>"
                    },
                    "image": {
                        "url": "https://images.unsplash.com/photo-1512758017271-d7b84c2113f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5NjQ0NzR8MHwxfHNlYXJjaHw0fHx1c2VyJTIwcGVyc29uYSUyMGNhbnZhcyUyMHN0aWNreSUyMG5vdGVzfGVufDF8MHx8fDE3ODAwODkzMDd8MA&ixlib=rb-4.1.0&q=80&w=1080",
                        "local_url": "",
                        "caption": "Foto de Daria Nepriakhina 🇺🇦 en Unsplash",
                        "alt": "printed sticky notes glued on board",
                        "source": "Unsplash",
                        "provider": "Unsplash API",
                        "source_url": "https://unsplash.com/photos/printed-sticky-notes-glued-on-board-zoCDWPuiRuA",
                        "photographer": "Daria Nepriakhina 🇺🇦",
                        "license": "Unsplash License",
                        "image_type": "photo",
                        "query": "user persona canvas sticky notes"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: Tu Canal de Ventas Express",
            "lessons": [
                {
                    "title": "Crea tu Enlace de WhatsApp: Tu Canal de Ventas en 3 Minutos",
                    "objective": "Configurar y activar un enlace de WhatsApp personalizado con un mensaje predefinido para facilitar el contacto inmediato de tus clientes.",
                    "sections": [
                        {
                            "heading": "La simplicidad vende",
                            "paragraphs": [
                                "Para conseguir tus primeros clientes no necesitas una tienda online sofisticada, pasarelas de pago integradas ni flujos técnicos complejos. Solo necesitas un canal directo para conversar.",
                                "Ese canal es WhatsApp, una aplicación que tus clientes ya usan a diario. Al eliminar barreras de entrada y permitir una comunicación instantánea, aceleras radicalmente la confianza y la decisión de compra."
                            ]
                        },
                        {
                            "heading": "Qué es un enlace directo y cómo funciona",
                            "paragraphs": [
                                "Un enlace directo (link de API de WhatsApp) abre un chat inmediato con tu número al hacer un solo clic, sin que el usuario tenga que guardarte en sus contactos.",
                                "Utilizando herramientas gratuitas como 'Walink' (create.wa.link), puedes generar este enlace e incluir un texto predefinido que el cliente enviará de inmediato.",
                                "Este texto previo debe estructurarse estratégicamente para indicarte exactamente qué producto o servicio le interesa al cliente, rompiendo el hielo de forma natural."
                            ]
                        },
                        {
                            "heading": "Ejemplo en acción",
                            "paragraphs": [
                                "Imagina que eres Laura, mentora de negocios. En lugar de publicar en tus redes 'Escríbeme al +54 9 11...', Laura comparte un enlace personalizado.",
                                "El enlace tiene el mensaje: 'Hola Laura, quiero agendar mi sesión de diagnóstico gratuita'. Cuando el interesado hace clic, el chat se abre con esa frase lista para enviar. Laura recibe el mensaje, conoce el interés exacto del cliente y puede iniciar la venta de inmediato."
                            ]
                        },
                        {
                            "heading": "Obstáculos de fricción",
                            "paragraphs": [
                                "El error más grave es obligar al cliente a copiar tu número, abrir la agenda de su teléfono, guardarte, buscarte en WhatsApp y escribir el primer mensaje. Cada paso extra reduce tu tasa de conversión a la mitad.",
                                "No dejes el mensaje predeterminado vacío o con un simple 'Hola'. Ayuda al prospecto redactando el inicio de la conversación por él."
                            ]
                        },
                        {
                            "heading": "Acción inmediata",
                            "paragraphs": [
                                "Un enlace de WhatsApp optimizado reduce la fricción del proceso comercial al mínimo.",
                                "Tu tarea de hoy: Entra a create.wa.link, ingresa tu número con el código internacional de tu país, redacta un mensaje inicial específico y genera tu enlace. Guárdalo en las notas de tu teléfono para tenerlo siempre a la mano."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu Canal de Ventas en 3 Minutos",
                        "questions": [
                            {
                                "question": "¿Cuál es la principal ventaja de utilizar un enlace directo de WhatsApp?",
                                "options": [
                                    "Permite que tus clientes te contacten con un solo clic y sin necesidad de guardar tu número en su agenda.",
                                    "Reemplaza la necesidad de tener un producto o servicio definido para empezar a vender.",
                                    "Te ayuda a diseñar una página web compleja y un carrito de compras interactivo.",
                                    "Envía de forma automática mensajes de cobro a todos tus contactos guardados."
                                ],
                                "answer": 0,
                                "explanation": "El enlace directo elimina la fricción del proceso, permitiendo al usuario iniciar la conversación de manera instantánea."
                            },
                            {
                                "question": "Según la lección, ¿cuál es un error grave al publicar tus datos de contacto?",
                                "options": [
                                    "Utilizar herramientas gratuitas en línea como 'Walink' para generar tus enlaces.",
                                    "Guardar el enlace generado en las notas de tu celular.",
                                    "Publicar tu número de teléfono suelto en tus publicaciones en lugar de un enlace clickable.",
                                    "Configurar un mensaje automático que mencione el nombre de tu producto."
                                ],
                                "answer": 2,
                                "explanation": "Publicar el número suelto obliga al usuario a realizar múltiples pasos manuales, lo que incrementa el abandono."
                            },
                            {
                                "question": "¿Por qué es fundamental configurar un mensaje de texto predeterminado en el enlace?",
                                "options": [
                                    "Porque le facilita al cliente iniciar la charla y a ti te ayuda a saber de inmediato qué producto o servicio le interesa.",
                                    "Porque WhatsApp cobra una tarifa adicional si no configuras un mensaje predeterminado.",
                                    "Porque así el cliente no tiene que presionar el botón de enviar en su teléfono.",
                                    "Porque es obligatorio para que el generador 'create.wa.link' pueda funcionar."
                                ],
                                "answer": 0,
                                "explanation": "El mensaje predeterminado reduce la incertidumbre del cliente sobre cómo empezar y te da contexto comercial inmediato."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: Tu Puente de Ventas en Un Clic",
                        "type": "Text",
                        "question": "<p>Activa el canal de entrada a tu negocio creando un enlace personalizado. Sigue estos pasos:</p><ol><li><strong>Define tu oferta:</strong> ¿Qué producto o servicio específico vas a promover hoy?</li><li><strong>Diseña tu mensaje:</strong> Redacta el mensaje automático que tu cliente enviará con un clic (debe ser específico y cercano).</li><li><strong>Genera el link:</strong> Entra a <a href=\"https://create.wa.link\" target=\"_blank\">create.wa.link</a>, introduce tu número de teléfono y el mensaje diseñado, y genera el enlace.</li></ol><p><strong>Entrega tu respuesta con la siguiente estructura:</strong></p><ul><li><strong>Producto/Servicio:</strong> [Nombre de tu oferta]</li><li><strong>Mensaje Automático:</strong> [El texto exacto configurado]</li><li><strong>Enlace Generado:</strong> [Pega tu enlace de wa.link real o simulado para la práctica]</li></ul>"
                    },
                    "image": {
                        "url": "https://images.unsplash.com/photo-1682941664177-7920d0e59418?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5NjQ0NzR8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjB0YXBwaW5nJTIwc21hcnRwaG9uZSUyMHNjcmVlbiUyMHNob3dpbmclMjBjaGF0JTIwaW50ZXJmYWNlfGVufDF8MHx8fDE3ODAwODkzMTV8MA&ixlib=rb-4.1.0&q=80&w=1080",
                        "local_url": "",
                        "caption": "Foto de Sanket Mishra en Unsplash",
                        "alt": "a person holding a cell phone with a chat app on the screen",
                        "source": "Unsplash",
                        "provider": "Unsplash API",
                        "source_url": "https://unsplash.com/photos/a-person-holding-a-cell-phone-with-a-chat-app-on-the-screen-qAKPcrIcRG8",
                        "photographer": "Sanket Mishra",
                        "license": "Unsplash License",
                        "image_type": "photo",
                        "query": "person tapping smartphone screen showing chat interface"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Tu Imán de Prospectos",
            "lessons": [
                {
                    "title": "Crea tu primera publicación de alto impacto con una plantilla probada",
                    "objective": "Redactar y estructurar una publicación atractiva y persuasiva para redes sociales orientada a capturar leads de forma orgánica.",
                    "sections": [
                        {
                            "heading": "El arte de llamar la atención",
                            "paragraphs": [
                                "No necesitas ser un redactor profesional para captar prospectos calificados. Las publicaciones de alto rendimiento no dependen de la inspiración, sino de aplicar estructuras validadas de comunicación.",
                                "Hoy aprenderás a diseñar un post optimizado para que tu audiencia levante la mano de inmediato y te diga: 'Me interesa saber más'."
                            ]
                        },
                        {
                            "heading": "La estructura Gancho - Valor - Acción",
                            "paragraphs": [
                                "Para que un post orgánico funcione, debe integrar tres elementos indispensables de forma secuencial:",
                                "1. El Gancho (Hook): Una frase o pregunta inicial que detenga el scroll del usuario en su pantalla atacando directamente un dolor o deseo.",
                                "2. El Valor (Value): Presenta un recurso gratuito (guía, plantilla, mini-auditoría) que actúe como solución inmediata y demuestre tu autoridad.",
                                "3. El Llamado a la Acción (CTA): Una instrucción ultra simple donde indiques exactamente qué palabra clave deben comentar para recibir el recurso."
                            ]
                        },
                        {
                            "heading": "Ejemplo de plantilla de alto impacto",
                            "paragraphs": [
                                "Esta es una plantilla lista para adaptar a tu sector:",
                                "\"¿[Pregunta directa sobre el dolor del cliente]? He creado una guía corta donde te enseño a [Resultado deseado] sin [Dolor principal]. Si la quieres gratis, escribe la palabra [PALABRA_CLAVE] en los comentarios y te la envío por privado hoy mismo.\"",
                                "Por ejemplo, para un asesor de finanzas personales: '¿Sientes que tu sueldo desaparece a mitad de mes? Diseñé una plantilla de control de gastos en Excel que se llena en 3 minutos al día sin recortar tus gustos. Si la quieres gratis, comenta la palabra CONTROL y te la mando de inmediato por mensaje directo'."
                            ]
                        },
                        {
                            "heading": "El error de vender antes de tiempo",
                            "paragraphs": [
                                "El error más común es intentar vender tu servicio de pago de entrada en este tipo de publicación. En redes, primero construyes confianza aportando valor gratuito; la venta del servicio principal se realiza en privado.",
                                "Otro error es no dar instrucciones claras. Si solo pones un link o dejas el post abierto, el usuario dará 'me gusta' y continuará navegando sin interactuar."
                            ]
                        },
                        {
                            "heading": "Acción inmediata",
                            "paragraphs": [
                                "Un post magnético atrae prospectos calificados filtrando de inmediato a quienes realmente sufren el problema que resuelves.",
                                "Tu tarea de hoy: Adapta la plantilla del ejemplo a tu nicho, define una palabra clave directa en mayúsculas y ten listo tu texto para publicar en tus redes sociales."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Crea tu primera publicación de alto impacto",
                        "questions": [
                            {
                                "question": "¿Cuáles son los tres pasos esenciales de una publicación para atraer prospectos?",
                                "options": [
                                    "Introducción formal, testimonios de clientes y precio de tu servicio.",
                                    "El Gancho, el Valor y el Llamado a la Acción.",
                                    "Una historia personal, tu propuesta de venta directa y un enlace de pago.",
                                    "Una imagen llamativa, hashtags populares y un saludo de bienvenida."
                                ],
                                "answer": 1,
                                "explanation": "El Gancho capta la atención, el Valor demuestra tu capacidad de resolver el problema y el Llamado a la Acción genera el contacto directo."
                            },
                            {
                                "question": "Según la lección, ¿cuál es el error más grave al hacer esta publicación?",
                                "options": [
                                    "Intentar vender tu servicio de pago directamente en el post.",
                                    "No incluir imágenes de alta calidad o diseñadas por profesionales.",
                                    "Escribir un texto de más de tres párrafos de extensión.",
                                    "Publicar el mensaje en más de una red social el mismo día."
                                ],
                                "answer": 0,
                                "explanation": "Vender directamente ahuyenta a los usuarios fríos. Primero se genera confianza entregando valor gratuito."
                            },
                            {
                                "question": "¿Por qué debes pedir a los usuarios que comenten una palabra clave específica?",
                                "options": [
                                    "Para que la red social traduzca automáticamente tu mensaje a otros idiomas.",
                                    "Para dar una instrucción clara y evitar que la gente solo le dé 'me gusta' y siga de largo.",
                                    "Para obligar a los usuarios a registrarse en tu sitio web de inmediato.",
                                    "Para demostrarle a la plataforma que tienes una cuenta muy popular."
                                ],
                                "answer": 1,
                                "explanation": "Las instrucciones de un solo paso facilitan la acción del usuario, incrementando la participación exponencialmente."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña tu primera publicación magnética",
                        "type": "Text",
                        "question": "<p>Escribe la publicación exacta que subirás a tus redes sociales para captar interesados.</p><p>Completa la siguiente estructura en el cuadro de texto:</p><ol><li><strong>Nicho o Negocio:</strong> [Ej: Consultoría contable, Diseño de marca, etc.]</li><li><strong>Recurso Gratuito (Imán):</strong> [Ej: PDF con 5 deducciones de impuestos legales / Checklist de identidad visual]</li><li><strong>Texto Final del Post:</strong> [Redacta el post completo uniendo el Gancho, el Valor y tu Llamado a la Acción con su palabra clave en mayúsculas]</li></ol>"
                    },
                    "image": {
                        "url": "https://images.unsplash.com/photo-1644771571408-f2b3b8782f41?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5NjQ0NzR8MHwxfHNlYXJjaHwxN3x8ZGVzaWduZXIlMjBlZGl0aW5nJTIwc29jaWFsJTIwbWVkaWElMjBwb3N0JTIwdGVtcGxhdGV8ZW58MXwwfHx8MTc4MDA4OTMyNHww&ixlib=rb-4.1.0&q=80&w=1080",
                        "local_url": "",
                        "caption": "Foto de Zhivko Minkov en Unsplash",
                        "alt": "an open laptop computer sitting next to a cell phone",
                        "source": "Unsplash",
                        "provider": "Unsplash API",
                        "source_url": "https://unsplash.com/photos/an-open-laptop-computer-sitting-next-to-a-cell-phone-dGS86Zc-zBM",
                        "photographer": "Zhivko Minkov",
                        "license": "Unsplash License",
                        "image_type": "photo",
                        "query": "designer editing social media post template"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: El Cierre de Ventas Fácil",
            "lessons": [
                {
                    "title": "Cierra ventas por chat con el guion de los 3 pasos",
                    "objective": "Aplicar una metodología de comunicación de 3 pasos por chat para convertir consultas informativas en ventas cerradas.",
                    "sections": [
                        {
                            "heading": "Conversar para convertir",
                            "paragraphs": [
                                "Cuando un cliente potencial llega a tu WhatsApp, la venta está a medio camino. Sin embargo, muchos emprendedores pierden la oportunidad al no saber cómo reaccionar cuando les preguntan el precio directamente.",
                                "Cerrar ventas por chat no se trata de presionar ni de enviar textos interminables. Se trata de escuchar, guiar y facilitar la decisión de compra con naturalidad."
                            ]
                        },
                        {
                            "heading": "El guion de los 3 pasos",
                            "paragraphs": [
                                "Estructura tus conversaciones de venta utilizando estas tres etapas claras:",
                                "Paso 1: Conectar y Calificar. No des el precio de inmediato. Haz una pregunta sencilla para conocer la necesidad real del cliente. Esto demuestra profesionalismo y baja las defensas del prospecto.",
                                "Paso 2: Presentar la Solución Vinculada + Precio. Presenta tu oferta relacionándola directamente con la necesidad que te acaba de confesar, y menciona el precio con total seguridad.",
                                "Paso 3: Llamado a la Acción Directo (CTA). Finaliza siempre con una pregunta cerrada de doble opción para guiar al cliente al pago, envío o agendamiento, evitando dejar la conversación en el aire."
                            ]
                        },
                        {
                            "heading": "El guion aplicado al mundo real",
                            "paragraphs": [
                                "Imagina que vendes pastelería saludable por chat y un usuario te escribe: 'Hola, ¿precio de la tarta de chocolate?':",
                                "- Paso 1 (Conectar): '¡Hola! Claro que sí, es nuestra tarta estrella. Para poder recomendarte el tamaño ideal, ¿es para un evento especial o para compartir en casa?'. El cliente responde: 'Es para el cumpleaños de mi pareja, somos 6 personas y él es intolerante al gluten'.",
                                "- Paso 2 (Solución + Precio): '¡Excelente! Para 6 personas te recomiendo la de tamaño mediano sin gluten, elaborada con harina de almendras premium. Queda súper húmeda y deliciosa. El precio es de $28'.",
                                "- Paso 3 (CTA): '¿La necesitarías para el sábado en la mañana o en la tarde para programar tu entrega?'"
                            ]
                        },
                        {
                            "heading": "Errores letales de comunicación",
                            "paragraphs": [
                                "Responder solo el precio (ej. '$28') convierte tu producto en un simple commodity y detiene la conversación en el acto. Tampoco envíes enormes testamentos de texto con especificaciones técnicas irrelevantes; mantén tus mensajes breves, legibles y conversacionales."
                            ]
                        },
                        {
                            "heading": "Acción inmediata",
                            "paragraphs": [
                                "Un buen proceso de venta por chat acompaña al cliente en su decisión sin resultar invasivo.",
                                "Tu tarea de hoy: Redacta tus plantillas para los tres pasos adaptándolas al producto o servicio que promueves y guárdalas para usarlas en tus próximas conversaciones de WhatsApp."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Domina el cierre de ventas por chat",
                        "questions": [
                            {
                                "question": "¿En qué consiste el primer paso del guion de cierre y qué debes evitar?",
                                "options": [
                                    "En Conectar y Calificar al cliente, evitando darle el precio de inmediato para entender primero su necesidad real.",
                                    "En presentar el precio con descuento, evitando hacer preguntas para no incomodar al cliente.",
                                    "En enviar el catálogo completo, evitando que el cliente tenga que preguntar por otros productos.",
                                    "En convencer al cliente con un discurso agresivo, evitando que cambie de opinión de inmediato."
                                ],
                                "answer": 0,
                                "explanation": "Calificar primero te permite adaptar tus argumentos a los dolores del cliente, incrementando el valor percibido."
                            },
                            {
                                "question": "De acuerdo con la lección, ¿cuáles son los errores más comunes al vender por chat?",
                                "options": [
                                    "Hacer preguntas cortas al inicio y dar opciones de entrega muy variadas.",
                                    "Ofrecer demasiadas opciones de pago y responder usando notas de voz.",
                                    "Responder únicamente con el precio de inmediato y enviar textos gigantescos con detalles técnicos no solicitados.",
                                    "Saludar de manera amigable y dar un seguimiento al día siguiente del primer contacto."
                                ],
                                "answer": 2,
                                "explanation": "Dar solo el precio destruye el valor de tu oferta, y los textos excesivamente largos abruman al comprador."
                            },
                            {
                                "question": "¿Cómo debe ser el Llamado a la Acción Directo (Paso 3) para cerrar la venta?",
                                "options": [
                                    "Debe ser una frase abierta como 'me avisas', dejando la decisión de escribirte de nuevo del lado del cliente.",
                                    "Debe ser una pregunta de cierre fácil de responder que guíe al cliente de forma natural al siguiente paso.",
                                    "Debe ser una solicitud de depósito inmediato sin haber acordado la fecha de entrega.",
                                    "Debe ser una lista con todas las formas de pago disponibles y sus respectivas comisiones."
                                ],
                                "answer": 1,
                                "explanation": "El cierre de doble alternativa o de confirmación sencilla facilita que el cliente tome el siguiente paso de manera natural."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Guion de Cierre de 3 Pasos",
                        "type": "Text",
                        "question": "<p>Crea tu propia plantilla de respuesta por chat para gestionar de manera efectiva las consultas de tus clientes.</p><p>Completa los siguientes puntos detallando los mensajes exactos que enviarías:</p><ol><li><strong>Mi Negocio o Producto:</strong> [¿Qué vendes?]</li><li><strong>Mensaje para Conectar y Calificar (Paso 1):</strong> [¿Qué pregunta de diagnóstico harás tras saludar?]</li><li><strong>Mensaje de Solución Vinculada + Precio (Paso 2):</strong> [¿Cómo presentarías la solución y el precio según lo que el cliente te responda?]</li><li><strong>Mensaje de Cierre (Paso 3):</strong> [¿Qué pregunta de doble alternativa o confirmación directa harás para concretar el trato?]</li></ol>"
                    },
                    "image": {
                        "url": "https://images.unsplash.com/photo-1682941664177-7920d0e59418?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5NjQ0NzR8MHwxfHNlYXJjaHw2fHxzbWFydHBob25lJTIwc2NyZWVuJTIwc2hvd2luZyUyMGN1c3RvbWVyJTIwY2hhdCUyMG1lc3NhZ2VzfGVufDF8MHx8fDE3ODAwODkzMzJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                        "local_url": "",
                        "caption": "Foto de Sanket Mishra en Unsplash",
                        "alt": "a person holding a cell phone with a chat app on the screen",
                        "source": "Unsplash",
                        "provider": "Unsplash API",
                        "source_url": "https://unsplash.com/photos/a-person-holding-a-cell-phone-with-a-chat-app-on-the-screen-qAKPcrIcRG8",
                        "photographer": "Sanket Mishra",
                        "license": "Unsplash License",
                        "image_type": "photo",
                        "query": "smartphone screen showing customer chat messages"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Maquinaria de Ventas Express en Acción",
        "type": "Document",
        "question": "<p>¡Enhorabuena! Has completado el recorrido teórico-práctico de <strong>Despegue Digital</strong>. Llegó el momento de consolidar tu aprendizaje y dar el paso definitivo reuniendo todas las piezas en tu propio <strong>Plan de Acción Express</strong>.</p><p>Este documento será tu hoja de ruta comercial inmediata para empezar a atraer y cerrar clientes desde hoy.</p><h3><strong>Instrucciones de entrega:</strong></h3><p>Copia y completa los siguientes 5 puntos clave en el cuadro de texto o adjunta tu documento de trabajo:</p><hr /><ol><li><strong>PASO 1: PROPUESTA DE VALOR POTENTE (Módulo 1)</strong><br />Escribe la frase de tu negocio bajo la fórmula exacta: <em>\"Ayudo a [Cliente ideal] a [Resultado deseado] a través de [Tu método] sin [Mayor frustración]\".</em></li><li><strong>PASO 2: FICHA DE CLIENTE IDEAL (Módulo 2)</strong><br />Describe brevemente el perfil de tu comprador:<br />- ¿Quién es y qué situación vive?<br />- ¿Cuál es su mayor dolor o frustración?<br />- ¿Qué beneficio urgente busca conseguir?</li><li><strong>PASO 3: ENLACE DE WHATSAPP CONFIGURADO (Módulo 3)</strong><br />Escribe el mensaje automático de bienvenida de tu enlace y comparte el link generado (puedes usar un formato simulado si lo prefieres para la práctica, ej: <code>https://wa.link/ejemplo</code>).</li><li><strong>PASO 4: PUBLICACIÓN MAGNÉTICA (Módulo 4)</strong><br />Escribe el texto de tu post orgánico de atracción incluyendo tu Gancho, tu Valor (recurso gratuito que entregarás) y el Llamado a la Acción con la palabra clave que deben comentar.</li><li><strong>PASO 5: TU GUION DE CIERRE POR CHAT (Módulo 5)</strong><br />Redacta la secuencia de respuestas que usarás cuando te pregunten el precio de tu oferta:<br />- Tu mensaje para <strong>Conectar y Calificar</strong> (Paso 1).<br />- Tu mensaje para <strong>Solucionar y Presentar el Precio</strong> (Paso 2).<br />- Tu mensaje de <strong>Cierre Directo</strong> (Paso 3).</li></ol><hr /><p><strong>¿Qué evaluará la IA para otorgar tu certificación?</strong></p><ul><li><strong>Coherencia estratégica:</strong> Que todos los pasos estén conectados (el cliente de tu ficha debe ser el mismo que se siente atraído por tu publicación y que se beneficia de tu propuesta de valor).</li><li><strong>Simplicidad y claridad:</strong> Mensajes directos, sin relleno técnico, fáciles de digerir y leer.</li><li><strong>Aplicabilidad:</strong> Que el plan esté listo para copiarse, pegarse y ponerse a prueba con clientes reales inmediatamente.</li></ul>"
    }
}


def field_exists(doctype, fieldname):
    try:
        meta = frappe.get_meta(doctype)
        return bool(meta.get_field(fieldname))
    except Exception:
        return False


def set_value_if_field_exists(doc, fieldname, value):
    if field_exists(doc.doctype, fieldname):
        setattr(doc, fieldname, value)


def get_existing_name(doctype, filters):
    try:
        found = frappe.get_all(doctype, filters=filters, fields=["name"], limit=1)
        if not found:
            return None
        first = found[0]
        return first.get("name") if isinstance(first, dict) else first.name
    except Exception:
        return None


def create_or_update_category(category_title):
    category_title = (category_title or "Sin categoría").strip()

    candidate_fields = ["category", "title", "category_name"]
    for fieldname in candidate_fields:
        if field_exists("LMS Category", fieldname):
            existing = get_existing_name("LMS Category", {fieldname: category_title})
            if existing:
                return existing

    doc = frappe.new_doc("LMS Category")

    if field_exists("LMS Category", "category"):
        doc.category = category_title
    elif field_exists("LMS Category", "title"):
        doc.title = category_title
    elif field_exists("LMS Category", "category_name"):
        doc.category_name = category_title
    else:
        doc.name = category_title

    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    return doc.name


def add_instructor_if_missing(course):
    if not field_exists("LMS Course", "instructors"):
        return

    instructors = course.get("instructors") or []
    for row in instructors:
        if getattr(row, "instructor", None) == INSTRUCTOR_NAME:
            return

    course.append("instructors", {"instructor": INSTRUCTOR_NAME})
    course.save(ignore_permissions=True)


def create_or_update_course(category_name):
    title = COURSE_DATA.get("title") or "Curso generado por StudyBadge"
    existing = get_existing_name("LMS Course", {"title": title})

    if existing:
        course = frappe.get_doc("LMS Course", existing)
    else:
        course = frappe.new_doc("LMS Course")
        course.title = title

    set_value_if_field_exists(course, "title", title)
    set_value_if_field_exists(course, "short_introduction", COURSE_DATA.get("short_introduction", ""))
    set_value_if_field_exists(course, "description", COURSE_DATA.get("description", ""))
    set_value_if_field_exists(course, "published", 1)
    set_value_if_field_exists(course, "category", category_name)
    set_value_if_field_exists(course, "card_gradient", COURSE_DATA.get("card_gradient", "Blue"))
    set_value_if_field_exists(course, "enable_certification", COURSE_DATA.get("enable_certification", 1))

    # Campos personalizados de StudyBadge. Si no existen, se ignoran.
    set_value_if_field_exists(course, "studybadge_ai_enabled", COURSE_DATA.get("studybadge_ai_enabled", 1))
    set_value_if_field_exists(course, "ai_rubric", COURSE_DATA.get("ai_rubric", ""))

    if existing:
        course.save(ignore_permissions=True)
    else:
        course.insert(ignore_permissions=True, ignore_mandatory=True)

    add_instructor_if_missing(course)
    return course.name


def assignment_filters(title, course_name):
    if field_exists("LMS Assignment", "course"):
        return {"title": title, "course": course_name}
    return {"title": title}


def create_or_update_assignment(course_name, assignment_data):
    if not assignment_data:
        return None

    title = assignment_data.get("title") or "Actividad sin título"
    existing = get_existing_name("LMS Assignment", assignment_filters(title, course_name))

    if existing:
        doc = frappe.get_doc("LMS Assignment", existing)
    else:
        doc = frappe.new_doc("LMS Assignment")
        doc.title = title

    set_value_if_field_exists(doc, "title", title)
    set_value_if_field_exists(doc, "course", course_name)
    set_value_if_field_exists(doc, "type", assignment_data.get("type", "Text"))
    set_value_if_field_exists(doc, "question", assignment_data.get("question", ""))

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    return doc.name


def normalize_question(question_data):
    q = dict(question_data or {})
    q["question"] = q.get("question") or "Pregunta sin título"

    options = q.get("options") or []
    options = [str(opt) for opt in options[:4]]
    while len(options) < 4:
        options.append("Opción pendiente")

    try:
        answer = int(q.get("answer", 0))
    except Exception:
        answer = 0

    if answer < 0 or answer > 3:
        answer = 0

    q["options"] = options
    q["answer"] = answer
    q["explanation"] = q.get("explanation") or "Respuesta correcta."
    return q


def create_or_update_question(question_data):
    question_data = normalize_question(question_data)
    q_text = question_data["question"]

    existing = get_existing_name("LMS Question", {"question": q_text})
    if existing:
        doc = frappe.get_doc("LMS Question", existing)
    else:
        doc = frappe.new_doc("LMS Question")
        doc.question = q_text

    set_value_if_field_exists(doc, "question", q_text)
    set_value_if_field_exists(doc, "type", "Choices")

    options = question_data["options"]
    answer_idx = question_data["answer"]
    explanation = question_data["explanation"]

    for idx in range(4):
        set_value_if_field_exists(doc, f"option_{idx + 1}", options[idx])
        set_value_if_field_exists(doc, f"is_correct_{idx + 1}", 1 if idx == answer_idx else 0)
        set_value_if_field_exists(doc, f"explanation_{idx + 1}", explanation if idx == answer_idx else "")

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    return doc.name


def quiz_filters(title, course_name):
    if field_exists("LMS Quiz", "course"):
        return {"title": title, "course": course_name}
    return {"title": title}


def create_or_update_quiz(course_name, quiz_data):
    if not quiz_data:
        return None

    title = quiz_data.get("title") or "Quiz sin título"
    existing = get_existing_name("LMS Quiz", quiz_filters(title, course_name))

    if existing:
        doc = frappe.get_doc("LMS Quiz", existing)
    else:
        doc = frappe.new_doc("LMS Quiz")
        doc.title = title

    set_value_if_field_exists(doc, "title", title)
    set_value_if_field_exists(doc, "course", course_name)
    set_value_if_field_exists(doc, "passing_percentage", quiz_data.get("passing_percentage", 70))
    set_value_if_field_exists(doc, "max_attempts", quiz_data.get("max_attempts", 3))

    if not existing:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    if field_exists("LMS Quiz", "questions"):
        doc.set("questions", [])
        for q in quiz_data.get("questions", []):
            question_name = create_or_update_question(q)
            row = {"question": question_name, "marks": q.get("marks", 1)}
            doc.append("questions", row)

    doc.save(ignore_permissions=True)
    return doc.name


def paragraph_block(text):
    text = str(text or "").replace("\n", "<br>")
    return {
        "type": "paragraph",
        "data": {
            "text": text
        }
    }


def header_block(text, level=3):
    return {
        "type": "header",
        "data": {
            "text": str(text or "Tema"),
            "level": level
        }
    }


def _safe_filename_part(value):
    value = str(value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "imagen"


def _guess_extension(response, source_url):
    content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    extension = mimetypes.guess_extension(content_type) if content_type else None
    if extension == ".jpe":
        extension = ".jpg"
    if not extension:
        parsed = urlparse(response.url or source_url or "")
        extension = os.path.splitext(parsed.path)[1]
    if extension.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".svg"}:
        extension = ".jpg"
    return extension or ".jpg"


def _existing_file_url(lesson_doc, file_name):
    if not lesson_doc or not file_name:
        return None

    try:
        existing = frappe.get_all(
            "File",
            filters={
                "attached_to_doctype": lesson_doc.doctype,
                "attached_to_name": lesson_doc.name,
                "file_name": file_name,
            },
            fields=["file_url"],
            limit=1,
        )
        if existing:
            return existing[0].get("file_url")
    except Exception:
        pass

    return None


def _download_and_store_image(image_url, lesson_doc, suggested_name):
    image_url = str(image_url or "").strip()
    if not image_url:
        return ""

    if image_url.startswith("/files/"):
        return image_url

    safe_name = _safe_filename_part(suggested_name)

    try:
        response = requests.get(image_url, timeout=60, stream=True, allow_redirects=True)
        response.raise_for_status()
        extension = _guess_extension(response, image_url)
        file_name = f"{safe_name}{extension}"

        existing_url = _existing_file_url(lesson_doc, file_name)
        if existing_url:
            return existing_url

        file_doc = save_file(
            file_name,
            response.content,
            lesson_doc.doctype,
            lesson_doc.name,
            is_private=0,
        )
        return file_doc.file_url if file_doc else ""
    except Exception as exc:
        print(f"No se pudo descargar la imagen '{image_url}': {exc}")
        return ""


def _resolve_local_image_url(image_data, lesson_doc=None):
    image_data = image_data or {}
    local_url = str(image_data.get("local_url") or image_data.get("file_url") or "").strip()
    if local_url:
        return local_url

    url = str(image_data.get("url") or "").strip()
    if not url:
        return ""

    if url.startswith("/files/"):
        return url

    if lesson_doc is None:
        return url

    source_name = (
        image_data.get("file_name")
        or image_data.get("filename")
        or image_data.get("source")
        or image_data.get("provider")
        or image_data.get("query")
        or image_data.get("caption")
        or "imagen"
    )
    stored_url = _download_and_store_image(url, lesson_doc, source_name)
    if stored_url:
        image_data["local_url"] = stored_url
        return stored_url
    return url


def image_block(image_data, lesson_doc=None):
    image_data = image_data or {}
    url = _resolve_local_image_url(image_data, lesson_doc)
    if not url:
        print("[IMAGE][SKIP] No hay URL de imagen para esta lección.")
        return None

    caption = str(image_data.get("caption") or image_data.get("alt") or "").strip()

    # IMPORTANTE:
    # Frappe LMS renderiza este bloque con el tool SimpleImage de EditorJS.
    # Ese tool espera data.url directamente.
    # Si le pasas data.file.url, el HTML queda como:
    # <div class="cdx-simple-image"><div class="cdx-loader"></div></div>
    # y se queda cargando para siempre.
    print(f"[IMAGE][BLOCK] Insertando imagen en EditorJS SimpleImage: {url}")

    return {
        "type": "image",
        "data": {
            "url": url,
            "caption": caption,
            "withBorder": False,
            "withBackground": False,
            "stretched": False
        }
    }


def build_editorjs_content(lesson_data, quiz_name=None, assignment_name=None, lesson_doc=None):
    blocks = []

    blocks.append(header_block("Objetivo de la lectura", 2))
    blocks.append(paragraph_block(
        lesson_data.get("objective")
        or "Lee esta sección con una idea práctica: al terminar, tendrás una pieza concreta para avanzar en tu proyecto."
    ))

    img = image_block(lesson_data.get("image"), lesson_doc)
    if img:
        blocks.append(img)

    for section in lesson_data.get("sections", []):
        heading = section.get("heading") or "Tema"
        blocks.append(header_block(heading, 3))
        for paragraph in section.get("paragraphs", []):
            if str(paragraph).strip():
                blocks.append(paragraph_block(paragraph))

    if quiz_name:
        blocks.append(header_block("Quiz corto de la lectura", 3))
        blocks.append(paragraph_block(
            "Responde este quiz breve para comprobar que entendiste las ideas principales antes de pasar a la actividad."
        ))
        blocks.append({
            "type": "quiz",
            "data": {
                "quiz": quiz_name
            }
        })

    if assignment_name:
        blocks.append(header_block("Actividad práctica", 3))
        blocks.append(paragraph_block(
            "Completa esta actividad pensando en un caso real o ficticio. La meta es construir algo aplicable, no solo responder teoría."
        ))
        blocks.append({
            "type": "assignment",
            "data": {
                "assignment": assignment_name
            }
        })

    return json.dumps({
        "time": int(time.time() * 1000),
        "blocks": blocks,
        "version": "2.29.1"
    }, ensure_ascii=False)


def lesson_filters(title, chapter_name):
    if field_exists("Course Lesson", "chapter"):
        return {"title": title, "chapter": chapter_name}
    return {"title": title}


def create_or_update_lesson(course_name, chapter_name, lesson_data):
    title = lesson_data.get("title") or "Lección sin título"
    existing = get_existing_name("Course Lesson", lesson_filters(title, chapter_name))

    if existing:
        doc = frappe.get_doc("Course Lesson", existing)
    else:
        doc = frappe.new_doc("Course Lesson")
        doc.title = title

    quiz_name = None
    if lesson_data.get("quiz"):
        quiz_name = create_or_update_quiz(course_name, lesson_data["quiz"])

    assignment_name = None
    if lesson_data.get("assignment"):
        assignment_name = create_or_update_assignment(course_name, lesson_data["assignment"])

    set_value_if_field_exists(doc, "title", title)
    set_value_if_field_exists(doc, "chapter", chapter_name)
    set_value_if_field_exists(doc, "course", course_name)

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    set_value_if_field_exists(doc, "body", "")
    set_value_if_field_exists(doc, "content", build_editorjs_content(lesson_data, quiz_name, assignment_name, doc))

    doc.save(ignore_permissions=True)

    return doc.name


def chapter_filters(title, course_name):
    if field_exists("Course Chapter", "course"):
        return {"title": title, "course": course_name}
    return {"title": title}


def get_chapter_lessons(chapter_data):
    lessons = chapter_data.get("lessons")
    if isinstance(lessons, list) and lessons:
        return lessons

    lesson = chapter_data.get("lesson")
    if isinstance(lesson, dict):
        return [lesson]

    return []


def create_or_update_chapter(course_name, chapter_data):
    title = chapter_data.get("title") or "Módulo sin título"
    existing = get_existing_name("Course Chapter", chapter_filters(title, course_name))

    if existing:
        doc = frappe.get_doc("Course Chapter", existing)
    else:
        doc = frappe.new_doc("Course Chapter")
        doc.title = title

    set_value_if_field_exists(doc, "title", title)
    set_value_if_field_exists(doc, "course", course_name)

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    lesson_names = []
    for lesson_data in get_chapter_lessons(chapter_data):
        lesson_name = create_or_update_lesson(course_name, doc.name, lesson_data)
        lesson_names.append(lesson_name)

    if field_exists("Course Chapter", "lessons"):
        doc.set("lessons", [])
        for lesson_name in lesson_names:
            doc.append("lessons", {"lesson": lesson_name})
        doc.save(ignore_permissions=True)

    return doc.name


def build_final_project_chapter():
    final_project = COURSE_DATA.get("final_project")
    if not final_project:
        return None

    return {
        "title": "Proyecto final del curso",
        "lessons": [
            {
                "title": final_project.get("title") or "Proyecto final",
                "objective": "Integra lo aprendido en el curso en un entregable práctico.",
                "sections": [
                    {
                        "heading": "Instrucciones del proyecto final",
                        "paragraphs": [
                            "Este proyecto final te ayuda a unir las ideas principales del curso en una entrega clara y aplicable.",
                            "Lee bien la consigna, organiza tu respuesta y entrega un documento o texto que pueda evaluarse con criterios prácticos."
                        ]
                    }
                ],
                "assignment": final_project
            }
        ]
    }


def rebuild_course_chapters(course_name, chapter_names):
    course = frappe.get_doc("LMS Course", course_name)
    if field_exists("LMS Course", "chapters"):
        course.set("chapters", [])
        for chapter_name in chapter_names:
            course.append("chapters", {"chapter": chapter_name})
        course.save(ignore_permissions=True)


def run():
    frappe.set_user("Administrator")
    print("=======================================")
    print("INICIANDO SETUP DE CURSO GENERADO...")
    print("=======================================")

    category_name = create_or_update_category(COURSE_DATA.get("category", "Sin categoría"))
    course_name = create_or_update_course(category_name)

    chapter_names = []
    for chapter_data in COURSE_DATA.get("chapters", []):
        chapter_name = create_or_update_chapter(course_name, chapter_data)
        chapter_names.append(chapter_name)

    final_project_chapter = build_final_project_chapter()
    if final_project_chapter:
        chapter_name = create_or_update_chapter(course_name, final_project_chapter)
        chapter_names.append(chapter_name)

    rebuild_course_chapters(course_name, chapter_names)

    frappe.db.commit()
    print("=======================================")
    print("CURSO CREADO O ACTUALIZADO CON ÉXITO")
    print("Curso:", COURSE_DATA.get("title"))
    print("Course ID:", course_name)
    print("Capítulos:", len(chapter_names))
    print("=======================================")


if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    try:
        frappe.init(site=site)
        frappe.connect()
        run()
    except Exception:
        print("Ocurrió un error al crear el curso.")
        traceback.print_exc()
        raise
    finally:
        try:
            frappe.destroy()
        except Exception:
            pass
