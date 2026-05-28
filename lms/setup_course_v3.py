# -*- coding: utf-8 -*-
"""
Curso generado para Frappe Learning / Frappe LMS por StudyBadge.

Uso desde frappe-bench:
    python apps/lms/setup_course_generated.py studybadge.localhost

Notas:
- Script idempotente: si lo ejecutas varias veces, actualiza en lugar de duplicar.
- Usa Course Lesson.content con bloques EditorJS para renderizar texto, quizzes y assignments.
"""

import os
import sys
import json
import time
import traceback

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

import frappe

INSTRUCTOR_NAME = "Administrator"
COURSE_DATA = {
    "category": "Negocios Digitales e Inteligencia Artificial",
    "title": "Máquina de Comisiones con IA: Tu Primera Venta en Hotmart Sin Mostrar tu Rostro",
    "short_introduction": "Crea un sistema automatizado de afiliado usando Inteligencia Artificial para generar comisiones reales sin invertir y de forma 100% anónima.",
    "description": "<p>Este curso práctico te enseña paso a paso a usar herramientas gratuitas de Inteligencia Artificial para encontrar productos ganadores en Hotmart y crear canales automatizados que venden por ti en piloto automático. Olvídate de la timidez de salir en cámara o de redactar textos complejos; aquí delegamos el 80% del trabajo pesado en la tecnología para que obtengas resultados en tiempo récord.</p><ul><li>Selecciona infoproductos de alta demanda con ayuda de IA.</li><li>Crea canales de TikTok o Reels altamente persuasivos sin mostrar tu rostro.</li><li>Genera guiones, locuciones y videos virales en cuestión de minutos.</li><li>Cierra tus primeras ventas de afiliado sin tecnicismos ni complicaciones.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza la comprensión del ecosistema, la aplicación real del método 'faceless', la claridad de los textos y la creatividad de los prompts antes que la perfección técnica. Valora el esfuerzo real, la coherencia con el nicho elegido y el uso correcto de llamados a la acción (CTA). Penaliza respuestas genéricas, vacías o que no apliquen lo aprendido en los módulos. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, áreas de mejora, nota final y estado: Aprobado (7 o más) o Desaprobado (menor a 7).",
    "chapters": [
        {
            "title": "Módulo 1: La Mina de Oro Digital",
            "lessons": [
                {
                    "title": "El Filtro Exprés: Encuentra tu Producto Ganador en 15 Minutos",
                    "objective": "Aprender a filtrar el catálogo de Hotmart y usar ChatGPT como tu consultor de negocios personal para seleccionar un infoproducto altamente vendible.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "El mayor error que comete el 90% de los afiliados novatos es elegir un producto basándose únicamente en su intuición. Intentar vender algo solo porque a ti te gusta es el camino más rápido hacia la frustración y las cero ventas.",
                                "Para construir una máquina de ventas que funcione en piloto automático y sin mostrar tu rostro, necesitas un producto que resuelva un dolor real, urgente y profundo. En esta lección aprenderás a delegar la parte analítica en ChatGPT, transformándolo en un experto en marketing que elegirá tu boleto dorado al éxito."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para encontrar un producto ganador con Inteligencia Artificial, primero debemos entender qué hace que un infoproducto se venda como pan caliente. Buscamos tres cosas clave: una comisión atractiva (entre el 60% y el 80%), una página de ventas persuasiva, y un \"dolor caliente\" (un problema urgente que la gente quiera resolver ya).",
                                "En lugar de pasar días leyendo foros para entender qué le duele a tu cliente ideal, usaremos ChatGPT. Tu única tarea será entrar a Hotmart, preseleccionar tres productos que llamen tu atención y luego activar el 'Prompt de Validación de Nicho'. Este comando le ordena a la IA analizar la psicología del comprador para cada opción y decirte con precisión matemática cuál es el producto más fácil de vender usando videos cortos sin rostro."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que entras al mercado de Hotmart y seleccionas estos tres cursos: 1) 'Adiestramiento Canino desde Cero', 2) 'Aprende Costura Premium' y 3) 'Reparación de Celulares'. En lugar de adivinar cuál es mejor, vas a ChatGPT y le escribes el siguiente prompt exacto:",
                                "\"Actúa como un experto en marketing de afiliados y psicología del consumidor. Voy a vender un infoproducto de forma orgánica en TikTok sin mostrar mi rostro. Analiza estas tres opciones: 1. Adiestramiento Canino, 2. Costura Premium, 3. Reparación de Celulares. Dime cuál de estos productos genera compras más impulsivas basadas en emociones, cuál tiene el público objetivo más fácil de segmentar con videos cortos y cuál me dará comisiones más rápido. Justifica tu respuesta.\"",
                                "ChatGPT analizará los disparadores psicológicos y te responderá de forma analítica confirmando que el ganador es 'Adiestramiento Canino', debido a que un perro travieso genera un dolor emocional inmediato y los videos de perritos son sumamente virales en redes sociales, facilitando la creación de contenido orgánico sin rostro."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "Evita elegir productos con una temperatura extremadamente alta (150 grados en Hotmart) al principio. Aunque se venden mucho, la competencia de afiliados profesionales es feroz. Apunta a productos de entre 20 y 70 grados de temperatura, donde hay demanda pero la competencia es moderada.",
                                "Tampoco promuevas productos que te paguen comisiones de apenas 2 o 5 dólares. El esfuerzo para crear contenido y atraer clientes es el mismo que harás para vender un producto que te deje 25 o 35 dólares por venta. Valora tu tiempo y no promuevas nada que pague menos del 60% de comisión."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: No adivines qué se va a vender. Deja que ChatGPT analice el comportamiento humano y el potencial de viralidad de tus opciones para que elijas sobre seguro. Enfócate en productos de alta comisión que resuelvan dolores urgentes.",
                                "Tu acción recomendada para hoy: Abre una cuenta gratuita en Hotmart, ve al Mercado de Afiliación y selecciona 3 productos que te llamen la atención. Copia sus nombres, abre ChatGPT, aplícales el prompt que viste en el ejemplo práctico y define hoy mismo tu producto ganador."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz Express: Tu Primer Producto Ganador con ChatGPT",
                        "questions": [
                            {
                                "question": "¿Cuál es la temperatura ideal en Hotmart recomendada para evitar la competencia feroz al iniciar?",
                                "options": [
                                    "Exactamente 150 grados de temperatura.",
                                    "Entre 20 y 70 grados de temperatura.",
                                    "Menos de 10 grados para asegurar que nadie más lo venda.",
                                    "Más de 120 grados para garantizar ventas automáticas."
                                ],
                                "answer": 1,
                                "explanation": "Apuntar a productos de entre 20 y 70 grados permite encontrar un mercado con demanda validada pero sin la competencia abrumadora de los afiliados profesionales que dominan los productos de 150 grados."
                            },
                            {
                                "question": "Según la lección, ¿cuáles son los tres factores clave que hacen que un infoproducto se venda de forma masiva?",
                                "options": [
                                    "Un banner atractivo, comisiones de 2 a 5 dólares y que el tema te guste a ti personalmente.",
                                    "Comisión del 60% al 80%, página de ventas persuasiva y que apunte a un 'dolor caliente'.",
                                    "Que tenga una temperatura de 150 grados, que sea fácil de entender y que requiera mostrar tu rostro.",
                                    "Que sea de un nicho racional, que tenga bajo precio y que no use inteligencia artificial."
                                ],
                                "answer": 1,
                                "explanation": "Para construir una máquina de ventas exitosa necesitas comisiones atractivas (60% al 80%), una página que persuada y, lo más importante, que resuelva un problema urgente o 'dolor caliente' para el comprador."
                            },
                            {
                                "question": "En el ejemplo práctico, ¿por qué ChatGPT determinó que el curso de 'Adiestramiento Canino' era mejor opción que el de 'Costura Premium'?",
                                "options": [
                                    "Porque el nicho de la costura no tiene personas interesadas en internet.",
                                    "Porque el curso de costura requiere comisiones más bajas de 5 dólares.",
                                    "Porque un perro travieso genera un dolor emocional inmediato y frustración diaria, y sus videos se viralizan fácilmente sin mostrar el rostro.",
                                    "Porque adiestrar un perro requiere un proceso de decisión de compra mucho más lento y racional."
                                ],
                                "answer": 2,
                                "explanation": "ChatGPT justifica que un problema con una mascota genera un dolor inmediato que impulsa compras más emocionales y rápidas, además de que el contenido de perritos es altamente viralizable de forma orgánica en redes sociales."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primer Boleto Dorado Validado por IA",
                        "type": "Text",
                        "question": "<p>¡Es hora de pasar de la teoría a la acción! Vas a convertirte en un detective de mercado y usarás la Inteligencia Artificial para validar tu primer producto ganador.</p><h3>Tu Objetivo:</h3><p>Encontrar 3 productos viables en Hotmart, pasarlos por el filtro de ChatGPT y seleccionar oficialmente el infoproducto ganador que promoverás de forma anónima.</p><h3>Instrucciones:</h3><ul><li><strong>Paso 1: La Cacería en Hotmart.</strong> Ingresa a tu cuenta de Hotmart, ve al Mercado y preselecciona 3 productos con temperatura entre 20 y 70 grados, que dejen al menos el 60% de comisión.</li><li><strong>Paso 2: Consulta al Experto.</strong> Copia el prompt de la lección en ChatGPT y adáptalo con los 3 productos elegidos. Analiza la respuesta detallada de la IA.</li><li><strong>Paso 3: Tu Decisión.</strong> Elige el producto ganador definitivo basándote en la recomendación de ChatGPT y en su viabilidad para videos cortos sin aparecer en cámara.</li></ul><h3>¿Qué debes entregar?</h3><p>Copia y pega en el cuadro de texto las siguientes respuestas:</p><ol><li><strong>Mis 3 candidatos:</strong> Nombre de los productos con su respectiva temperatura y comisión.</li><li><strong>La recomendación de ChatGPT:</strong> Cuál de los tres fue el ganador según el análisis de la IA y por qué.</li><li><strong>Mi veredicto y plan de acción:</strong> Explica brevemente por qué te convence este producto y qué tipo de videos cortos (sin rostro) te imaginas creando para promocionarlo.</li></ol>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: Tu Identidad Digital Secreta",
            "lessons": [
                {
                    "title": "Configuración Magnética de tus Redes 'Faceless' con IA",
                    "objective": "Crear y optimizar un perfil persuasivo en TikTok o Instagram sin mostrar tu rostro, utilizando IA para definir tu nombre, biografía y avatar en minutos.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¡Bienvenido al Módulo 2! Hoy vas a dar el primer gran paso práctico de tu negocio digital. En el método 'Faceless', tu perfil de redes sociales no es un espacio personal; es una máquina de ventas automatizada orientada a un nicho específico.",
                                "Para que esta máquina funcione y atraiga clientes todos los días, necesita verse profesional, confiable y magnética desde el segundo uno. No necesitas ser diseñador ni redactor. Vamos a delegar este trabajo creativo en herramientas gratuitas de Inteligencia Artificial."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para construir un perfil magnético sin rostro, optimizaremos tres elementos clave con ayuda de la IA: el Nombre de Usuario, la Biografía Persuasiva y la Identidad Visual.",
                                "El Nombre de Usuario debe ser corto, memorable y contener la palabra clave del nicho (por ejemplo: @adiestramiento.pro). Esto ayuda a que el algoritmo de búsqueda te recomiende.",
                                "La Biografía es tu carta de presentación. En menos de 150 caracteres debe responder tres preguntas esenciales: ¿Qué aprenderá aquí el usuario?, ¿Por qué debería seguirte? y ¿Qué tiene que hacer ahora? (Llamado a la Acción o CTA).",
                                "Para la Imagen de Perfil, al ser una cuenta sin rostro, usaremos un logotipo minimalista o una ilustración conceptual de alta calidad relacionada con tu nicho generada por herramientas gratuitas como Bing Image Creator (DALL-E 3) o Canva."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que elegiste vender un curso de Hotmart sobre 'Adiestramiento Canino'. Vas a ChatGPT y le escribes: 'Dame 10 ideas de nombres de usuario cortos y magnéticos para una cuenta de Instagram Faceless sobre adiestramiento de perros. Además, escribe 3 opciones de biografía persuasiva que terminen con un llamado a la acción para hacer clic en el enlace'.",
                                "ChatGPT te devolverá opciones como '@EducaTuCan' y biografías listas como: '🐶 Transforma el comportamiento de tu perro en casa. 🎓 Tips diarios de adiestramiento sin castigos. 👇 ¡Consigue el acceso aquí!'",
                                "Luego, vas a Bing Image Creator y escribes el prompt visual: 'Un logotipo minimalista y moderno de la silueta de un perro feliz, estilo vector, fondo plano de color azul pastel, alta resolución'. Descargas la imagen, la subes a tu perfil y listo: tienes una marca profesional creada en minutos y gratis."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es usar nombres de usuario personales o confusos llenos de números y guiones difíciles de recordar (como @pedro_1994_adiestramiento_perros_ok). Esto destruye la confianza y dificulta que te encuentren.",
                                "Otro error es dejar la biografía vacía o sin un llamado a la acción (CTA) claro. Si la gente llega a tu perfil y no les dices exactamente qué hacer, se irán sin comprar.",
                                "Por último, usar imágenes de perfil pixeladas o descargadas directamente de Google con mala calidad transmite falta de profesionalismo, lo que arruinará tus conversiones."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Configurar tu identidad secreta consiste en alinear un nombre de usuario con palabra clave, una biografía con gancho y llamada a la acción, y una imagen limpia generada por IA.",
                                "Tu acción recomendada para hoy: Abre una nueva cuenta en TikTok o Instagram. Usa ChatGPT para definir tu nombre y biografía siguiendo las pautas de esta lección. Genera tu avatar con Bing Image Creator o Canva, configúralo todo en tu perfil y déjalo listo. ¡Aún no publiques contenido!"
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Configuración de tu Perfil Faceless",
                        "questions": [
                            {
                                "question": "¿Qué características debe tener un Nombre de Usuario ideal para tu cuenta 'Faceless'?",
                                "options": [
                                    "Debe ser corto, memorable y contener la palabra clave de tu nicho para que el algoritmo te recomiende.",
                                    "Debe incluir tu nombre real, año de nacimiento y varios guiones para que sea único.",
                                    "Debe ser lo más largo posible para explicar detalladamente de qué trata tu cuenta.",
                                    "Debe consistir únicamente en emojis y códigos numéricos difíciles de rastrear."
                                ],
                                "answer": 0,
                                "explanation": "Un buen nombre de usuario debe ser limpio, corto e incluir la palabra clave de tu nicho para facilitar las búsquedas y ayudar al algoritmo a posicionar tu cuenta."
                            },
                            {
                                "question": "¿Cuáles son las tres preguntas clave que debe responder una biografía persuasiva en menos de 150 caracteres?",
                                "options": [
                                    "¿Quién es el dueño de la cuenta?, ¿cuánto dinero gana? y ¿dónde vive?",
                                    "¿Cuántas publicaciones harás al día?, ¿qué hashtags usarás? y ¿qué IA prefieres?",
                                    "¿Qué aprenderá aquí?, ¿por qué debería seguirte? y ¿qué tiene que hacer ahora (CTA)?",
                                    "¿Cuál es el precio del producto afiliado?, ¿qué garantía tiene? y ¿cómo se paga?"
                                ],
                                "answer": 2,
                                "explanation": "Una biografía magnética debe dejar claro el beneficio inmediato para el visitante, darle una razón sólida para seguirte y guiarlo con un llamado a la acción (CTA) claro hacia tu enlace."
                            },
                            {
                                "question": "Según la acción recomendada de esta lección, ¿qué debes hacer inmediatamente después de configurar tu perfil con IA?",
                                "options": [
                                    "Comenzar a publicar al menos tres videos diarios inmediatamente.",
                                    "Dejar listo el perfil (nombre, biografía y avatar) pero sin publicar contenido todavía.",
                                    "Invertir en publicidad de pago para conseguir seguidores rápidamente.",
                                    "Enviar mensajes privados para venderle directamente a tus conocidos."
                                ],
                                "answer": 1,
                                "explanation": "El plan de acción te invita a preparar y optimizar profesionalmente tu perfil con IA hoy mismo, pero te recomienda esperar al siguiente módulo antes de empezar a publicar contenido."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primer Perfil Faceless Magnético Creado con IA",
                        "type": "Text",
                        "question": "<p>¡Ha llegado el momento de diseñar tu marca secreta! Vas a estructurar la identidad de tu nueva cuenta \"Faceless\" aplicando Inteligencia Artificial.</p><p>Para completar esta tarea, copia la siguiente estructura, complétala con tus datos y envíala:</p><ul><li><strong>1. Mi Nicho de Mercado:</strong> Define el nicho que elegiste (ej: Repostería Saludable, Adiestramiento de Perros, Finanzas).</li><li><strong>2. Mi Nombre de Usuario Pro:</strong> El nombre de usuario estratégico que elegiste y su palabra clave para el algoritmo.</li><li><strong>3. Mi Biografía Persuasiva:</strong> Escribe tu biografía dividida en las 3 líneas clave:<ul><li><em>Línea 1 (¿Qué aprenderán aquí?):</em></li><li><em>Línea 2 (¿Por qué seguirte / Beneficio?):</em></li><li><em>Línea 3 (Llamado a la acción o CTA):</em></li></ul></li><li><strong>4. El Prompt de mi Avatar:</strong> Escribe el prompt visual que le diste a Bing Image Creator o Canva para generar tu foto de perfil, y describe cómo luce el diseño final.</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: La Fábrica de Contenido Infinito",
            "lessons": [
                {
                    "title": "Creación en Masa de Videos con ChatGPT y CapCut",
                    "objective": "Aprender a estructurar, redactar y producir decenas de videos cortos (Reels, TikToks o Shorts) de forma automatizada utilizando ChatGPT para los guiones y CapCut para la edición rápida sin salir en cámara.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Pensar en qué decir, grabarse frente a la cámara, equivocarse mil veces y luego pasar horas editando es una receta segura para el cansancio. La buena noticia es que ya no tienes que hacer nada de eso.",
                                "Con el método 'Faceless' (sin rostro), delegamos el trabajo pesado en la Inteligencia Artificial. En esta lección aprenderás a activar una auténtica fábrica de videos virales utilizando ChatGPT como tu guionista estrella y CapCut como tu editor automatizado."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para que un video corto venda de forma orgánica, necesita tres ingredientes obligatorios: un gancho visual y magnético en los primeros 3 segundos, un desarrollo rápido (problema/solución), y un llamado a la acción (CTA) clarísimo al final.",
                                "El proceso se divide en tres pasos ultra rápidos. Primero, usamos ChatGPT con un prompt optimizado para escribir guiones virales basados en los dolores de tu cliente ideal. Segundo, descargamos videos de fondo (B-Roll) de alta calidad en plataformas de stock gratuitas como Pexels o Pixabay. Tercero, llevamos todo a CapCut, aplicamos subtítulos automáticos modernos y generamos una voz digital realista con la opción de 'Texto a Voz'."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que estás vendiendo un curso sobre 'Pastelería Canina'. En lugar de romperte la cabeza, vas a ChatGPT y escribes el siguiente comando exacto:",
                                "\"Actúa como un experto en marketing de afiliados. Escribe 3 guiones de 15 segundos para TikTok sobre Pastelería Canina. Cada guion debe tener: 1. Un gancho intrigante para dueños de perros, 2. Un dolor (los premios industriales les hacen daño) y 3. Un llamado a la acción para ir al enlace de mi biografía. Usa un tono cercano y directo.\"",
                                "ChatGPT te entregará los guiones al instante. Luego, vas a Pexels, descargas un video de 15 segundos de un perrito feliz, lo abres en CapCut, añades el texto, activas la opción 'Texto a voz' (con una voz natural como la de 'Julio'), generas subtítulos automáticos en un estilo llamativo y listo. Tienes un video vendedor en menos de 5 minutos."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es usar voces de IA que suenan extremadamente robóticas o aburridas. CapCut tiene opciones muy realistas y amigables. Dedica un minuto a seleccionar la correcta.",
                                "Otro fallo común es poner subtítulos aburridos, gigantes o que tapan todo el video. Usa fuentes modernas como 'Montserrat', resalta palabras clave en color amarillo o verde y asegúrate de centrar el texto.",
                                "Por último, no olvides el llamado a la acción. Si no le dices a la gente al final del video: 'Ve al enlace de mi perfil para más información', simplemente le darán 'me gusta' y se irán."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Con ChatGPT redactando tus textos, videos de stock gratuitos de fondo y CapCut automatizando los subtítulos y la voz, puedes tener listo el contenido de toda una semana en una sola tarde.",
                                "Tu acción recomendada para hoy: Abre ChatGPT y pídele 3 guiones utilizando el prompt del ejemplo adaptado al producto que elegiste vender. Descarga un video de stock, monta tu primer video sin rostro en CapCut, expórtalo y déjalo listo en tu galería para publicar."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz rápido: Fábrica de Videos Virales sin Rostro",
                        "questions": [
                            {
                                "question": "¿Cuáles son los tres ingredientes clave que debe tener un video corto para vender en redes sociales sin mostrar tu rostro?",
                                "options": [
                                    "Un gancho magnético en los primeros 3 segundos, un desarrollo rápido de problema/solución y un llamado a la acción claro al final.",
                                    "Una cámara profesional de alta gama, música en tendencia y un guion largo de más de dos minutos.",
                                    "Aparecer bailando frente a la pantalla, usar efectos de animación 3D y colocar subtítulos en tres idiomas.",
                                    "Un logo gigante de tu marca, un fondo completamente blanco y no incluir ninguna voz."
                                ],
                                "answer": 0,
                                "explanation": "Según la lección, estos tres elementos garantizan que el video capte la atención de inmediato, mantenga el interés con una solución rápida y guíe al espectador a realizar la acción de compra o registro."
                            },
                            {
                                "question": "¿Qué es el 'B-Roll' y en qué plataformas puedes conseguirlo de forma gratuita?",
                                "options": [
                                    "Es un tipo de subtítulo dinámico y colorido que se descarga desde la biblioteca de Google.",
                                    "Es un video de fondo libre de derechos de autor que ilustra lo que dices, y se puede descargar de sitios como Pexels o Pixabay.",
                                    "Es el comando exacto o 'prompt' que le introduces a ChatGPT para generar un guion de ventas.",
                                    "Es la voz digital e hiperrealista que se genera automáticamente con la inteligencia artificial de CapCut."
                                ],
                                "answer": 1,
                                "explanation": "El B-Roll sirve para ilustrar visualmente tu mensaje (como un perrito jugando o alguien cocinando) sin tener que grabarte a ti mismo, y plataformas como Pexels o Pixabay te lo ofrecen de forma gratuita."
                            },
                            {
                                "question": "De acuerdo con la lección, ¿cuál es uno de los errores más graves que debes evitar al crear estos videos?",
                                "options": [
                                    "Utilizar la computadora para editar en lugar de hacer todo exclusivamente en el teléfono celular.",
                                    "Hacer guiones basados en los dolores y deseos del cliente ideal en lugar de solo hablar del producto.",
                                    "Utilizar voces de Inteligencia Artificial que suenan extremadamente robóticas, aburridas o sin vida.",
                                    "Publicar videos de 15 segundos porque la gente solo consume contenido de exactamente un minuto."
                                ],
                                "answer": 2,
                                "explanation": "La lección destaca que las voces robóticas ahuyentan a la audiencia. Lo ideal es tomarse un minuto para elegir voces naturales y amigables en CapCut (como la voz de 'Julio' o voces tiernas) para generar una conexión real."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: Tu Primer Video Faceless Listo para Publicar",
                        "type": "Text",
                        "question": "<p>¡Llegó el momento de activar tu fábrica de contenido! Vas a estructurar tu primer video corto listo para atraer clientes en redes sociales.</p><p><strong>Instrucciones:</strong> Escribe tu respuesta en el cuadro de texto completando los siguientes puntos:</p><ol><li>El <strong>nicho o producto</strong> elegido de Hotmart.</li><li>El <strong>guion de 15 segundos</strong> generado por ChatGPT (señalando claramente cuál es el Gancho, la Solución y el CTA).</li><li>La <strong>descripción del video de fondo</strong> (B-roll) que elegiste usar de Pexels o Pixabay.</li><li>La <strong>voz de CapCut seleccionada</strong> y el estilo de tus subtítulos (colores y palabras de resalte).</li></ol>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: El Arte de Vender en Automático",
            "lessons": [
                {
                    "title": "El Script de Cierre Perfecto y Automatización de Enlaces",
                    "objective": "Estructurar un mensaje de ventas irresistible y configurar un sistema sencillo de automatización para que tus enlaces de afiliado se entreguen solos.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Has creado contenido con IA, tus videos tienen visitas y la gente empieza a comentar de forma masiva. ¡Felicidades! Pero ahora toca el paso decisivo: ¿cómo conviertes esos comentarios en comisiones de Hotmart sin estar pegado todo el día a la pantalla?",
                                "Aquí es donde ocurre la magia de la automatización Faceless. Con un script bien estructurado y una herramienta que responda por ti, tu único trabajo real será revisar las notificaciones de ventas mientras realizas otras actividades."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "El 'Script de Cierre Perfecto' no es un discurso molesto, sino una conversación guiada en tres pasos rápidos: Conexión, Transformación y Llamado a la Acción. Primero, validas el interés del usuario; segundo, presentas el beneficio principal del producto digital; y tercero, das una instrucción clara para que haga clic.",
                                "Para automatizar el proceso, utilizamos 'palabras de activación' en los videos (ej: 'Comenta la palabra QUIERO'). Herramientas gratuitas y sencillas como ManyChat para Instagram, o las respuestas automáticas integradas en TikTok, detectarán esa palabra clave y enviarán tu script persuasivo con tu enlace de afiliado por mensaje privado (DM) de manera instantánea."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que promueves un curso online de 'Pastelería Canina'. Tu video termina invitando a la gente a comentar 'SANO'. Cuando un usuario lo hace, tu sistema le envía instantáneamente por privado:",
                                "'¡Hola! Qué gusto tu interés en cuidar la salud de tu mejor amigo. 🐾 Con nuestro programa online aprenderás a preparar snacks saludables en casa y sin conservantes. Hoy tenemos un descuento especial del 50%. ¿Te gustaría ver las recetas incluidas y asegurar tu cupo? Toca aquí para ver todos los detalles: [Tu Enlace de Afiliado]'"
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es pegar el enlace de afiliado directamente en los comentarios públicos o responder con links secos. Esto da aspecto de spam, genera desconfianza y las plataformas podrían penalizar el alcance de tu cuenta.",
                                "Otro fallo común es escribir textos gigantescos. En redes sociales la atención es mínima. Si tu mensaje es un testamento técnico, el usuario lo ignorará. Mantén el texto corto, amigable, directo al grano y utiliza saltos de línea para facilitar la lectura móvil."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: La venta automática consiste en guiar al prospecto desde un comentario público en tu video hasta su bandeja de mensajes privados, donde recibe un script persuasivo y directo con tu enlace de afiliado.",
                                "Tu acción recomendada para hoy: Redacta tu propio script de cierre adaptado al producto digital elegido en el Módulo 2. Define una palabra clave sencilla (como 'QUIERO' o 'INFO') y configúrala para responder de manera automática."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: El Script de Cierre Perfecto y Automatización",
                        "questions": [
                            {
                                "question": "¿Cuáles son los tres pasos rápidos que estructuran el 'Script de Cierre Perfecto'?",
                                "options": [
                                    "Conexión, Transformación y Llamado a la Acción.",
                                    "Características técnicas, Precio y Despedida.",
                                    "Saludo, Envío de enlace directo y Seguimiento diario.",
                                    "Presentación, Debate de objeciones y Cierre forzado."
                                ],
                                "answer": 0,
                                "explanation": "La lección detalla que la conversación amigable se guía en tres pasos: Conexión (validar interés con empatía), Transformación (presentar el beneficio principal del producto) y Llamado a la Acción (instrucción clara para dar el clic final)."
                            },
                            {
                                "question": "¿Por qué es un error grave dejar tu enlace de afiliado directamente en los comentarios públicos?",
                                "options": [
                                    "Porque disminuye el precio de comisión que te otorga Hotmart.",
                                    "Porque la gente desconfiará, parecerás un robot de spam y las plataformas podrían penalizar tu alcance.",
                                    "Porque las herramientas de automatización solo funcionan si el mensaje es extremadamente largo.",
                                    "Porque los usuarios prefieren que les envíes un correo electrónico en su lugar."
                                ],
                                "answer": 1,
                                "explanation": "Pegar el link 'seco' en comentarios públicos genera desconfianza, da aspecto de spam y las plataformas de redes sociales suelen castigar el alcance orgánico de tu cuenta por este comportamiento."
                            },
                            {
                                "question": "En el sistema de venta automática, ¿cómo se entrega el enlace de Hotmart de forma privada y al instante?",
                                "options": [
                                    "Configurando un bot que publica el enlace en las cuentas de otros creadores.",
                                    "Esperando a que el usuario te busque en tu sitio web externo sin interactuar en redes.",
                                    "Usando una palabra de activación en el contenido que una herramienta detecta para enviar el mensaje por privado.",
                                    "Enviando un correo electrónico masivo a todos los que dieron 'like' a tu video."
                                ],
                                "answer": 2,
                                "explanation": "El flujo ideal es pedir a los usuarios que comenten una palabra clave (como 'SANO' o 'CLASE') para que herramientas de automatización (como ManyChat) detecten la palabra y les envíen de inmediato el script con tu enlace de afiliado por mensaje privado."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: Tu Primer Script Automatizado de Ventas",
                        "type": "Text",
                        "question": "<p>¡Es hora de poner a trabajar la tecnología para ti! Vas a diseñar la estructura exacta de tu mensaje automatizado.</p><p>Para completar esta actividad, define el producto digital de Hotmart que promueves y entrega los siguientes puntos:</p><ul><li><strong>1. Producto y Nicho:</strong> El nombre de tu producto digital y a qué público objetivo va dirigido.</li><li><strong>2. Palabra de Activación:</strong> La palabra clave estratégica que tus seguidores comentarán en tus videos para recibir la información (ej. 'QUIERO', 'SANO').</li><li><strong>3. Tu Script de Cierre Perfecto:</strong> El mensaje privado automatizado que se enviará, respetando las 3 fases clave: <em>Conexión</em>, <em>Transformación</em> y <em>Llamado a la Acción</em> (usando tu enlace de afiliado simulado).</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: Escalado e Ingresos Recurrentes",
            "lessons": [
                {
                    "title": "La Rutina de 30 Minutos: Consistencia sin Esfuerzo",
                    "objective": "Diseñar y ejecutar un hábito diario apoyado en Inteligencia Artificial para programar contenido, responder prospectos y asegurar ventas consistentes en Hotmart.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¡Felicidades por llegar hasta aquí! Ya tienes tu sistema Faceless listo para rodar. El paso final no es trabajar más horas, sino trabajar de forma inteligente y automatizada.",
                                "Muchos cometen el error de pasar todo el día editando hasta que se cansan y abandonan. Con la Inteligencia Artificial de nuestro lado, mantener activas tus cuentas es cuestión de minutos. Aquí aprenderás a estructurar tu día para que tu negocio trabaje para ti."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para dominar la rutina de los 30 minutos diarios, usaremos el Método 10-15-5, dividido en tres bloques precisos que optimizan tu productividad al máximo.",
                                "Bloque 1 (10 minutos) - Creación Express de Contenido: Utilizando ChatGPT, generas en un instante 3 ideas de guiones de alta retención basados en los deseos y dolores de tu cliente ideal.",
                                "Bloque 2 (15 minutos) - Producción Automatizada: Llevas los guiones a CapCut. Utilizas plantillas de video stock, aplicas una voz sintética realista y generas subtítulos dinámicos de forma automática.",
                                "Bloque 3 (5 minutos) - Cosecha de Ventas: Te dedicas exclusivamente a responder comentarios utilizando plantillas de texto guardadas en tu teclado móvil para redirigir a los prospectos interesados a tu enlace de afiliado."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina tu mañana de 30 minutos promoviendo el curso de 'Pastelería Canina' como afiliado antes de comenzar tu rutina diaria de trabajo o estudio:",
                                "De 07:00 a 07:10 AM: Le pides a ChatGPT: 'Dame un guion de 15 segundos para un Reel que empiece con un gancho polémico sobre la comida para perros'. La IA te entrega un texto sobre ingredientes industriales dañinos vs snacks saludables.",
                                "De 07:10 a 07:25 AM: Abres CapCut, seleccionas un video stock rápido de un perrito feliz comiendo, pegas el texto de la IA para generar la voz artificial de 'Julio', aplicas subtítulos dinámicos y exportas el video.",
                                "De 07:25 a 07:30 AM: Entras a tu red social y respondes comentarios de tus videos anteriores usando respuestas preguardadas como: '¡Hola! Te dejé la información detallada con el 50% de descuento en el enlace de mi perfil'."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es romper la consistencia buscando la perfección de forma obsesiva. El algoritmo de TikTok e Instagram premia la regularidad diaria por encima de producciones complejas que tomen horas y que te hagan desistir a los pocos días.",
                                "Otro error común es 'subir contenido e irse'. Las comisiones se ganan y aseguran interactuando en la sección de comentarios y guiando de inmediato el impulso de compra del prospecto hacia tus enlaces."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Mantener tu negocio activo de forma paralela a tus estudios o empleo requiere disciplina de bloque de tiempo utilizando el método optimizado 10-15-5.",
                                "Tu acción recomendada para hoy: Agenda un bloque inamovible de 30 minutos para mañana. Ejecuta el proceso de guion, edición express con IA e interacción rápida de manera disciplinada."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Domina tu Rutina de Ventas de 30 Minutos",
                        "questions": [
                            {
                                "question": "¿Cómo se dividen los tres bloques de tiempo de la rutina de 30 minutos (método 10-15-5) para mantener tu máquina de ventas?",
                                "options": [
                                    "10 minutos de creación de guiones con IA, 15 minutos de edición automatizada con plantillas y 5 minutos de interacción en comentarios.",
                                    "15 minutos de diseño gráfico, 10 minutos de grabación de voz propia y 5 minutos de publicación en redes.",
                                    "10 minutos de búsqueda de hashtags, 10 minutos de edición avanzada en PC y 10 minutos de revisión de Hotmart.",
                                    "5 minutos de escritura, 20 minutos de edición de video desde cero y 5 minutos de envío de correos."
                                ],
                                "answer": 0,
                                "explanation": "El método optimizado consiste en usar 10 minutos para generar guiones con IA, 15 minutos para montar el video con plantillas en CapCut o Canva, y 5 minutos para interactuar y cosechar ventas."
                            },
                            {
                                "question": "Según la lección, ¿cuál es uno de los errores más graves que cometen los afiliados principiantes al crear contenido?",
                                "options": [
                                    "No usar micrófonos profesionales de alta gama para grabar los videos.",
                                    "Romper la consistencia buscando la perfección en lugar de publicar con regularidad usando IA.",
                                    "Publicar exactamente a la misma hora todos los días sin importar la zona horaria.",
                                    "Usar subtítulos de color blanco en lugar de colores llamativos."
                                ],
                                "answer": 1,
                                "explanation": "El algoritmo premia la regularidad. Es mucho mejor y más rentable publicar un video sencillo creado con IA de forma diaria y constante, que buscar una superproducción que te tome horas y te haga abandonar el proceso."
                            },
                            {
                                "question": "¿Por qué es un error grave la práctica de 'postear y rezar' (subir el video y cerrar la aplicación)?",
                                "options": [
                                    "Refleja que estás usando software de pago innecesario.",
                                    "Disminuye directamente el porcentaje de comisiones que te otorga el productor del curso.",
                                    "Porque las comisiones se cierran en los comentarios y mensajes privados; si no respondes rápido, el prospecto pierde el interés de compra.",
                                    "Porque la IA de Canva o CapCut requiere que vigiles la publicación activa del contenido."
                                ],
                                "answer": 2,
                                "explanation": "El dinero está en la interacción. Si un prospecto comenta con interés y no le respondes de inmediato para dirigirlo a tu enlace, perderás una venta casi asegurada porque su impulso de compra se enfriará."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña tu Plan de Acción de 30 Minutos",
                        "type": "Text",
                        "question": "<p>¡Es hora de poner a prueba la eficiencia! Vas a diseñar tu rutina diaria de 30 minutos con el Método 10-15-5.</p><p>Completa y entrega la siguiente plantilla en la caja de respuesta:</p><ul><li><strong>1. Tu Producto y Cliente Ideal:</strong> Qué producto promueves y cuál es el dolor o deseo de tu comprador.</li><li><strong>2. Bloque 1 (10 min) - Tu Prompt de Oro:</strong> El prompt exacto que usarás en ChatGPT para generar 3 guiones de 15 segundos altamente gancheros.</li><li><strong>3. Bloque 2 (15 min) - Tu Plan de Producción Express:</strong> El tipo de video de fondo que buscarás y la voz artificial o música que aplicarás.</li><li><strong>4. Bloque 3 (5 min) - Tus Respuestas de Cosecha (Quick Replies):</strong> Escribe 2 variaciones de respuestas rápidas listas para copiar, pegar y dirigir a las personas interesadas hacia tu enlace de afiliado.</li></ul>"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Primera Máquina de Ventas Faceless Activa",
        "type": "Document",
        "question": "<p>¡Felicidades por llegar al final del camino! Ahora uniremos todas las piezas para consolidar tu <strong>Máquina de Ventas Faceless</strong>. Presentarás tu plan operativo de afiliado listo para vender desde el primer día.</p><h3>Los 5 Entregables del Proyecto:</h3><p>Copia la siguiente estructura, llénala con los datos de tu estrategia y pégala para su entrega:</p><ol><li><strong>ENTREGABLE 1: El Producto Ganador (Módulo 1)</strong><br/>- Nombre del infoproducto de Hotmart elegido.<br/>- Temperatura actual, comisión y ganancia estimada en dólares por venta.<br/>- Justificación analítica de la IA sobre por qué es un 'dolor caliente'.</li><li><strong>ENTREGABLE 2: Tu Identidad Digital Secreta (Módulo 2)</strong><br/>- Nombre de usuario estratégico para tus redes (ej: @EducaTuCan).<br/>- Tu Biografía Persuasiva en 3 líneas (Gancho, Beneficio de seguirte y CTA).<br/>- El prompt exacto utilizado en Bing Image Creator o Canva para generar tu foto de perfil.</li><li><strong>ENTREGABLE 3: Tu Video de Lanzamiento (Módulo 3)</strong><br/>- Tu guion de 15 segundos exacto, dividido claramente en: <em>Gancho</em>, <em>Dolor/Solución</em> y <em>Llamado a la Acción (CTA)</em>.<br/>- Descripción del video de fondo y la voz sintética elegida en CapCut.</li><li><strong>ENTREGABLE 4: Tu Script de Cierre Automatizado (Módulo 4)</strong><br/>- Tu palabra de activación para que tus usuarios comenten (ej: 'SANO').<br/>- El mensaje privado (DM) automatizado redactado con enfoque de Conexión, Transformación y Acción que contiene tu link de afiliado.</li><li><strong>ENTREGABLE 5: Tu Plan de Consistencia de 30 Minutos (Módulo 5)</strong><br/>- El horario del día inamovible seleccionado para aplicar el método de publicación e interacción rápida de 30 minutos de forma constante.</li></ol>"
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


def build_editorjs_content(lesson_data, quiz_name=None, assignment_name=None):
    blocks = []

    blocks.append(header_block("Objetivo de la lectura", 2))
    blocks.append(paragraph_block(
        lesson_data.get("objective")
        or "Lee esta sección con una idea práctica: al terminar, tendrás una pieza concreta para avanzar en tu proyecto."
    ))

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
    set_value_if_field_exists(doc, "body", "")
    set_value_if_field_exists(doc, "content", build_editorjs_content(lesson_data, quiz_name, assignment_name))

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

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
