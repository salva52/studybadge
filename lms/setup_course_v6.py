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
    "category": "Negocios Digitales e Inteligencia Artificial",
    "title": "Web Start: Crea y Vende Páginas Web de Alto Impacto con IA Gratuita",
    "short_introduction": "Domina la creación y venta de sitios web profesionales utilizando asistentes de IA gratuitos, sin tocar código complejo ni pagar herramientas costosas.",
    "description": "<p>Descubre el método definitivo para diseñar, personalizar y publicar sitios web profesionales a costo cero. En este curso práctico aprenderás a dominar la Inteligencia Artificial para generar código real y desplegar proyectos en minutos, transformando esta habilidad técnica en un negocio digital altamente rentable.</p><ul><li><strong>Autonomía total:</strong> Crea páginas web modernas sin depender de costosas suscripciones mensuales como Webflow o Lovable.</li><li><strong>Control de código:</strong> Entiende y edita el código generado por la IA para personalizar cada detalle al gusto de tu cliente.</li><li><strong>Negocio llave en mano:</strong> Implementa un plan de acción directo para empaquetar, ofrecer y vender tus servicios de diseño web inmediatamente.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza comprensión, aplicación real, claridad y creatividad antes que perfección técnica. Valora respuestas naturales, ejemplos útiles y esfuerzo real. Penaliza respuestas vacías, copiadas, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, qué mejorar, nota final y estado: Aprobado si es 7 o más, Desaprobado si es menor a 7.",
    "chapters": [
        {
            "title": "Módulo 1: El Prompt Maestro: Diseña tu Web con Inteligencia Artificial",
            "lessons": [
                {
                    "title": "Diseño de Prompts de Alta Conversión: Estructura en 5 Capas",
                    "objective": "Aprender a estructurar instrucciones (prompts) de nivel profesional para que modelos de IA gratuitos como Claude generen código web limpio, moderno y funcional al primer intento.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Pedirle código a una Inteligencia Artificial sin un método claro es como jugar a la lotería: escribes una frase rápida y esperas que la IA adivine mágicamente lo que tienes en la cabeza. En el desarrollo web, este enfoque genera frustración, diseños desalineados y código obsoleto.",
                                "Tu nuevo superpoder no consiste en memorizar código, sino en comunicarte como un Director de Tecnología (CTO). Aprenderás la estructura exacta para que Claude actúe como un desarrollador frontend senior, entregándote páginas web profesionales, responsivas y listas para producción a costo cero."
                            ]
                        },
                        {
                            "heading": "La Estructura de 5 Capas",
                            "paragraphs": [
                                "Para obtener un sitio web profesional al primer intento, tu prompt debe seguir una estructura estricta de cinco niveles:",
                                "1. Rol: Le indicamos a la IA que actúe como un Diseñador UX/UI y Desarrollador Frontend Senior experto en conversión.",
                                "2. Contexto: Explicamos qué negocio es, quién es su cliente ideal y qué acción queremos que realice el usuario en la web.",
                                "3. Stack Tecnológico: Ordenamos usar HTML5 puro, Tailwind CSS (cargado mediante CDN) y JavaScript nativo. Tailwind CSS es clave para diseñar de forma moderna escribiendo clases directamente en el HTML, sin configurar servidores ni archivos CSS externos.",
                                "4. Anatomía del Sitio: Listamos detalladamente las secciones requeridas (Hero con llamado a la acción, grid de servicios, beneficios, testimonios y formulario de contacto).",
                                "5. Estilo Visual: Especificamos la paleta de colores (ej. negro mate, acentos verde lima) y exigimos un diseño 100% responsivo."
                            ]
                        },
                        {
                            "heading": "Plantilla del Prompt Maestro",
                            "paragraphs": [
                                "Copia y adapta esta estructura para tus proyectos:",
                                "Actúa como un Diseñador UX/UI y Desarrollador Frontend Senior. Crea una página web de una sola página (Landing Page) profesional, moderna y de alta conversión para un [negocio, ej: Consultorio Dental Premium]. El objetivo principal es que el usuario [acción, ej: agende una cita].",
                                "Tecnologías requeridas: Genera un único archivo HTML completo. Utiliza Tailwind CSS mediante su CDN oficial en el head para los estilos. No uses CSS externo. Asegúrate de que el diseño sea totalmente adaptativo (mobile-first).",
                                "Estructura de la página: 1. Navegación moderna con logo y botón de contacto. 2. Sección Hero: título persuasivo, subtítulo, dos botones de llamado a la acción (CTA) y espacio para una imagen ilustrativa. 3. Servicios: grid de 3 tarjetas con efectos hover. 4. Prueba Social: 3 testimonios con avatares. 5. Pie de página con enlaces de contacto.",
                                "Estilo visual: Usa una paleta de colores [ej: azul profundo, blanco y detalles en cian brillante]. Aplica esquinas redondeadas (rounded-lg/xl) y transiciones suaves en botones. Devuelve únicamente el código HTML completo listo para guardar."
                            ]
                        },
                        {
                            "heading": "Errores comunes a evitar",
                            "paragraphs": [
                                "El error más común es el 'Prompting Perezoso': instrucciones cortas como 'hazme una web para una pizzería'. La IA creará un sitio genérico y aburrido.",
                                "Otro error es no especificar el Stack Tecnológico. Si no aclaras que use Tailwind CSS por CDN, la IA podría inventarse archivos CSS separados que no sabrás cómo vincular.",
                                "Finalmente, evita pedir un sitio de 10 páginas de golpe. Es mucho más inteligente comenzar con una estructura sólida de una sola página (landing page), pulirla y luego añadir más secciones de forma modular."
                            ]
                        },
                        {
                            "heading": "Acción recomendada de la lección",
                            "paragraphs": [
                                "La precisión es la clave de la agilidad. Estructurar tus prompts definiendo el rol, el stack y la anatomía garantiza un resultado profesional inmediato.",
                                "Tu acción para hoy: Abre Claude.ai (la versión gratuita), adapta el 'Prompt Maestro' para un negocio real de tu zona (cafetería, gimnasio o consultorio) y genera el código. Cópialo, guárdalo en tu computadora como 'index.html' y ábrelo en tu navegador para ver nacer tu primera web."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Domina el Arte de los Prompts Maestros",
                        "questions": [
                            {
                                "question": "¿Cuáles son las cinco capas que debe seguir la estructura de tu prompt para obtener un sitio web profesional al primer intento?",
                                "options": [
                                    "Rol, Contexto, Stack Tecnológico, Anatomía del Sitio y Estilo Visual.",
                                    "Idea, Presupuesto, Estructura, Paleta de Colores y Hosting.",
                                    "Introducción, Objetivos, Programación, Pruebas y Lanzamiento.",
                                    "Rol, Audiencia, Base de Datos, Servidor y Dominio de Internet."
                                ],
                                "answer": 0,
                                "explanation": "La lección detalla que para guiar a la IA con precisión milimétrica debemos definir estrictamente estas cinco capas en nuestro prompt."
                            },
                            {
                                "question": "¿Por qué es clave ordenar a la IA que use Tailwind CSS mediante su CDN oficial en el Stack Tecnológico?",
                                "options": [
                                    "Porque obliga a la IA a generar archivos CSS externos que luego debemos subir a un servidor de pago.",
                                    "Porque permite diseñar de forma ultra moderna escribiendo clases directamente en el HTML, sin configurar archivos externos.",
                                    "Porque es el único framework que permite que la página web sea responsiva y se adapte a dispositivos móviles.",
                                    "Porque es un lenguaje de programación que reemplaza por completo a JavaScript nativo."
                                ],
                                "answer": 1,
                                "explanation": "Tailwind CSS por CDN nos permite aplicar estilos modernos directamente en las clases del HTML, logrando un desarrollo ágil, limpio y a coste cero."
                            },
                            {
                                "question": "Para evitar frustraciones, ¿cómo recomienda la lección abordar el desarrollo de un sitio web con la IA en lugar de pedirle 10 páginas de golpe?",
                                "options": [
                                    "Comenzar con una landing page sólida de una sola página, pulirla y luego añadir más páginas de manera modular.",
                                    "Escribir prompts muy cortos como 'hazme una web para una pizzería' y dejar que la IA adivine el resto.",
                                    "Pedirle que programe todo el sitio web completo de inmediato para ahorrar tiempo de conversación.",
                                    "Usar múltiples herramientas de IA de pago a la vez para que cada una programe una sección diferente."
                                ],
                                "answer": 0,
                                "explanation": "Es mucho más inteligente y efectivo estructurar, pulir y validar primero una landing page de una sola página antes de solicitar secciones adicionales de forma modular."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primer Prompt Maestro en Acción",
                        "type": "Text",
                        "question": "<p>¡Ha llegado el momento de activar tu nuevo superpoder! En esta actividad práctica vas a redactar tu primer <strong>Prompt Maestro</strong>, generarás el código con IA y evaluarás el resultado.</p><p><strong>Instrucciones:</strong></p><ol><li><strong>Elige un negocio:</strong> Puede ser una cafetería de especialidad, un gimnasio de barrio, una estética canina o un consultorio de psicología.</li><li><strong>Escribe tu Prompt Maestro:</strong> Utiliza la estructura de 5 capas aprendida (Rol, Contexto, Stack con HTML/Tailwind CDN, Anatomía del sitio y Estilo Visual) y adáptala a tu negocio elegido.</li><li><strong>Pon a prueba la IA:</strong> Introduce tu prompt en Claude (u otra IA gratuita) para obtener el código. Pruébalo guardándolo como un archivo con extensión <code>index.html</code> en tu computadora y abriéndolo con tu navegador web.</li></ol><p><strong>Entregable requerido:</strong></p><ul><li><strong>Parte 1:</strong> El prompt de 5 capas completo que redactaste y enviaste a la IA.</li><li><strong>Parte 2:</strong> Una breve reflexión (de 3 a 5 líneas) sobre el resultado visual obtenido y qué cambio específico le pedirías a la IA en una segunda interacción para pulir el diseño.</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: Workspace a Costo Cero: Claude y Antigravity",
            "lessons": [
                {
                    "title": "Configura tu Workspace en 5 Minutos: De la Idea al Código En Vivo",
                    "objective": "Configurar tu primer entorno de desarrollo 100% gratuito conectando la potencia de Claude con la visualización ágil de Antigravity para ver tus ideas publicadas al instante.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Para lanzar un proyecto web ya no necesitas pagar suscripciones de 20 o 30 dólares mensuales. En esta lección vamos a romper esa barrera configurando un entorno de trabajo profesional y completamente gratuito.",
                                "Usaremos dos herramientas espectaculares: Claude, la IA más precisa para escribir código limpio, y Antigravity.dev, un entorno de desarrollo ágil y visual que te permite ver tus cambios en tiempo real sin instalar nada en tu computadora. Pasarás de una idea a una página web interactiva en cuestión de minutos."
                            ]
                        },
                        {
                            "heading": "La Conexión de Herramientas",
                            "paragraphs": [
                                "Nuestra estrategia se basa en dos pilares independientes pero conectados de forma ágil:",
                                "Claude actúa como nuestro arquitecto e ingeniero de software. Genera la estructura (HTML), los estilos (Tailwind CSS) y la interactividad (JavaScript). Su código destaca por ser semántico, ordenado y optimizado para diseño.",
                                "Antigravity.dev es nuestro lienzo de visualización y despliegue rápido. Es un editor web gratuito que renderiza código al instante. Simplemente copiamos el código optimizado de Claude, lo pegamos en Antigravity y observamos el resultado en vivo. Esto te da total independencia de los constructores visuales cerrados."
                            ]
                        },
                        {
                            "heading": "Paso a Paso Práctico",
                            "paragraphs": [
                                "Sigue este flujo de trabajo para maquetar tu idea:",
                                "1. Abre Claude (claude.ai) y solicita: 'Genera el código de una sola página para una landing page de consultoría digital. Incluye un diseño moderno con Tailwind CSS, héroe llamativo, servicios con iconos, formulario de contacto y botón flotante. Devuelve un único archivo HTML completo.'",
                                "2. Copia el código entregado por Claude usando el botón 'Copy' del bloque de código.",
                                "3. Abre otra pestaña, ingresa a Antigravity.dev y crea un nuevo lienzo en blanco (Blank Canvas).",
                                "4. Pega el código en el editor de Antigravity. En el panel derecho verás tu landing page interactiva en tiempo real, lista para modificar y testear."
                            ]
                        },
                        {
                            "heading": "Solución a Retos Comunes",
                            "paragraphs": [
                                "Código incompleto: Si el código es muy largo, Claude puede detenerse. Escríbele: 'Continúa desde donde te quedaste' para que complete el archivo sin perder la estructura anterior.",
                                "Imágenes que no cargan: Al usar imágenes genéricas, pueden aparecer enlaces rotos. Asegúrate de pedirle a Claude que use URLs de Unsplash o marcadores de posición (placeholders) temporales.",
                                "Miedo a la edición: Realiza cambios pequeños directamente en el panel de código de Antigravity (como modificar textos o clases de color). Es la forma más rápida de ganar confianza técnica."
                            ]
                        },
                        {
                            "heading": "Acción recomendada de la lección",
                            "paragraphs": [
                                "La combinación de Claude y Antigravity te da una velocidad de desarrollo increíble y total independencia técnica sin tocar tu tarjeta de crédito.",
                                "Tu acción para hoy: Genera una landing page básica en Claude usando el ejemplo práctico, pégala en Antigravity.dev, cambia manualmente el título principal en el código y observa cómo se actualiza al instante."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu Workspace a Costo Cero",
                        "questions": [
                            {
                                "question": "¿Qué rol cumple cada una de las dos herramientas recomendadas en esta estrategia de desarrollo rápido?",
                                "options": [
                                    "Claude genera la estructura, estilos e interactividad (código), mientras que Antigravity funciona como el lienzo de visualización y despliegue en tiempo real.",
                                    "Antigravity crea el código de forma automática y Claude sirve únicamente para registrar el dominio de la web.",
                                    "Claude funciona como un servidor de base de datos de pago y Antigravity es un editor de imágenes en la nube.",
                                    "Ambas herramientas hacen exactamente lo mismo y es necesario pagar suscripciones en las dos para poder conectarlas."
                                ],
                                "answer": 0,
                                "explanation": "La lección define a Claude como el arquitecto que escribe el código (HTML, CSS y JS) y a Antigravity como el entorno web gratuito para visualizar y desplegar el resultado al instante."
                            },
                            {
                                "question": "Si el código generado por Claude se detiene antes de terminar por ser demasiado largo, ¿cuál es la solución recomendada?",
                                "options": [
                                    "Reiniciar la computadora y volver a escribir el prompt desde cero.",
                                    "Escribirle a Claude el mensaje: 'Continúa desde donde te quedaste' para que complete la estructura.",
                                    "Copiar el código incompleto y pagar una herramienta de diseño visual para que lo repare.",
                                    "Borrar todo y cambiar a otro asistente de inteligencia artificial de pago."
                                ],
                                "answer": 1,
                                "explanation": "Para solucionar el código cortado, basta con pedirle a Claude que continúe desde donde se quedó para que complete el archivo sin perder la estructura."
                            },
                            {
                                "question": "De acuerdo con la lección, ¿cómo se debe resolver el problema de las imágenes rotas o invisibles en tu prototipo?",
                                "options": [
                                    "Subiendo las imágenes directamente a la terminal de comandos de tu computadora.",
                                    "Eliminando todas las secciones de imágenes del código para evitar errores visuales.",
                                    "Asegurándote de usar URLs de imágenes reales de servicios gratuitos como Unsplash o pidiendo a Claude marcadores de posición temporales.",
                                    "Comprando un hosting de imágenes premium antes de pegar el código en Antigravity."
                                ],
                                "answer": 2,
                                "explanation": "Para evitar imágenes rotas, la lección aconseja usar enlaces reales de plataformas gratuitas como Unsplash o solicitar marcadores de posición (placeholders) visuales y temporales a Claude."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primera Landing Page 'Costo Cero' en Vivo",
                        "type": "Text",
                        "question": "<p>¡Es hora de ensuciarse las manos y ver tu primera creación en vivo sin gastar un solo centavo! Diseñarás la landing page de un negocio local ficticio: <strong>'Café de Especialidad Origen'</strong>, conectarás Claude con Antigravity, y harás tu primera modificación manual de código.</p><p><strong>Instrucciones Paso a Paso:</strong></p><ul><li><strong>Paso 1: Generación con Claude.</strong> Pídele a Claude que genere el código con este prompt:<br><em>'Genera el código de una sola página para una cafetería de especialidad llamada Café Origen. Debe tener un diseño moderno usando Tailwind CSS, sección héroe con fondo oscuro, listado de 3 productos destacados con precios, formulario de reserva de mesa interactivo y botón de WhatsApp flotante. Usa imágenes reales de Unsplash. Devuelve un único archivo HTML con CSS y JS embebidos.'</em></li><li><strong>Paso 2: Visualización.</strong> Copia el código, ve a <a href='https://antigravity.dev' target='_blank'>Antigravity.dev</a>, crea un lienzo en blanco (Blank Canvas) y pega el código. Confirma que se visualice correctamente en el panel derecho.</li><li><strong>Paso 3: Edición Manual.</strong> Busca en el código y realiza dos cambios sencillos: 1. Cambia el título principal por uno personalizado (ej. 'Café Origen: El combustible de tus mañanas'). 2. Modifica un color de fondo de un botón de Tailwind directamente en el código (ej. cambia una clase como <code>bg-amber-600</code> por <code>bg-stone-800</code>).</li></ul><p><strong>Entregable requerido:</strong></p><ol><li>El código HTML final modificado en tu editor de Antigravity.</li><li>Un breve comentario (de 2 o 3 líneas) explicando cuáles fueron los cambios manuales que realizaste y cómo afectaron al diseño visual de la página.</li></ol>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: Edición de Código Inteligente y Estilos Pro",
            "lessons": [
                {
                    "title": "Cirugía Web: Modificaciones Milimétricas con Tailwind y Claude",
                    "objective": "Aprenderás a identificar componentes específicos de tu código y a guiar a la IA para realizar modificaciones visuales y funcionales precisas, sin dañar el resto de tu página web.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Para crear páginas web profesionales no necesitas memorizar miles de líneas de código, sino aprender a alterarlo con precisión quirúrgica. En lugar de reescribir un sitio completo desde cero cuando algo no nos gusta, intervenimos únicamente la zona que requiere mejoras.",
                                "Al trabajar con Claude, tu mayor ventaja es aislar componentes específicos (como un menú, un botón o una tarjeta de producto), pedirle a la IA que lo rediseñe o le agregue interactividad, y volver a colocarlo en el archivo de forma limpia. Esto te otorga un control total sobre tus entregables sin depender de plataformas cerradas de suscripción."
                            ]
                        },
                        {
                            "heading": "El Enfoque Modular",
                            "paragraphs": [
                                "Tu página web se compone de bloques modulares e independientes (header, hero, services, testimonials, footer). Si deseas cambiar el diseño o comportamiento de una sección, nunca le envíes a la IA el código completo de 2,000 líneas. Solo copia y trabaja sobre el fragmento de ese componente.",
                                "Al solicitar un cambio, sigue este orden en tu instrucción: primero, dale el fragmento de código actual; segundo, detalla la modificación exacta (visual o funcional); y tercero, pídele que devuelva exclusivamente el bloque editado con comentarios explicativos. Este método evita que la IA sufra pérdidas de memoria o recorte partes del archivo original."
                            ]
                        },
                        {
                            "heading": "Ejemplo Práctico de Cirugía",
                            "paragraphs": [
                                "Imagina que tienes un botón de contacto básico y quieres transformarlo en un elemento moderno con degradado y movimiento dinámico.",
                                "Tomas el fragmento HTML del botón actual: `<button class='bg-blue-500 text-white p-2'>Enviar</button>` y le escribes a Claude: 'Tengo este botón. Transfórmalo usando Tailwind CSS para que tenga un fondo degradado de azul a morado, bordes redondeados, sombra elegante al pasar el cursor (hover) y una transición suave. Devuélveme solo la línea de código modificada.'",
                                "La IA te devolverá una clase optimizada lista para copiar y pegar en tu proyecto. Al refrescar tu navegador, verás un botón interactivo de alta calidad visual."
                            ]
                        },
                        {
                            "heading": "Errores Críticos a Evitar",
                            "paragraphs": [
                                "No hacer respaldos: Nunca edites un archivo sin antes duplicarlo. Si un cambio sugerido rompe el diseño, tener un respaldo te permite restaurar el sitio al instante.",
                                "Instrucciones ambiguas: Decirle a la IA 'haz que mi página se vea moderna' da resultados impredecibles. Sé específico: define colores, espaciados, fuentes y referencias visuales.",
                                "Etiquetas rotas: Al pegar el código editado, ten extremo cuidado de no eliminar accidentalmente etiquetas de apertura o cierre (como `<div>` o `</div>`). Una etiqueta mal cerrada deformará toda la estructura visual."
                            ]
                        },
                        {
                            "heading": "Acción recomendada de la lección",
                            "paragraphs": [
                                "Personalizar tu sitio con IA requiere criterio visual, no años de estudio de programación. La edición modular te permite experimentar de forma rápida y segura.",
                                "Tu acción para hoy: Selecciona una sección de la página que estás construyendo (como el pie de página o un botón), pídele a Claude que le aplique una mejora visual específica (como transiciones suaves de color o sombras) y reemplaza el fragmento de código para validar los cambios."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Domina la Cirugía Web Guiada con IA",
                        "questions": [
                            {
                                "question": "¿En qué consiste el 'enfoque modular' recomendado para editar tu web con Inteligencia Artificial?",
                                "options": [
                                    "En aislar y trabajar con bloques independientes (como un menú o un botón) en lugar de entregarle todo el código de la web a la IA.",
                                    "En dividir tu sitio web en múltiples páginas independientes para que carguen más rápido en el navegador.",
                                    "Eniseñar la página web utilizando únicamente constructores visuales con suscripciones mensuales.",
                                    "En memorizar bloques de código específicos para programar manualmente sin ayuda de asistentes virtuales."
                                ],
                                "answer": 0,
                                "explanation": "El enfoque modular consiste en trabajar con bloques independientes (como el encabezado o un botón) y enviarle a la IA únicamente el fragmento de código correspondiente a esa sección para evitar que se pierda información."
                            },
                            {
                                "question": "¿Cuál es el error más grave que puedes cometer al realizar cambios en tu código?",
                                "options": [
                                    "Utilizar colores degradados modernos en botones de llamada a la acción.",
                                    "No realizar una copia de seguridad o respaldo de tus archivos HTML o CSS antes de editar.",
                                    "Pedirle a la IA que devuelva únicamente el fragmento de código modificado.",
                                    "Trabajar con asistentes de inteligencia artificial gratuitos en lugar de herramientas de pago."
                                ],
                                "answer": 1,
                                "explanation": "El error más grave es modificar tu código directamente sin guardar un respaldo. Duplicar tu archivo antes de editar te permite restaurar tu página al instante si algo se rompe."
                            },
                            {
                                "question": "Para comunicarte con la IA con precisión y evitar que omita partes del código original, ¿qué estructura debes seguir?",
                                "options": [
                                    "Escribir una idea general, indicando que quieres que todo el sitio web sea más moderno.",
                                    "Entregarle las 2,000 líneas de tu sitio y pedirle que encuentre y modifique el pie de página.",
                                    "Proporcionar el fragmento actual, detallar el cambio visual o funcional deseado y pedir que devuelva solo el bloque modificado con comentarios.",
                                    "Pedirle que rediseñe la estructura completa de la página desde cero usando un lenguaje diferente."
                                ],
                                "answer": 2,
                                "explanation": "La estructura ideal es proporcionarle el fragmento actual, indicarle detalladamente el cambio (por ejemplo, con clases de Tailwind CSS) y solicitarle que devuelva solo ese bloque modificado con comentarios explicativos."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Cirugía Estética a un Botón de Suscripción",
                        "type": "Text",
                        "question": "<p>¡Es hora de realizar tu primera <strong>cirugía estética web</strong>! Aplicarás el enfoque modular para transformar un componente plano en una pieza de diseño interactiva y profesional usando la IA.</p><h3>El Código Base</h3><p>Imagina que tienes este bloque HTML plano:</p><pre><code>&lt;div class='p-6 bg-gray-100 rounded-lg'&gt;\n  &lt;h3 class='text-lg font-bold mb-2'&gt;Únete a nuestro Newsletter&lt;/h3&gt;\n  &lt;p class='text-sm text-gray-600 mb-4'&gt;Recibe actualizaciones semanales.&lt;/p&gt;\n  &lt;input type='email' placeholder='Tu correo aquí' class='border p-2 rounded mr-2'&gt;\n  &lt;button class='bg-gray-500 text-white p-2 rounded'&gt;Suscribirse&lt;/button&gt;\n&lt;/div&gt;</code></pre><h3>Instrucciones de la Actividad</h3><ol><li><strong>Paso 1: Redacta tu Prompt.</strong> Diseña una instrucción usando el método aprendido: pásale solo este bloque a la IA, detalla mejoras específicas para el botón (color vibrante, bordes rounded, sombras, efecto de escala al pasar el cursor) y pídele que devuelva <strong>únicamente el código modificado</strong>.</li><li><strong>Paso 2: Ejecuta y verifica.</strong> Pasa el prompt por tu IA, revisa el código y comprueba que mantenga todas las etiquetas HTML correctamente cerradas.</li></ol><h3>Entregable Requerido</h3><ul><li><strong>1. El prompt exacto</strong> que utilizaste para guiar a la IA.</li><li><strong>2. El código HTML final modificado</strong> devuelto por la IA.</li><li><strong>3. Tu reflexión (2-3 líneas):</strong> ¿Por qué trabajar de manera modular es más rápido y seguro que pedirle a la IA que reescriba toda tu página?</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Lanzamiento Express: Tu Web en Vivo Gratis",
            "lessons": [
                {
                    "title": "Despliegue con un Clic: Servidores Globales con Netlify Drop",
                    "objective": "Subir tu sitio web a internet de forma totalmente gratuita, segura y en menos de cinco minutos, obteniendo un enlace público profesional para compartir con tus clientes.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Has estructurado tu página con Claude, pulido los estilos y revisado el diseño interactivo. Ahora es momento de la verdad: poner la web en internet para que cualquier cliente pueda acceder a ella. Olvídate de configuraciones de hosting complejas o pagos mensuales elevados.",
                                "Plataformas de nivel empresarial como Netlify o Vercel ofrecen planes gratuitos sumamente robustos. Permiten publicar tu sitio con el simple gesto de 'arrastrar y soltar', entregándote un certificado SSL de seguridad (el candado verde HTTPS) y una velocidad de carga óptima sin costo alguno."
                            ]
                        },
                        {
                            "heading": "El Poder de las Plataformas Estáticas",
                            "paragraphs": [
                                "Netlify es la opción ideal para nuestro modelo de negocio de costo cero. Al alojar proyectos estáticos (HTML, CSS, JS), elimina por completo la necesidad de pagar servidores por cada cliente que captes. Puedes hospedar múltiples proyectos bajo sus subdominios gratuitos (ej. tusitio.netlify.app) o conectar un dominio propio comprado por tu cliente.",
                                "Gracias a su red CDN global, tus archivos se copian en servidores de todo el mundo. Esto garantiza que la web cargue instantáneamente desde cualquier país. Además, si conectas tu proyecto con GitHub, cualquier actualización que realices en el código se reflejará automáticamente en vivo."
                            ]
                        },
                        {
                            "heading": "Despliegue Paso a Paso con Netlify Drop",
                            "paragraphs": [
                                "Sigue esta guía rápida de 3 minutos para lanzar tu web:",
                                "1. Prepara tu carpeta: Agrupa todos tus archivos de diseño (index.html, imágenes, carpetas de recursos) en un único directorio en tu computadora. El archivo principal de entrada debe llamarse estrictamente 'index.html'.",
                                "2. Accede a Netlify: Crea una cuenta gratuita en netlify.com.",
                                "3. Sube tu proyecto: Ve a la sección 'Sites' de tu panel, desplázate hasta el final y localiza el recuadro que dice 'Netlify Drop' ('Drag and drop your site folder here').",
                                "4. Arrastra y suelta: Mueve la carpeta de tu proyecto al recuadro. En segundos obtendrás un enlace público automático.",
                                "5. Personaliza la URL: Entra a 'Site configuration' -> 'Change site name' y renombra el subdominio por un nombre profesional adaptado a tu cliente (ej. 'clinica-fisiovida.netlify.app')."
                            ]
                        },
                        {
                            "heading": "Errores comunes de publicación",
                            "paragraphs": [
                                "Error de Página No Encontrada (404): Ocurre si el archivo principal no se llama 'index.html' (en minúsculas) o si está guardado dentro de subcarpetas en lugar de la raíz. El servidor siempre buscará 'index.html' para iniciar la navegación.",
                                "Imágenes rotas en vivo: Sucede al utilizar rutas locales absolutas (como apuntar a archivos en tu disco C:) en lugar de rutas relativas (ej. 'images/foto.jpg'). Siempre verifica tus rutas antes de subir la carpeta."
                            ]
                        },
                        {
                            "heading": "Acción recomendada de la lección",
                            "paragraphs": [
                                "La publicación web ya no es una barrera técnica ni financiera. Con Netlify Drop, dispones de una infraestructura global de alta velocidad y costo cero que maximiza tus márgenes de ganancia.",
                                "Tu acción para hoy: Agrupa la landing page estructurada en los módulos anteriores, comprueba que el archivo sea 'index.html', súbelo a Netlify Drop, personaliza su URL y verifica su excelente velocidad de carga en tu teléfono móvil."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz corto: Despliega tu web como un profesional",
                        "questions": [
                            {
                                "question": "¿Cómo debe llamarse estrictamente el archivo principal de tu sitio web para evitar el error 'Page Not Found (404)' al subirlo a Netlify?",
                                "options": [
                                    "home.html",
                                    "index.html",
                                    "inicio.html",
                                    "main.html"
                                ],
                                "answer": 1,
                                "explanation": "El servidor de Netlify busca por defecto el archivo 'index.html' (todo en minúsculas) para saber qué página mostrar primero. Si usas nombres como 'inicio.html' o 'home.html', el sistema arrojará un error 404."
                            },
                            {
                                "question": "¿Por qué tu sitio web carga de forma instantánea en cualquier parte del mundo al usar Netlify o Vercel?",
                                "options": [
                                    "Porque utilizan una red de distribución de contenido (CDN) global que copia tus archivos en servidores de todo el mundo.",
                                    "Porque las plataformas reducen la calidad de tu código y eliminan los archivos CSS pesados.",
                                    "Porque obligan a los visitantes a instalar un software de aceleración en sus navegadores.",
                                    "Porque solo permiten subir páginas web de una sola línea de texto."
                                ],
                                "answer": 0,
                                "explanation": "Gracias a su Red de Distribución de Contenido (CDN) global, los archivos de tu web se replican en servidores ubicados en todo el planeta, asegurando que carguen de inmediato sin importar de dónde se conecte el usuario."
                            },
                            {
                                "question": "¿Qué error provoca que las imágenes o estilos de tu web se rompan al publicarla en internet?",
                                "options": [
                                    "Usar un subdominio personalizado gratuito en lugar de un dominio propio comprado.",
                                    "Registrarse en Netlify usando un correo electrónico en lugar de una cuenta de GitHub.",
                                    "Utilizar rutas absolutas (como apuntar a tu disco C:) en lugar de rutas relativas (como 'images/foto.jpg').",
                                    "Arrastrar la carpeta de tu sitio web directamente a la sección Netlify Drop."
                                ],
                                "answer": 2,
                                "explanation": "Si usas rutas absolutas que apuntan a tu disco local, el navegador de tus usuarios buscará los archivos en sus propias computadoras en lugar de en internet. Usar rutas relativas garantiza que Netlify encuentre y cargue todos tus recursos correctamente."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: ¡Lanza tu web en vivo y personaliza tu enlace!",
                        "type": "Text",
                        "question": "<p>¡Tu sitio web dejará de vivir solo en tu computadora! Lo publicarás en internet de forma gratuita para que sea accesible desde cualquier dispositivo.</p><p><strong>Pasos para la actividad:</strong></p><ol><li><strong>Revisión local:</strong> Revisa tu carpeta de proyecto. Confirma que tu archivo principal sea <code>index.html</code> (en minúsculas) y que las imágenes tengan rutas relativas.</li><li><strong>Despliegue:</strong> Entra a <a href='https://app.netlify.com/drop' target='_blank'>Netlify Drop</a> y arrastra la carpeta del proyecto. Espera unos segundos a que se genere tu URL.</li><li><strong>Personalización:</strong> Entra a <em>Site configuration</em> &gt; <em>Change site name</em> y cambia el nombre genérico por uno limpio (ej: <code>mi-agencia-digital.netlify.app</code>).</li><li><strong>Verificación:</strong> Abre el nuevo enlace en tu móvil para comprobar que carga rápido y se adapta bien.</li></ol><p><strong>Entregable requerido:</strong></p><ul><li><strong>1. El enlace público de tu web en Netlify:</strong> (Ej: <code>https://nombre-de-tu-proyecto.netlify.app</code>)</li><li><strong>2. Check de calidad (Sí/No):</strong> ¿El archivo se llama index.html? ¿Las imágenes cargan correctamente?</li><li><strong>3. Feedback:</strong> ¿Qué ventajas encuentras en este sistema de publicación rápida frente a los hostings tradicionales?</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: Tu Agencia Web: Estrategia de Venta de 500 USD",
            "lessons": [
                {
                    "title": "El Plan de 7 Días: Cómo Cerrar tu Primer Cliente de 500 USD",
                    "objective": "Aprender y ejecutar un método de prospección y venta rápida de 7 días para cerrar tu primer servicio de diseño web por 500 USD, utilizando prototipos rápidos creados con IA sin costo de software.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Dominar el aspecto técnico es solo la mitad del camino. El paso decisivo es transformar esa habilidad en un negocio rentable y constante. Cobrar 500 USD por una landing page o un sitio corporativo es una excelente tarifa de entrada para ti y una inversión de bajo riesgo para cualquier negocio local.",
                                "Dado que desarrollas sin costos fijos de software o plantillas costosas, tu margen de ganancia es prácticamente del 100%. Implementarás una metodología comercial práctica basada en aportar valor antes de vender."
                            ]
                        },
                        {
                            "heading": "Estrategia: Demostración de Valor Inmediata",
                            "paragraphs": [
                                "Los dueños de negocios no compran tecnologías o lenguajes de programación; compran clientes, optimización y una imagen profesional. Por ello, en lugar de enviar correos masivos fríos, usaremos un método de prospección activa basado en prototipos previos.",
                                "La hoja de ruta de 7 días se divide así:",
                                "Días 1-2: Auditoría. Identifica de 10 a 15 negocios locales (gimnasios, clínicas, consultoras) que tengan una web lenta, no adaptada a celulares o que directamente no posean un sitio pero sí una ficha de Google Maps.",
                                "Días 3-4: Prototipo Gancho. Con la ayuda de Claude, genera la sección principal (Hero) de la web para el negocio seleccionado usando su logo y colores. Te tomará menos de 30 minutos. Súbela a un hosting gratuito de Netlify.",
                                "Días 5-6: Contacto Directo. Graba un video de pantalla de 2 minutos (con herramientas gratuitas como Loom). Muestra su sitio deficiente actual y compáralo con el prototipo moderno y rápido que diseñaste. Explica los beneficios de agendamiento o velocidad de carga.",
                                "Día 7: Cierre. Agenda una sesión virtual de 15 minutos, detalla los pasos finales de desarrollo y solicita un 50% de anticipo para arrancar la entrega del proyecto."
                            ]
                        },
                        {
                            "heading": "Ejemplo de Prospección en Acción",
                            "paragraphs": [
                                "Encuentras un centro estético local llamado 'Estética Aura' con una web obsoleta de carga lenta.",
                                "Ingresas a Claude y solicitas: 'Genera el código HTML y Tailwind para la sección Hero de un centro de estética llamado Estética Aura. Usa tonos crema, tipografía refinada, botón de acción directo a WhatsApp y diseño mobile-first.'",
                                "Despliegas el resultado en Netlify en un minuto. Envías un video Loom rápido: 'Hola, equipo de Aura. Analicé su sitio web actual y vi que a sus clientes les cuesta agendar desde el celular. Diseñé este prototipo rápido que optimiza la carga y permite reservar por WhatsApp en un clic. Si les gusta, podemos construir todo el sitio web esta misma semana.' La respuesta positiva con este enfoque es altísima."
                            ]
                        },
                        {
                            "heading": "Evita los errores típicos de ventas",
                            "paragraphs": [
                                "Vender características en lugar de soluciones: Al cliente no le importa si usas Tailwind o HTML5; le importa que su negocio consiga más citas y cargue de forma instantánea.",
                                "Sobrabajar antes de cobrar: El prototipo gancho debe ser rápido y selectivo. No maquetes el sitio completo ni desarrolles todas las páginas antes de asegurar el primer abono del 50%.",
                                "Temor a mencionar la IA: No ocultes que usas herramientas de IA. Es tu ventaja comercial. Explica que gracias a tu flujo de trabajo asistido por IA puedes entregar el sitio en 5 días en vez de las 4 semanas que tarda una agencia tradicional, a un precio sumamente competitivo."
                            ]
                        },
                        {
                            "heading": "Acción recomendada de la lección",
                            "paragraphs": [
                                "El secreto de las ventas rápidas es mitigar el riesgo del cliente demostrando el valor de tu servicio antes de que paguen un centavo. Un prototipo personalizado y un video de 2 minutos marcan la diferencia comercial.",
                                "Tu acción para hoy: Elige 3 negocios reales en tu ciudad, analiza su presencia online, detecta sus puntos críticos de mejora y diseña la estructura del mensaje o video que les enviarás usando tu nuevo prototipo asistido por IA."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu primer cliente de diseño web en 7 días",
                        "questions": [
                            {
                                "question": "¿En qué consiste la estrategia de 'Demostración de Valor Inmediata' recomendada en el plan?",
                                "options": [
                                    "Enviar una propuesta formal por correo detallando el código y las licencias de software que vas a utilizar.",
                                    "Crear un prototipo interactivo de la sección Hero en menos de 30 minutos y mostrarlo en un video personalizado de 2 minutos.",
                                    "Construir la web completa de forma gratuita para que el cliente decida si quiere pagarte después de un mes.",
                                    "Llamar en frío a 50 negocios al día para ofrecerles servicios genéricos de programación."
                                ],
                                "answer": 1,
                                "explanation": "La estrategia busca captar la atención del cliente mostrándole un cambio visual real y personalizado en su propia marca mediante un video corto, sin que tú inviertas horas de trabajo innecesarias antes de cobrar."
                            },
                            {
                                "question": "Con respecto al uso de Inteligencia Artificial en tu flujo de trabajo, ¿cuál es la postura recomendada?",
                                "options": [
                                    "Ocultarlo por completo para evitar que el cliente piense que el trabajo es sencillo.",
                                    "Cobrar menos de la mitad del precio regular porque la IA hace todo el esfuerzo.",
                                    "Presentarlo abiertamente como tu ventaja competitiva para ofrecer entregas mucho más rápidas y a costos competitivos.",
                                    "Usarla solo para la redacción de textos, pero nunca para generar código o diseño."
                                ],
                                "answer": 2,
                                "explanation": "No debes temer decir que usas IA; al contrario, es tu mejor argumento para explicar por qué puedes entregar una web a medida en días en lugar de las semanas que tarda una agencia tradicional."
                            },
                            {
                                "question": "Para evitar el error común de 'trabajar de más antes de cobrar', ¿qué debes asegurar en el Día 7 del plan?",
                                "options": [
                                    "Solicitar un 50% de anticipo durante la llamada de cierre para comenzar con el desarrollo completo del sitio.",
                                    "Entregar todo el sitio terminado y esperar a que el cliente decida el monto del pago.",
                                    "Ofrecer modificaciones ilimitadas y gratuitas durante el primer año sin firmar un acuerdo.",
                                    "Pedirle al cliente que compre un hosting costoso antes de ver cualquier diseño."
                                ],
                                "answer": 0,
                                "explanation": "El plan establece que el prototipo inicial es solo un gancho rápido. Para desarrollar el sitio completo, debes cerrar el trato en la llamada del Día 7 solicitando el 50% de anticipo."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primer Cliente en 7 Días - Diseña tu Prototipo y Pitch de Alto Impacto",
                        "type": "Text",
                        "question": "<p>¡Llegó el momento de pasar de la teoría a la acción! Diseñarás la estrategia del plan de 7 días: la creación de tu <strong>Prototipo Gancho</strong> y la redacción del guion de tu <strong>Video Pitch</strong> para captar a tu primer cliente.</p><p>Elige un negocio local real o ficticio y desarrolla los siguientes 4 puntos en tu respuesta:</p><ol><li><strong>Ficha del Cliente Objetivo:</strong> Nombre, nicho y los 2 problemas principales que detectaste en su web actual (ej. no se adapta a móviles, carga lento).</li><li><strong>El Prompt del Prototipo:</strong> Escribe el prompt exacto que le darías a Claude para generar la estructura de la sección 'Hero' (portada) de este negocio con su paleta de colores sugerida y llamado a la acción.</li><li><strong>Guion del Video (Pitch de 2 minutos):</strong> Redacta lo que dirás en tu video explicativo (Loom), dividido en: <em>Gancho (30 seg)</em>, <em>Demostración de Valor (60 seg)</em> y <em>Llamado a la Acción (30 seg)</em>.</li><li><strong>Cierre de Venta:</strong> Redacta la frase exacta que usarás para presentar el precio de 500 USD (con el 50% de anticipo) y cómo explicarás el uso positivo de la IA para garantizar una entrega rápida.</li></ol>"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Primera Agencia Web - De la Idea al Despliegue y la Venta en 24 Horas",
        "type": "Document",
        "question": "<p>¡Felicidades! Has completado el recorrido teórico y práctico. En este proyecto final simularás el ciclo completo de tu agencia digital: desde el concepto de diseño y la generación de código con Inteligencia Artificial, pasando por la edición manual, publicación en vivo y la propuesta comercial de venta.</p><p>Este proyecto se convertirá en un caso de estudio real que podrás utilizar en tu portafolio para presentarte con clientes y cerrar contratos de manera inmediata.</p><h3>📋 Instrucciones Paso a Paso y Entregables</h3><p>Para aprobar de forma exitosa, debes estructurar tu documento de respuesta en los siguientes <strong>5 bloques de información</strong>:</p><h4>1. Ficha Técnica del Cliente y Diagnóstico</h4><ul><li><strong>Nombre del negocio y nicho:</strong> (Ej: 'FisioSport - Fisioterapia Deportiva').</li><li><strong>Puntos débiles detectados:</strong> Describe brevemente (2-3 líneas) qué fallas tiene su presencia digital actual o por qué necesitan urgentemente esta página web para optimizar sus ventas.</li></ul><h4>2. El Prompt Maestro de 5 Capas</h4><ul><li>Escribe el <strong>Prompt Maestro completo</strong> que redactaste y enviaste a Claude para generar la estructura de la web. Debe contener las 5 capas del método: <em>Rol, Contexto, Stack (HTML, Tailwind por CDN, JS), Anatomía del Sitio y Estilo Visual</em>.</li></ul><h4>3. Enlace Público del Sitio Web Desplegado</h4><ul><li><strong>Enlace de Netlify:</strong> Pega la URL pública y activa de tu sitio web (debe contar con un subdominio personalizado limpio, ej: <code>https://fisiosport.netlify.app</code>).</li><li><em>Asegúrate de que las imágenes (placeholders de Unsplash) carguen correctamente y el diseño sea totalmente adaptativo en dispositivos móviles.</em></li></ul><h4>4. Cirugía Web: Tu Toque de Código Personalizado</h4><ul><li>Muestra tu autonomía técnica. Copia y pega un <strong>fragmento de código específico (HTML/Tailwind)</strong> que hayas decidido modificar o mejorar manualmente en el editor de Antigravity o localmente (ej: diseño del botón, colores del menú, etc.).</li><li>Explica en 2 líneas qué cambio realizaste directamente en el código y cómo mejoró la experiencia visual del usuario.</li></ul><h4>5. El Video Pitch de Venta de 500 USD</h4><ul><li>Redacta el <strong>guion de texto completo</strong> de lo que dirías en tu video de prospección de 2 minutos (Loom). Estructúralo de la siguiente manera:<ul><li><strong>El Gancho (0:00 - 0:30):</strong> Cómo captas su atención señalando de forma profesional el problema actual de su web.</li><li><strong>La Solución y Demostración (0:30 - 1:30):</strong> Cómo les presentas tu prototipo en vivo desde tu enlace de Netlify, destacando la velocidad de carga y adaptación móvil.</li><li><strong>El Cierre y Llamado a la Acción (1:30 - 2:00):</strong> Tu propuesta para agendar una llamada breve de 15 minutos, planteando el valor de 500 USD con un 50% de anticipo y entrega rápida en 5 días gracias a tu flujo de trabajo asistido por IA.</li></ul></li></ul><p><strong>💡 Consejo de calidad del Agente 7:</strong> Sé sumamente específico, cuida la ortografía de tus guiones y diseña la landing page pensando en lo que un cliente real amaría ver para su negocio. ¡Este es el lanzamiento oficial de tu nuevo camino profesional!</p>"
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
        return None

    caption = str(image_data.get("caption") or image_data.get("alt") or "").strip()
    return {
        "type": "image",
        "data": {
            "file": {
                "url": url
            },
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
