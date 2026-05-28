import os
import sys
import json
import time
import traceback

# Corrige el sys.path para evitar shadowing al ejecutar desde apps/lms
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)

import frappe

INSTRUCTOR_NAME = "Administrator"
COURSE_DATA = {
    "category": "Marketing y Ventas con IA",
    "title": "Hotmart AI System: Automatización de Afiliados de Alto Rendimiento",
    "short_introduction": "Escala un negocio de afiliación en Hotmart optimizado con Inteligencia Artificial. Automatiza el 80% del proceso operativo, desde el análisis de mercado hasta la conversión.",
    "description": "<p>La diferencia entre un afiliado promedio y uno de alto rendimiento radica en la escala y la velocidad de ejecución. Este programa estratégico está diseñado para enseñarte a delegar el trabajo operativo, creativo y analítico en modelos de Inteligencia Artificial de última generación, permitiéndote estructurar canales de venta en Hotmart altamente rentables sin fricciones técnicas.</p><p><strong>Lo que dominarás en este programa:</strong></p><ul><li><strong>Selección y Análisis Predictivo:</strong> Identifica infoproductos de alta demanda en Hotmart utilizando prompts avanzados de inteligencia comercial.</li><li><strong>Ecosistemas de Contenido Automatizados:</strong> Diseña una infraestructura de distribución de contenidos automatizada para redes sociales, sin necesidad de exponerte ante la cámara.</li><li><strong>Copywriting y Narrativa Persuasiva:</strong> Configura sistemas de IA generativa para redactar textos de ventas de alta conversión y estructurar guiones de video altamente efectivos.</li><li><strong>Embudos de Conversión Simplificados:</strong> Implementa flujos de venta directos y eficientes que canalicen tráfico cualificado hacia tus enlaces de afiliación de forma continua.</li></ul>",
    "card_gradient": "Blue",
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza comprensión, aplicación real, claridad y creatividad antes que perfección técnica. Valora respuestas naturales, ejemplos útiles y esfuerzo real. Penaliza respuestas vacías, copiadas, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, qué mejorar, nota final y estado: Aprobado si es 7 o más, Desaprobado si es menor a 7.",
    "chapters": [
        {
            "title": "Módulo 1: Fundamentos del Afiliado Digital y la IA",
            "lesson": {
                "title": "Cómo estructurar tu negocio en Hotmart y el rol de la IA en la automatización",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Te doy la bienvenida a esta lección! Si alguna vez has pensado que para emprender en internet necesitas crear tu propio producto desde cero, pasar horas frente a una cámara o ser un experto en programación, tengo una excelente noticia para ti: eso es parte del pasado. Hoy vas a descubrir cómo estructurar un negocio digital sólido utilizando Hotmart y el poder de la Inteligencia Artificial.",
                            "El marketing de afiliados es el modelo de negocio más accesible del momento: tú recomiendas productos de otras personas (cursos online, ebooks, mentorías) y te llevas una comisión por cada venta. Pero lo verdaderamente revolucionario ocurre cuando sumamos la IA a la ecuación. En esta lección, aprenderás cómo montar la estructura de tu negocio para que la tecnología trabaje por ti, liberándote del 80% del trabajo operativo."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Para construir un negocio de afiliados exitoso con Hotmart, necesitas entender sus tres pilares fundamentales: el Producto (qué vas a vender), el Cliente Ideal (a quién se lo vas a vender) y el Sistema de Atracción (cómo vas a captar su atención). Tradicionalmente, investigar estos tres puntos tomaba semanas de análisis y redacción. Aquí es donde la Inteligencia Artificial se convierte en tu socia estratégica de bajo costo.",
                            "¿Cuál es el rol de la IA en tu negocio de afiliados? En primer lugar, la IA actúa como un analista de mercado ultrarrápido: herramientas como ChatGPT te permiten identificar los dolores, deseos e intereses de tu audiencia en segundos. En segundo lugar, automatiza la creación de contenido. Puedes generar guiones para videos rápidos (Reels, TikToks), copies para publicaciones y correos de venta sin necesidad de mostrar tu rostro ni sufrir de 'bloqueo creativo'.",
                            "El sistema funciona como un embudo automatizado. Tú utilizas la IA para crear contenido magnético que atrae visitas a tus redes sociales; luego, los diriges hacia tu enlace de afiliado de Hotmart (Hotlink). Cuando la persona compra, Hotmart entrega el producto de forma automática y deposita tu comisión en tu cuenta de inmediato. Así de simple y limpio."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Imagina que decides entrar en el nicho de la 'Repostería Saludable para Mascotas', un sector con alta demanda y poca competencia directa. Vas al mercado de Hotmart y eliges un curso de pastelería canina que te paga una comisión del 60% por venta.",
                            "En lugar de pasar días pensando qué publicar en tus redes para atraer clientes, abres ChatGPT y le das esta instrucción: 'Actúa como un experto en marketing de afiliados. Dame 5 dolores principales de los dueños de perros que quieren alimentar mejor a sus mascotas, y escribe un guion de 30 segundos para un video de TikTok que resuelva uno de esos dolores de forma rápida'.",
                            "En menos de un minuto, la IA te entregará el guion exacto con un gancho irresistible. Luego, usas una herramienta de IA de generación de voz o un editor sencillo como CapCut para crear un video usando imágenes de perritos felices comiendo galletas saludables (sin mostrar tu cara). Subes el video, pones tu enlace de Hotmart en tu biografía y listo: has creado un activo de ventas automatizado en menos de 20 minutos."
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "El primer gran error es el 'Spammasivo': andar pegando tu enlace de afiliado de Hotmart en grupos de Facebook o comentarios de Instagram sin aportar valor. Esto solo genera desconfianza y hará que bloqueen tus cuentas.",
                            "El segundo error es querer venderle a todo el mundo. Quien le vende a todos, no le vende a nadie. Usa la IA para hiper-especializarte en un público específico (por ejemplo, en lugar de 'fitness general', enfócate en 'yoga para personas con dolor de espalda').",
                            "El tercer error es confiar ciegamente en la IA sin darle tu toque personal. La IA es excelente estructurando y redactando, pero tú debes revisar el resultado final para asegurarte de que suene natural, empático y realmente conecte con las emociones de tu cliente ideal."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "En resumen: Hotmart te da el producto y la logística de cobro; la Inteligencia Artificial te da la velocidad, las ideas de contenido y la automatización; y tú pones la estrategia. No necesitas inventar la rueda, solo conectar las herramientas correctas.",
                            "Tu acción para hoy: 1. Regístrate gratis en Hotmart (si aún no lo has hecho). 2. Abre ChatGPT y escribe: 'Hola, quiero ser afiliado digital. ¿Cuáles son los 3 nichos más rentables actualmente para vender productos digitales y por qué?'. Analiza las opciones y elige la que más te llame la atención para empezar a trabajar con ella en la siguiente lección."
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: Negocio Digital con Hotmart e Inteligencia Artificial",
                    "questions": [
                        {
                            "question": "¿Cuáles son los tres pilares fundamentales para construir un negocio de afiliados exitoso con Hotmart?",
                            "options": [
                                "El Producto, la Inteligencia Artificial y la automatización de pagos.",
                                "El Producto, el Cliente Ideal y el Sistema de Atracción.",
                                "La cuenta de Hotmart, el editor CapCut y el correo electrónico.",
                                "El nicho de repostería, el guion de TikTok y el enlace de afiliado."
                            ],
                            "answer": 1,
                            "explanation": "La lección detalla que el Producto (qué vender), el Cliente Ideal (a quién vender) y el Sistema de Atracción (cómo captar su atención) son los tres pilares fundamentales de este modelo de negocio."
                        },
                        {
                            "question": "Al usar Inteligencia Artificial para la creación de contenido, ¿cuál es un error clave que debes evitar?",
                            "options": [
                                "Usar ChatGPT para estructurar y redactar guiones de video.",
                                "No mostrar tu rostro en los videos de plataformas como TikTok o Reels.",
                                "Confiar ciegamente en la IA sin darle tu toque personal para que suene natural y empático.",
                                "Elegir un nicho muy específico en lugar de intentar venderle a todo el mundo."
                            ],
                            "answer": 2,
                            "explanation": "La IA es excelente para estructurar y redactar, pero un error común es confiar ciegamente en ella sin revisar el resultado para asegurar que conecte de forma humana y empática con la audiencia."
                        },
                        {
                            "question": "¿Qué práctica incorrecta se conoce como 'Spam masivo' y puede causar el bloqueo de tus redes sociales?",
                            "options": [
                                "Pegar tu enlace de afiliado en grupos de Facebook o comentarios de Instagram sin aportar valor.",
                                "Publicar videos de 30 segundos utilizando imágenes de stock y voces generadas por IA.",
                                "Registrarse de forma gratuita en la plataforma de Hotmart para buscar productos.",
                                "Pedirle a ChatGPT que identifique los dolores y deseos del cliente ideal."
                            ],
                            "answer": 0,
                            "explanation": "El 'Spam masivo' consiste en difundir los enlaces de afiliado en comunidades digitales sin aportar ningún tipo de valor previo, lo que genera desconfianza y el bloqueo de cuentas."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Tu Primer Estudio de Mercado y Gancho con IA",
                    "type": "Text",
                    "question": "### **Objetivo de la actividad**\n¡Es hora de pasar a la acción! En esta actividad práctica vas a dar tus primeros pasos como afiliado digital utilizando la Inteligencia Artificial para investigar un nicho de mercado y estructurar tu primer gancho de ventas sin rodeos.\n\n### **Instrucciones paso a paso**\n\n1. **Elige un micro-nicho:** Piensa en un tema específico que te llame la atención. Evita temas genéricos como \"fitness\" o \"cocina\"; sé más específico, por ejemplo: \"huertos orgánicos en departamentos pequeños\" o \"repostería sin gluten para emprendedoras\".\n\n2. **Investiga con ChatGPT:** Copia y pega el siguiente prompt en ChatGPT (reemplazando lo que está entre corchetes):\n   > *\"Actúa como un experto en marketing de afiliados. Para el micro-nicho de [Inserta tu nicho aquí], identifica los 3 dolores, miedos o frustraciones más profundos de las personas interesadas en este tema.\"*\n\n3. **Crea un gancho de atención (Hook):** Elige uno de los dolores que te dio la IA y pídele que genere la apertura de un video corto con este prompt:\n   > *\"Para el dolor principal que mencionaste, escribe 2 opciones de ganchos (frases de inicio de 3 segundos) para un video corto de TikTok o Reels que capte la atención de forma inmediata.\"*\n\n4. **Aplica el toque humano (Evita el Error #3):** Lee los dos ganchos que te dio la IA. Elige uno y edítalo para que suene más natural, empático y conversacional. Quítale cualquier palabra exagerada o robótica.\n\n---\n### **Entregables que debes publicar en tu respuesta:**\n\n1. **Tu Micro-Nicho seleccionado.**\n2. **Los 3 dolores de tu cliente ideal** (copia y pega el resultado que te dio ChatGPT).\n3. **El Gancho Original de la IA vs. Tu Gancho Humanizado:** Muestra el gancho original que te dio la herramienta y, justo abajo, escribe tu versión mejorada con tu toque personal."
                }
            }
        },
        {
            "title": "Módulo 2: Selección Inteligente de Productos Ganadores",
            "lesson": {
                "title": "Uso de prompts en ChatGPT para analizar nichos millonarios y elegir el producto perfecto",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Hola! Qué gusto tenerte aquí. Si alguna vez has entrado al mercado de Hotmart, seguro te ha pasado: ves miles de productos disponibles, te abrumas con tantas opciones y terminas cerrando la pestaña sin saber cuál elegir. Es completamente normal. El miedo a equivocarte de producto y perder tu tiempo es el principal freno de los principiantes.",
                            "Hoy vamos a eliminar esa incertidumbre de raíz. No vamos a jugar a las adivinanzas ni a elegir un producto solo porque 'se ve bonito'. Vamos a usar ChatGPT como nuestro consultor de marketing personal para analizar nichos millonarios y encontrar ese producto perfecto que la gente ya está deseando comprar, incluso antes de que se lo ofrezcas."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "La clave para vender masivamente en Hotmart no está en el producto en sí, sino en el dolor que resuelve. La gente no compra un curso de 'Adiestramiento Canino' porque quiere que su perro dé la pata; lo compra porque está desesperada porque su perro destruye los muebles de la casa cuando se quedan solos. Ese es el verdadero 'dolor'.",
                            "Para encontrar estos dolores profundos sin pasar días investigando en foros, utilizamos la Inteligencia Artificial. Si tratas a ChatGPT como un simple buscador, te dará respuestas genéricas. Pero si le das instrucciones ultraespecíficas (llamadas 'prompts'), se convertirá en un detector de oportunidades de oro. Buscaremos micro-nichos: subcategorías dentro de un gran mercado donde hay mucha demanda, poca competencia y un público dispuesto a sacar la tarjeta de crédito para solucionar su problema de inmediato."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Vamos a la acción. Abre ChatGPT, copia el siguiente prompt y pégalo en el chat (puedes cambiar lo que está entre corchetes según tu interés):",
                            "\"Actúa como un experto en investigación de mercado y marketing de afiliados de Hotmart. Quiero analizar el nicho de [Alimentación Saludable para Niños de 2 a 5 años]. Por favor, entrégame un análisis detallado que incluya: 1) Los 3 dolores o frustraciones más grandes de los padres en este tema. 2) Cuál sería el formato de producto digital ideal para resolverlos (¿ebook, video-curso, recetario?). 3) Un perfil rápido del cliente ideal (Avatar) detallando su mayor deseo y su mayor miedo al comprar en internet. Dame la información en un formato claro, directo y con un tono muy práctico.\"",
                            "Al ejecutar este prompt, ChatGPT te revelará que el gran dolor de los padres no es la 'comida sana', sino la frustración de pasar horas cocinando para que el niño rechace el plato (el famoso 'niño melindroso'). Con esta información de oro, vas a Hotmart y buscas un producto específico sobre 'recetas divertidas y rápidas para niños difíciles de alimentar'. ¡Felicidades, acabas de encontrar un producto ganador con base científica!"
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "El error más grave de los afiliados novatos es el 'enamoramiento del producto'. Eligen un curso solo porque a ellos les gusta el tema (por ejemplo, historia medieval), sin validar si realmente hay un mercado dispuesto a pagar por ello. Recuerda: tú no eres tu cliente.",
                            "Otro error clásico es querer venderle a todo el mundo. Si intentas promocionar 'ejercicio en casa para todos', competirás con canales de YouTube gratuitos y gigantes del fitness. Pero si usas la IA para enfocarte en 'ejercicios de bajo impacto en casa para mujeres ocupadas mayores de 50 años', tu mensaje conectará tan fuerte que las ventas fluirán de forma natural."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "En resumen: elegir un producto ganador ya no es cuestión de suerte, sino de usar la IA para leer la mente de tus futuros clientes. Al saber exactamente qué les duele, podrás elegir el infoproducto de Hotmart que mejor resuelva esa necesidad.",
                            "Tu misión para hoy es simple y te tomará menos de 15 minutos: 1. Copia el prompt que te compartí arriba. 2. Pruébalo en ChatGPT con 2 nichos diferentes que te llamen la atención (por ejemplo: manualidades, finanzas personales, mascotas o idiomas). 3. Analiza los resultados y quédate con el que muestre los dolores más urgentes. ¡Hazlo ahora y nos vemos en la siguiente lección para empezar a crear el contenido que atraerá a tus compradores!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: Cómo encontrar tu Producto Ganador con IA",
                    "questions": [
                        {
                            "question": "Según la lección, ¿cuál es la verdadera clave para vender masivamente un producto en Hotmart?",
                            "options": [
                                "Que el producto tenga un diseño atractivo y un precio muy bajo.",
                                "Que sea un tema que te apasione personalmente a ti.",
                                "El dolor o frustración profunda que el producto resuelve para el comprador.",
                                "Intentar venderle a todo el mundo sin segmentar el mercado."
                            ],
                            "answer": 2,
                            "explanation": "La clave de las ventas masivas no está en el producto en sí, sino en el 'dolor' que resuelve. Las personas compran soluciones a sus problemas y necesidades urgentes."
                        },
                        {
                            "question": "¿En qué consiste el error del 'enamoramiento del producto' en los afiliados novatos?",
                            "options": [
                                "Elegir un curso solo porque a ti te gusta el tema, sin validar si realmente hay un mercado dispuesto a pagar por él.",
                                "Vender productos únicamente a través de canales de video gratuitos.",
                                "Gastar demasiado presupuesto en campañas de publicidad antes de elegir el nicho.",
                                "Obsesionarse con encontrar productos que tengan demasiada competencia."
                            ],
                            "answer": 0,
                            "explanation": "El enamoramiento del producto ocurre cuando el afiliado elige un tema basándose en su gusto personal (como historia medieval) en lugar de investigar si existe un público con intención de compra real."
                        },
                        {
                            "question": "¿Por qué es tan efectivo enfocarse en micro-nichos usando la Inteligencia Artificial?",
                            "options": [
                                "Porque los mercados generales no tienen productos disponibles en Hotmart.",
                                "Porque la inteligencia artificial no puede procesar temas que sean demasiado amplios.",
                                "Porque es la única forma de vender productos que no tienen reembolsos.",
                                "Porque disminuye la competencia directa y el mensaje conecta con un público específico dispuesto a pagar de inmediato."
                            ],
                            "answer": 3,
                            "explanation": "Al enfocarte en un micro-nicho (como ejercicios en casa para mujeres ocupadas mayores de 50 años), compites menos y logras que tu mensaje de marketing sea tan preciso que las ventas fluyen de forma natural."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Detector de Micro-Nichos Ganadores con IA",
                    "type": "Text",
                    "question": "¡Es hora de poner la Inteligencia Artificial a trabajar para ti! En esta actividad práctica vas a dejar de adivinar qué se vende y vas a usar el poder de ChatGPT para descubrir un producto ganador en Hotmart basado en dolores reales de las personas.\n\nSigue estos pasos para completar tu actividad y comparte tus resultados:\n\n### **Paso 1: Elige 2 Micro-nichos de tu interés**\nPiensa en dos subcategorías o temas específicos que te llamen la atención (por ejemplo: 'Adiestramiento de cachorros que se quedan solos en casa', 'Maquillaje para pieles con acné', 'Finanzas para parejas jóvenes', o 'Inglés conversacional para profesionales de tecnología').\n\n### **Paso 2: Interroga a la IA (ChatGPT)**\nAbre ChatGPT y ejecuta el siguiente prompt dos veces (una para cada micro-nicho que elegiste):\n\n> *\"Actúa como un experto en investigación de mercado y marketing de afiliados de Hotmart. Quiero analizar el nicho de [Inserta aquí tu micro-nicho]. Por favor, entrégame un análisis detallado que incluya: 1) Los 3 dolores o frustraciones más grandes de las personas en este tema. 2) Cuál sería el formato de producto digital ideal para resolverlos (¿ebook, video-curso, recetario, etc.?). 3) Un perfil rápido del cliente ideal (Avatar) detallando su mayor deseo y su mayor miedo al comprar en internet. Dame la información en un formato claro, directo y con un tono muy práctico.\"*\n\n### **Paso 3: Analiza, Compara y Elige tu Ganador**\nLee las respuestas de ChatGPT. Identifica cuál de los dos nichos tiene los **dolores más urgentes y desesperados** (es decir, dónde la gente tiene más prisa por sacar la tarjeta de crédito para solucionar su problema).\n\n---\n\n### **¿Qué debes entregar como respuesta a esta actividad?**\n\nCopia y pega la siguiente plantilla completada con tu investigación:\n\n1. **Los 2 Micro-nichos analizados:** \n   * *Micro-nicho A: [Nombre del nicho]*\n   * *Micro-nicho B: [Nombre del nicho]*\n\n2. **El Dolor Más Profundo:** Revela cuál fue el dolor más impactante o revelador que descubrió la IA para cada uno.\n   * *Dolor clave del Nicho A: [Ejemplo: El miedo a que el perro destruya el sillón nuevo]*\n   * *Dolor clave del Nicho B: [Ejemplo: La vergüenza de hablar en público en las reuniones de trabajo]*\n\n3. **Tu Elección Ganadora y Justificación:** ¿Con cuál de los dos nichos te vas a quedar para buscar un producto en Hotmart y por qué consideras que su dolor es más urgente de resolver?\n\n4. **Tu Criterio de Búsqueda en Hotmart:** Escribe exactamente qué palabras clave o término de búsqueda vas a escribir en el buscador del mercado de Hotmart para encontrar el producto ideal que resuelva este problema (ejemplo: 'Adiestramiento canino ansiedad por separación' o 'Inglés para call centers')."
                }
            }
        },
        {
            "title": "Módulo 3: Fábrica de Contenido Viral Sin Rostro",
            "lesson": {
                "title": "Creación masiva de videos y guiones persuasivos utilizando herramientas de IA generativa",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Bienvenido a uno de los módulos más transformadores de este entrenamiento! Si alguna vez has sentido que crear contenido te quita demasiado tiempo, o si te da pánico aparecer frente a la cámara, estás en el lugar correcto. Hoy vas a descubrir cómo romper esas barreras de una vez por todas usando la Inteligencia Artificial a tu favor.",
                            "En esta lección aprenderás a estructurar una verdadera 'fábrica de videos' sin necesidad de mostrar tu rostro, grabar tu propia voz o pasar horas editando. Al configurar las herramientas correctas de IA, dejarás que la tecnología haga el 80% del trabajo pesado mientras tú te concentras en la estrategia y en ver llegar tus comisiones de Hotmart. ¡Prepárate para automatizar tu éxito!"
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Para que un video corto (ya sea en TikTok, Reels o YouTube Shorts) se vuelva viral y genere ventas, no necesitas un equipo de producción de Hollywood; solo requieres una estructura persuasiva y el flujo de trabajo adecuado. La IA generativa nos permite crear guiones magnéticos en segundos y unirlos con imágenes de stock y voces ultra realistas sin esfuerzo.",
                            "El secreto de un guion que vende reside en la regla de los tres pasos: 1) El Gancho (los primeros 3 segundos para capturar la atención del usuario que hace scroll), 2) El Cuerpo (donde aportas valor rápido o tocas un dolor específico de tu audiencia), y 3) El Llamado a la Acción (la invitación clara a realizar una acción, como ir al enlace de tu perfil). Para lograr una creación masiva, utilizamos ChatGPT o Claude para redactar múltiples guiones a la vez, ElevenLabs para generar locuciones hiperrealistas y herramientas como CapCut o Canva para el ensamblaje visual rápido."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Imagina que estás promocionando un producto digital de Hotmart sobre 'Adiestramiento Canino'. En lugar de romperte la cabeza pensando qué decir, vas a ChatGPT y escribes el siguiente prompt: 'Actúa como un experto en marketing de afiliados y psicología canina. Escribe 3 guiones de 30 segundos para TikTok usando la estructura: Gancho intrigante, Problema de comportamiento canino y Solución rápida. El objetivo final es que el usuario haga clic en el enlace de mi biografía para acceder a un curso online'.",
                            "En segundos, la IA te entregará las opciones listas. El siguiente paso es copiar el texto del mejor guion, pegarlo en ElevenLabs seleccionando una voz en español que suene natural y enérgica, y descargar el archivo de audio. Finalmente, abres CapCut, importas el audio, utilizas la función de 'subtítulos automáticos' para que el texto aparezca dinámicamente en pantalla y superpones videos de stock gratuitos de perritos (que puedes descargar de Pexels o Pixabay). ¡Listo! En menos de 10 minutos tienes un video profesional de alta conversión sin haber grabado un solo segundo de ti mismo."
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "El error más grave es el síndrome del 'copiar y pegar sin alma'. Muchos afiliados generan textos con IA y los publican exactamente como salen, resultando en videos aburridos, planos y con voces robóticas que la gente ignora de inmediato. Recuerda que la IA te da el 80% del trabajo, pero tú debes aportar ese 20% de toque humano, asegurándote de que los textos conecten con las emociones de tu cliente ideal.",
                            "Otro fallo común es olvidarse del Llamado a la Acción (CTA). De nada sirve tener un video con un millón de visualizaciones si no le dices explícitamente a la audiencia qué es lo que debe hacer después. Si no los invitas a ir al enlace de tu biografía de Hotmart, tus visitas nunca se convertirán en comisiones."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "Crear contenido viral y persuasivo de forma masiva ya no es un privilegio de pocos; con la IA es un juego de consistencia y estrategia. Tu tarea para hoy mismo es muy sencilla: selecciona el producto de Hotmart que vas a promocionar, pídele a ChatGPT que te genere tus primeros 5 guiones utilizando la fórmula que aprendiste, conviértelos en audio y edita tu primer video sin rostro en CapCut. ¡Súbelo a tus redes y da el primer paso para activar tu máquina de ventas automatizada!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: Automatización de Videos con IA",
                    "questions": [
                        {
                            "question": "¿Cuál es la estructura de tres pasos recomendada en la lección para crear un guion de video corto que venda?",
                            "options": [
                                "La Presentación del producto, los Beneficios técnicos y la Despedida cordial.",
                                "El Gancho (primeros 3 segundos), el Cuerpo (valor o dolor) y el Llamado a la Acción (invitación clara).",
                                "La Introducción con saludo formal, el Desarrollo del tema y el Enlace de pago directo.",
                                "El Título llamativo, la Demostración del producto y el Cierre con descuento especial."
                            ],
                            "answer": 1,
                            "explanation": "La lección detalla que el secreto de un guion vendedor es: 1) El Gancho para retener al usuario en los primeros 3 segundos, 2) El Cuerpo para aportar valor o tocar un dolor de la audiencia, y 3) El Llamado a la Acción para guiar al usuario al enlace del perfil."
                        },
                        {
                            "question": "Para la creación masiva de videos sin mostrar el rostro, ¿qué herramientas específicas se sugieren para generar la locución y realizar el ensamblaje visual rápido?",
                            "options": [
                                "Audacity para la locución de voz y Premiere Pro para el montaje cinematográfico complejo.",
                                "Zoom para grabar la voz de fondo y PowerPoint para colocar los subtítulos dinámicos.",
                                "ElevenLabs para generar locuciones hiperrealistas y CapCut o Canva para el ensamblaje visual rápido.",
                                "La voz interna de TikTok para la locución y Photoshop para crear las imágenes fijas."
                            ],
                            "answer": 2,
                            "explanation": "El flujo de trabajo automatizado propuesto en la lección utiliza ChatGPT/Claude para redactar, ElevenLabs para convertir esos guiones en voces hiperrealistas, y CapCut o Canva para unirlos de forma rápida con recursos visuales."
                        },
                        {
                            "question": "Según la lección, ¿cuál es uno de los errores más graves al usar Inteligencia Artificial para crear videos de afiliados?",
                            "options": [
                                "El 'copiar y pegar sin alma', publicando textos idénticos de la IA sin toque humano y olvidándose del Llamado a la Acción (CTA).",
                                "Utilizar videos de stock gratuitos de plataformas como Pexels o Pixabay en lugar de grabaciones propias.",
                                "No pagar la suscripción premium de ChatGPT y ElevenLabs desde el primer día de trabajo.",
                                "Publicar los videos únicamente en TikTok e ignorar por completo los Reels de Instagram."
                            ],
                            "answer": 0,
                            "explanation": "La lección enfatiza que la IA hace el 80% del trabajo, pero el afiliado debe aportar el 20% de toque humano para evitar videos aburridos con voces robóticas. Además, olvidarse del Llamado a la Acción (CTA) impide que las visitas se conviertan en comisiones."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Tu Primer Video Viral Sin Rostro",
                    "type": "Text",
                    "question": "¡Es hora de poner en marcha tu fábrica de contenido! En esta actividad práctica vas a crear tu primer video corto de alta conversión sin mostrar tu rostro, aplicando la regla del 80/20 (80% IA, 20% toque humano) y la estructura persuasiva de tres pasos.\n\nSigue estos pasos para completar tu entrega:\n\n### **Paso 1: Selección del Producto**\nElige el producto de Hotmart que vas a promocionar para esta práctica y define su nicho.\n\n### **Paso 2: Generación y Refinamiento del Guion**\n1. Escribe un prompt persuasivo en ChatGPT o Claude para generar el guion de tu video.\n2. Copia la mejor opción de guion que te dé la IA y edítala para darle tu **20% de toque humano** (asegúrate de que no suene robótico, añade emoción y fuerza).\n3. Identifica claramente las 3 partes en tu guion:\n   * **Gancho (0-3 segundos):** ¿Cómo vas a detener el scroll del usuario?\n   * **Cuerpo:** ¿Qué dolor vas a tocar o qué valor rápido vas a aportar?\n   * **Llamado a la Acción (CTA):** ¿Cuál es la instrucción exacta para que vayan a tu enlace de Hotmart?\n\n### **Paso 3: Locución y Edición**\n1. Convierte tu guion en un audio ultra-realista usando ElevenLabs.\n2. Importa el audio en CapCut o Canva.\n3. Agrega videos de stock de alta calidad (desde Pexels o Pixabay) relacionados con tu temática.\n4. Genera subtítulos automáticos, dales un estilo llamativo y exporta tu video listo para publicar.\n\n---\n\n### **¿Qué debes entregar?**\nResponde a esta actividad en el cuadro de texto completando los siguientes puntos:\n\n1. **Producto de Hotmart elegido:** (Ej: Curso de Adiestramiento Canino Online).\n2. **Prompt de IA utilizado:** Copia y pega el prompt exacto que usaste en ChatGPT o Claude.\n3. **Guion Final Refinado:** Pega tu guion final dividiéndolo claramente en: *Gancho*, *Cuerpo* y *Llamado a la Acción (CTA)*.\n4. **Enlace al Video:** Sube tu video terminado a Google Drive (asegúrate de que el enlace sea público) o comparte el enlace directo si ya lo subiste a tus redes sociales (TikTok, Instagram Reels o YouTube Shorts)."
                }
            }
        },
        {
            "title": "Módulo 4: El Embudo de Ventas Automatizado",
            "lesson": {
                "title": "Configuración del ecosistema de enlaces de afiliado y la estructura del embudo mínimo viable",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Bienvenido al Módulo 4! Si has llegado hasta aquí, ya tienes claro qué vas a vender y cómo la Inteligencia Artificial te ayudará a crear contenido magnético. Ahora es el momento de construir la tubería digital por donde pasará tu audiencia para convertirse en clientes. No te preocupes, no necesitas ser un programador ni gastar cientos de dólares en software complicados. Hoy vamos a montar tu Embudo Mínimo Viable (EMV).",
                            "El gran error de los principiantes es querer crear una web gigante y compleja desde el primer día. Eso solo genera frustración y parálisis por análisis. Aquí vamos a ir al grano: configuraremos un ecosistema de enlaces de afiliado sencillo pero altamente efectivo, diseñado para capturar la atención de tu cliente ideal y guiarlo directamente hacia la comisión sin fricciones."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Para entender este ecosistema, primero debes dominar los 'Hotlinks' de Hotmart. Un Hotlink es tu enlace único de afiliado que contiene un código de seguimiento (cookie). Cuando alguien hace clic en tu Hotlink y compra, el sistema sabe instantáneamente que la venta es tuya y te asigna la comisión. Es así de sencillo y seguro.",
                            "Ahora, ¿cómo estructuramos nuestro Embudo Mínimo Viable? Un EMV consta de tres piezas clave que conectaremos en menos de una hora: 1) Tu fuente de tráfico (las redes sociales donde publicas el contenido creado con IA), 2) Tu página puente o enlace de redirección, y 3) La página de pago (checkout) de Hotmart.",
                            "En lugar de enviar a la gente directamente a la página de ventas fría de Hotmart, utilizaremos una 'página de enlace en bio' optimizada (como Beacons, Linktree o Canva) o un enlace directo a un chat de WhatsApp automatizado. ¿Por qué? Porque la IA nos ayudará a redactar copys tan persuasivos en estos pasos intermedios que la conversión se duplicará. Este flujo es simple, rápido de montar y, lo mejor de todo, 100% gratuito."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Imagina que estás promocionando un curso de 'Repostería Saludable y Sin Gluten' sin mostrar tu rostro. Tu estrategia en redes sociales atrae a miles de personas interesadas con videos creados por IA. Para monetizar ese tráfico, sigue este paso a paso:",
                            "Paso 1: Ve a Hotmart, accede a los enlaces de divulgación del producto y copia tu 'Hotlink de la página de ventas' o, mejor aún, el 'Hotlink de Checkout Limpio' (que lleva directo al pago si ya diste la información previa).",
                            "Paso 2: Abre ChatGPT y pídele: 'Escribe una biografía de Instagram de 150 caracteres para una cuenta de repostería saludable y un llamado a la acción (CTA) irresistible para que hagan clic en el enlace'. Copia el resultado y pégalo en tu perfil.",
                            "Paso 3: Crea una cuenta gratuita en Beacons.ai. Diseña un botón llamativo con un texto como: '¡Accede hoy con 50% de descuento al Programa de Repostería Saludable!'. Detrás de ese botón, pega tu Hotlink de afiliado.",
                            "¡Listo! Cuando un usuario vea tu video de IA en TikTok o Reels, se interesará por la receta, irá a tu biografía, hará clic en tu enlace de Beacons y comprará el curso. El sistema de Hotmart registrará la venta automáticamente y tú recibirás tu notificación de comisión en el celular."
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "El error número uno y más grave: Hacer spam con tu enlace de afiliado directamente en los comentarios de publicaciones ajenas o enviarlo por mensaje privado sin que nadie te lo pida. Esto solo hará que bloqueen tu cuenta y dañará tu reputación.",
                            "Error número dos: Confundir los enlaces. Copiar la URL de la barra del navegador una vez que ya estás dentro de la página de ventas en lugar de usar el Hotlink oficial que te da la plataforma de Hotmart. Si haces esto, perderás el rastreo y la comisión no te llegará.",
                            "Error número tres: Complicarte la vida intentando diseñar un sitio web complejo desde el día uno. Recuerda la regla de oro: menos es más. Valida tu producto primero con el Embudo Mínimo Viable y, una vez que tengas tus primeras ventas, escala a estructuras más avanzadas."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "En resumen: Tu ecosistema de afiliado no necesita ser complejo para ser millonario. Solo requieres un perfil optimizado en redes sociales, un enlace inteligente en tu bio con un llamado a la acción claro y tu Hotlink de Hotmart correctamente configurado para asegurar tus comisiones.",
                            "Tu tarea para hoy: Entra a Hotmart y copia tus Hotlinks del producto que elegiste. Luego, crea tu cuenta gratuita en Beacons o Linktree y diseña tu página puente. Usa ChatGPT para redactar un llamado a la acción que despierte curiosidad y déjalo todo listo en tu biografía. ¡Estás a un solo clic de distancia de tu primera venta!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz del Módulo: Tu Embudo Mínimo Viable (EMV)",
                    "questions": [
                        {
                            "question": "¿Qué es un \"Hotlink\" en la plataforma de Hotmart y cuál es su función principal?",
                            "options": [
                                "Un enlace único de afiliado con un código de seguimiento (cookie) que asegura la asignación de tu comisión al realizarse una venta.",
                                "Un enlace de descuento temporal que los productores activan de forma aleatoria para los clientes.",
                                "La dirección URL de la barra de tu navegador que copias después de entrar a la página de ventas.",
                                "Un código de programación complejo que debes instalar en tu propio servidor web para rastrear clics."
                            ],
                            "answer": 0,
                            "explanation": "El Hotlink es tu enlace exclusivo generado por Hotmart que contiene una cookie de seguimiento. Gracias a este, el sistema detecta que la venta llegó a través de ti y te asigna la comisión automáticamente."
                        },
                        {
                            "question": "¿Cuáles son las tres piezas clave que componen el Embudo Mínimo Viable (EMV) recomendado en la lección?",
                            "options": [
                                "Un sitio web corporativo, un blog optimizado para SEO y un sistema de pasarela de pago propio.",
                                "La fuente de tráfico (redes sociales), una página puente o enlace de redirección (como Beacons), y la página de pago (checkout) de Hotmart.",
                                "Una campaña publicitaria de pago, un grupo de soporte técnico y un sistema de correos automatizados.",
                                "Un catálogo en PDF, un grupo privado de Telegram y un formulario de Google para registrar datos."
                            ],
                            "answer": 1,
                            "explanation": "El EMV simplifica el proceso al conectar el tráfico de tus redes sociales con una página puente sencilla (como Beacons) que dirige directamente al checkout de Hotmart, facilitando una conversión rápida y sin fricciones."
                        },
                        {
                            "question": "¿Qué error grave puede provocar que pierdas el rastreo de tu afiliación y, por lo tanto, tu comisión?",
                            "options": [
                                "Utilizar ChatGPT para redactar copys de alta conversión para tu enlace de la biografía.",
                                "Usar herramientas gratuitas para la página puente como Beacons.ai o Linktree.",
                                "Hacer videos con Inteligencia Artificial sin mostrar tu rostro en redes sociales.",
                                "Copiar la URL final de la barra de direcciones del navegador en lugar de usar el Hotlink oficial que te entrega Hotmart."
                            ],
                            "answer": 3,
                            "explanation": "Copiar la URL de la barra del navegador cuando la página ya ha cargado elimina el código de rastreo (cookie) de afiliado. Debes usar siempre el Hotlink oficial directamente de la plataforma de Hotmart para garantizar tu comisión."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Tu Primer Embudo Mínimo Viable (EMV)",
                    "type": "Text",
                    "question": "¡Es hora de construir la tubería digital que automatizará tus ventas! En esta actividad práctica vas a diseñar y configurar tu propio Embudo Mínimo Viable (EMV) utilizando herramientas 100% gratuitas.\n\nSigue estos pasos detallados para completar la actividad:\n\n### **Paso 1: Obtén tu Hotlink Correcto**\n1. Entra a tu cuenta de Hotmart, ve a los productos en los que estás afiliado y copia tu **Hotlink oficial** de la página de ventas o de checkout limpio.\n*Recuerda:* No copies la URL de la barra de direcciones del navegador una vez que la página ya cargó; usa únicamente el enlace de divulgación que te proporciona Hotmart.\n\n### **Paso 2: Co-crea tu Bio y CTA con Inteligencia Artificial**\n1. Abre ChatGPT y pídele redactar la biografía para tu red social. Puedes usar este prompt adaptado a tu producto:\n   *\"Escribe una biografía de Instagram de 150 caracteres para una cuenta sobre [Nicho/Tema de tu producto] y un llamado a la acción (CTA) irresistible para que hagan clic en el enlace de mi biografía.\"*\n2. Copia y pule el resultado para que quede perfecto.\n\n### **Paso 3: Configura tu Página Puente**\n1. Regístrate de forma gratuita en **Beacons.ai** (o Linktree).\n2. Crea un botón llamativo. El texto del botón debe ser un CTA persuasivo e irresistible (por ejemplo: \"¡Accede hoy con 50% de descuento al Programa de Repostería Saludable!\").\n3. Vincula tu Hotlink oficial de Hotmart detrás de ese botón.\n\n---\n\n### **Entregables que debes presentar:**\n\n1. **Tu Hotlink oficial:** Pega el enlace de afiliado de Hotmart que vas a utilizar (asegúrate de que sea el formato de Hotlink para que se registre tu comisión).\n2. **Texto de tu Biografía y CTA:** Pega la biografía optimizada y el llamado a la acción que generaste con la ayuda de ChatGPT.\n3. **Enlace de tu Página Puente:** Comparte el link público de tu Beacons o Linktree para comprobar que el botón y el enlace de afiliado funcionan correctamente.\n4. **Checklist Anti-Errores (Responde con un 'Sí' o 'No' a cada una):**\n   - ¿Confirmaste que tu enlace de afiliado es el Hotlink oficial y no la URL de la barra de navegación? [ ]\n   - ¿Te comprometiste a no hacer spam en comentarios o mensajes directos no solicitados? [ ]\n   - ¿Mantuviste la estructura simple sin complicarte con páginas web costosas desde el inicio? [ ]"
                }
            }
        },
        {
            "title": "Módulo 5: Lanzamiento de Campaña y Optimización",
            "lesson": {
                "title": "Puesta en marcha de tu primera estrategia de ventas orgánica y optimización con IA",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Ha llegado el gran momento! Has elegido tu producto, has estructurado tu estrategia y ahora es tiempo de encender la maquinaria. En esta lección vas a poner en marcha tu primera estrategia de ventas orgánica —es decir, sin invertir un solo centavo en publicidad— utilizando el poder de la Inteligencia Artificial para optimizar cada paso del proceso.",
                            "No te preocupes si nunca has vendido nada en internet o si te da pánico mostrar tu rostro ante la cámara. Hoy en día, gracias a la IA, puedes crear canales de contenido altamente persuasivos, automatizar las interacciones con tus prospectos y cerrar ventas en piloto automático mientras te enfocas en lo que realmente importa: analizar tus métricas y escalar tus ingresos."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Una estrategia de venta orgánica exitosa se basa en tres pilares: Atracción, Conexión y Conversión. La IA nos permite optimizar cada uno de estos pilares para que el 80% del trabajo pesado se haga en segundos. Primero, en la fase de Atracción, utilizamos herramientas como ChatGPT para generar ganchos (hooks) virales y guiones de videos cortos (Reels, TikToks o Shorts) que capturen la atención de tu cliente ideal al instante.",
                            "Para la fase de Conexión, en lugar de pasar horas respondiendo mensajes uno a uno, estructuramos un sistema de respuestas semiasistido por IA. Redactamos plantillas de persuasión utilizando disparadores psicológicos que resuelven objeciones comunes del comprador de inmediato. Finalmente, en la Conversión, optimizamos tu enlace de afiliado de Hotmart colocándolo de forma estratégica en tu biografía y usando llamados a la acción (CTA) irresistibles que guíen al usuario a la compra de forma natural."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Imagina que estás vendiendo un curso de Hotmart sobre \"Educación Felina y Comportamiento de Gatos\". En lugar de grabar videos tú mismo, le pides a ChatGPT lo siguiente: 'Actúa como un experto en marketing de afiliados. Escríbeme 3 guiones de 15 segundos para TikTok sobre cómo evitar que los gatos arañen los muebles. Incluye un gancho fuerte al inicio y un llamado a la acción para que vayan al enlace de mi biografía al final'.",
                            "La IA te entregará guiones perfectos. Luego, usas una plataforma de videos de stock gratuitos (como Pexels o Pixabay) para descargar clips de gatitos adorables, les superpones el texto del guion con una voz de IA en CapCut y ¡listo! Tienes tu video listo en 10 minutos. En la descripción escribes: '¿Quieres que tu michi deje de destruir tu casa? Ve al enlace de mi perfil y accede hoy con el 50% de descuento'. Cuando los usuarios comenten, tú solo copias y pegas las respuestas optimizadas por la IA que cierran la venta en su chat privado."
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "El error más grave es la falta de constancia. Muchos publican solo dos o tres videos, no ven ventas inmediatas y abandonan. El algoritmo orgánico necesita consistencia (mínimo 1 video diario durante las primeras dos semanas) para entender a quién le interesa tu contenido.",
                            "Otro error común es sonar demasiado técnico o desesperado por vender. A la gente no le gusta que le vendan, le gusta comprar soluciones a sus problemas. Usa la IA para suavizar tus mensajes y enfocarte siempre en la transformación y los beneficios del producto, no solo en sus características."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "En resumen: la IA es tu redactora creativa, tu editora de video y tu asistente de ventas personal. Tu única tarea es programar los contenidos, analizar cuáles funcionan mejor y refinar el mensaje.",
                            "Tu reto para hoy: Elige el producto de Hotmart con el que vas a trabajar, genera tus primeros 3 guiones con IA y publícalos en tu cuenta de nicho. Da el primer paso hoy mismo; la acción es lo único que separa una idea de una comisión real en tu cuenta bancaria. ¡A por ello!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz de Estrategia de Ventas Orgánica con IA",
                    "questions": [
                        {
                            "question": "¿Cuáles son los tres pilares en los que se basa una estrategia de venta orgánica exitosa según la lección?",
                            "options": [
                                "Publicidad pagada, Segmentación y Cierre de ventas.",
                                "Atracción, Conexión y Conversión.",
                                "Creación de marca, Diseño web y Email marketing.",
                                "Investigación de mercado, Logística y Distribución."
                            ],
                            "answer": 1,
                            "explanation": "La lección explica que una estrategia orgánica exitosa se divide en tres pilares: Atracción (capturar atención con ganchos/guiones), Conexión (resolver objeciones) y Conversión (guiar al usuario a la compra mediante el enlace de afiliado)."
                        },
                        {
                            "question": "Según la sección de 'Errores Comunes', ¿cuál es el mínimo de constancia recomendado para que el algoritmo entienda a tu audiencia?",
                            "options": [
                                "Al menos un video diario durante las primeras dos semanas.",
                                "Publicar dos o tres videos en total para ver si funcionan.",
                                "Subir un video cada tres días durante un mes.",
                                "Publicar únicamente los fines de semana."
                            ],
                            "answer": 0,
                            "explanation": "El texto señala que el error más grave es la falta de constancia y que el algoritmo orgánico requiere un mínimo de un video diario durante las primeras dos semanas para entender qué tipo de usuarios se interesan en tu contenido."
                        },
                        {
                            "question": "Si no deseas mostrar tu rostro en cámara, ¿qué alternativa práctica propone la lección para crear tus videos?",
                            "options": [
                                "Pagar a un presentador profesional en plataformas de freelancers.",
                                "Hacer capturas de pantalla de la página de Hotmart sin agregar sonido.",
                                "Utilizar clips de video de stock gratuitos, agregarles el texto del guion de ChatGPT y usar una voz de IA.",
                                "Subir únicamente imágenes estáticas con música de fondo sin texto explicativo."
                            ],
                            "answer": 2,
                            "explanation": "El ejemplo práctico detalla que puedes descargar videos de stock (como en Pexels o Pixabay), superponerles el guion redactado por ChatGPT y usar una voz de IA (por ejemplo, en CapCut) para tener videos listos sin necesidad de grabarte a ti mismo."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Tu Primer Lanzamiento Orgánico Potenciado con IA",
                    "type": "Text",
                    "question": "¡Ha llegado el momento de encender la maquinaria y lanzar tu campaña! En esta actividad práctica vas a diseñar la estructura completa de tu primera campaña orgánica utilizando Inteligencia Artificial para las fases de Atracción y Conexión.\n\nSigue estos pasos detallados para completar tu actividad y comparte tus resultados:\n\n### **Paso 1: Define tu Producto y Nicho**\n1. Elige un producto digital en Hotmart con el que vas a trabajar (por ejemplo: adiestramiento canino, costura, finanzas personales, etc.).\n2. Define brevemente quién es tu cliente ideal (ejemplo: dueños de cachorros estresados que muerden muebles).\n\n### **Paso 2: Fase de Atracción (Redacción de Guion con IA)**\n1. Entra a ChatGPT (o la IA de tu preferencia) y escribe un prompt adaptado a tu nicho para generar guiones de videos cortos (Reels/TikTok).\n*Ejemplo de estructura de prompt:* \"Actúa como un experto en marketing de afiliados de Hotmart. Escríbeme un guion de 15 segundos para TikTok sobre [Problema de tu Nicho]. Incluye un gancho (hook) intrigante en los primeros 3 segundos, un beneficio claro, y un llamado a la acción (CTA) para que vayan al enlace de mi biografía.\"\n2. Copia el prompt que utilizaste y selecciona **uno** de los guiones generados por la IA para incluirlo en tu entrega.\n\n### **Paso 3: Fase de Conexión (Plantilla de Cierre por DM)**\nCuando tus videos empiecen a recibir comentarios como \"Yo quiero\", \"Me interesa\" o \"Más info\", no debes vender de forma fría. \n1. Pídele a la IA que redacte una plantilla de respuesta persuasiva y amigable para enviar por mensaje privado (DM).\n2. Asegúrate de que esta plantilla: genere empatía, resuelva una objeción común y guíe al usuario a tu enlace de afiliado con un beneficio de escasez o urgencia (ejemplo: 50% de descuento solo por hoy).\n\n---\n\n### **Entregables que debes publicar:**\nPara completar esta actividad con éxito, copia y pega en el recuadro de texto los siguientes 4 puntos:\n\n1. **Producto seleccionado y Nicho:** (Nombre del producto de Hotmart y a quién va dirigido).\n2. **Prompt de IA utilizado:** (El texto exacto que le diste a la IA para crear tus guiones).\n3. **Guion Ganador:** (Pega el guion de 15 segundos generado, identificando claramente el **Gancho**, el **Contenido** y el **Llamado a la Acción (CTA)**).\n4. **Plantilla de Mensaje de Cierre (DM):** (La respuesta optimizada que enviarás a los interesados para concretar la venta)."
                }
            }
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Máquina de Ventas en Hotmart Automatizada con IA",
        "type": "Document",
        "question": "¡Bienvenido al Proyecto Final Integrador! En este proyecto vas a aplicar todo lo aprendido para estructurar tu propio negocio de afiliados en Hotmart, utilizando la Inteligencia Artificial como tu asistente principal. El objetivo es que dejes configurado un sistema de ventas listo para rodar, delegando el 80% del trabajo pesado a la IA.\n\nPara completar este proyecto y recibir tu evaluación (la cual será procesada por una IA), debes entregar un único documento en formato PDF o de texto que contenga los siguientes 4 pasos debidamente desarrollados:\n\n---\n\n### **PASO 1: Selección del Producto Ganador y Buyer Persona con IA**\n1. **Selección en Hotmart**: Elige un producto del mercado de afiliación de Hotmart. Indica su nombre, nicho, porcentaje de comisión y por qué lo elegiste (mínimo 2 razones de temperatura, Blueprint o satisfacción).\n2. **Definición del Cliente Ideal (Buyer Persona) con ChatGPT**: Utiliza un prompt de IA para extraer el perfil de tu cliente ideal. \n   * *Debes incluir en tu entrega el prompt exacto que utilizaste y la respuesta resumida de la IA que detalle: Dolores, Deseos, Objeciones de compra y un Gancho (Hook) mental para captar su atención.*\n\n### **PASO 2: Creación de la Estrategia de Contenido (Método Sin Aparecer en Cámara)**\n1. **Calendario de Contenidos**: Pídele a la IA (ChatGPT/Claude) que genere una estrategia de 3 videos cortos (TikTok/Instagram Reels/YouTube Shorts) para atraer a tu Buyer Persona.\n   * *Debes incluir en tu entrega la estructura de los 3 guiones generados por la IA. Cada guion debe tener: Gancho (0-3 seg), Desarrollo (valor/curiosidad) y Llamado a la Acción (CTA) directo a tu enlace de afiliado o canal de ventas.*\n\n### **PASO 3: Producción de Contenido Automatizado con IA**\n1. **Materialización del Contenido**: Elige uno de los 3 guiones del Paso 2 y créalo utilizando herramientas de IA (puedes usar Canva para video/imágenes de stock, ElevenLabs o Clipchamp para voces sintéticas, o CapCut para la edición automatizada con subtítulos dinámicos).\n   * *Debes incluir en tu entrega el enlace público al video finalizado (subido a Google Drive, YouTube, Instagram o TikTok de manera pública/oculta) para verificar su creación.*\n\n### **PASO 4: Estructura del Embudo de Ventas Mínimo Viable (MVE)**\n1. **Script de Cierre por WhatsApp**: Crea un script automatizado o plantilla de respuestas rápidas con IA para cuando las personas te contacten interesadas en el producto.\n   * *Debes incluir en tu entrega el script de cierre en 3 pasos: Bienvenida/Filtro, Presentación de la Oferta (derribando objeciones con IA) y Cierre con urgencia/escasez.*\n\n---\n\n### **FORMATO DE ENTREGA REQUERIDO PARA LA EVALUACIÓN**\nCopia y pega la siguiente plantilla en tu documento de entrega y completa los campos:\n\n1. **Nombre del Producto Hotmart:** [Inserta aquí]\n2. **Prompt de Buyer Persona utilizado:** [Inserta aquí]\n3. **Resumen del Buyer Persona (Dolores, Deseos, Objeciones):** [Inserta aquí]\n4. **Guiones de los 3 videos generados por IA:** [Inserta aquí]\n5. **Enlace al video final creado (Drive/TikTok/Reels):** [Inserta enlace aquí]\n6. **Script de Cierre de Ventas por WhatsApp:** [Inserta aquí]\n\n*Nota: La IA evaluará la coherencia entre el producto elegido, el perfil del cliente ideal desarrollado, la calidad persuasiva de los guiones de video y la estructura del script de ventas por WhatsApp.*"
    }
}

def field_exists(doctype, fieldname):
    try:
        return frappe.get_meta(doctype).has_field(fieldname)
    except Exception:
        return False

def set_value_if_field_exists(doc, fieldname, value):
    if field_exists(doc.doctype, fieldname):
        doc.set(fieldname, value)

def get_existing_name(doctype, filters):
    return frappe.db.exists(doctype, filters)

def create_or_update_category(category_name):
    name = frappe.db.exists("LMS Category", category_name)
    if name:
        return name
    doc = frappe.new_doc("LMS Category")
    if field_exists("LMS Category", "title"):
        doc.title = category_name
    elif field_exists("LMS Category", "category"):
        doc.category = category_name
    elif field_exists("LMS Category", "category_name"):
        doc.category_name = category_name
    else:
        doc.name = category_name
    doc.insert(ignore_permissions=True)
    return doc.name

def create_or_update_course(course_data, category_name):
    name = frappe.db.exists("LMS Course", {"title": course_data["title"]})
    if name:
        doc = frappe.get_doc("LMS Course", name)
    else:
        doc = frappe.new_doc("LMS Course")
        doc.title = course_data["title"]
        
    doc.short_introduction = course_data.get("short_introduction", "")
    doc.description = course_data.get("description", "")
    doc.published = 1
    doc.category = category_name
    
    set_value_if_field_exists(doc, "card_gradient", course_data.get("card_gradient", "Blue"))
    set_value_if_field_exists(doc, "enable_certification", 1)
    set_value_if_field_exists(doc, "studybadge_ai_enabled", course_data.get("studybadge_ai_enabled", 1))
    set_value_if_field_exists(doc, "ai_rubric", course_data.get("ai_rubric", ""))
    
    has_instructor = any(i.instructor == INSTRUCTOR_NAME for i in doc.get("instructors", []))
    if not has_instructor:
        doc.append("instructors", {"instructor": INSTRUCTOR_NAME})
        
    doc.save(ignore_permissions=True)
    return doc.name

def create_or_update_assignment(assignment_data, course_name):
    name = frappe.db.exists("LMS Assignment", {"title": assignment_data["title"], "course": course_name})
    if name:
        doc = frappe.get_doc("LMS Assignment", name)
    else:
        doc = frappe.new_doc("LMS Assignment")
        doc.title = assignment_data["title"]
        doc.course = course_name
        
    doc.type = assignment_data.get("type", "Text")
    doc.question = assignment_data.get("question", "")
    doc.save(ignore_permissions=True)
    return doc.name

def create_or_update_question(question_data):
    name = frappe.db.exists("LMS Question", {"question": question_data["question"]})
    if name:
        doc = frappe.get_doc("LMS Question", name)
    else:
        doc = frappe.new_doc("LMS Question")
        doc.question = question_data["question"]
        
    doc.type = "Choices"
    options = question_data.get("options", ["", "", "", ""])
    answer_idx = question_data.get("answer", 0)
    explanation = question_data.get("explanation", "")
    
    for i in range(1, 5):
        opt_text = options[i-1] if i-1 < len(options) else ""
        doc.set(f"option_{i}", opt_text)
        doc.set(f"is_correct_{i}", 1 if i-1 == answer_idx else 0)
        doc.set(f"explanation_{i}", explanation if i-1 == answer_idx else "")
        
    doc.save(ignore_permissions=True)
    return doc.name

def create_or_update_quiz(quiz_data, course_name):
    name = frappe.db.exists("LMS Quiz", {"title": quiz_data["title"], "course": course_name})
    if name:
        doc = frappe.get_doc("LMS Quiz", name)
        doc.set("questions", [])
    else:
        doc = frappe.new_doc("LMS Quiz")
        doc.title = quiz_data["title"]
        doc.course = course_name
        
    set_value_if_field_exists(doc, "passing_percentage", 50)
        
    for q_data in quiz_data.get("questions", []):
        q_name = create_or_update_question(q_data)
        doc.append("questions", {"question": q_name})
        
    doc.save(ignore_permissions=True)
    return doc.name

def paragraph_block(text):
    return {"type": "paragraph", "data": {"text": text}}

def header_block(text, level=2):
    return {"type": "header", "data": {"text": text, "level": level}}

def build_editorjs_content(sections, quiz_name=None, assignment_name=None):
    blocks = []
    for sec in sections:
        if sec.get("heading"):
            blocks.append(header_block(sec["heading"]))
        for p in sec.get("paragraphs", []):
            if p.strip():
                blocks.append(paragraph_block(p))
                
    if quiz_name:
        blocks.append({"type": "quiz", "data": {"quiz": quiz_name}})
        
    if assignment_name:
        blocks.append({"type": "assignment", "data": {"assignment": assignment_name}})
        
    return json.dumps({
        "time": int(time.time() * 1000),
        "blocks": blocks,
        "version": "2.29.1"
    })

def create_or_update_lesson(lesson_data, chapter_name, course_name):
    name = frappe.db.exists("Course Lesson", {"title": lesson_data["title"], "chapter": chapter_name})
    if name:
        doc = frappe.get_doc("Course Lesson", name)
    else:
        doc = frappe.new_doc("Course Lesson")
        doc.title = lesson_data["title"]
        doc.chapter = chapter_name
        doc.course = course_name
        
    quiz_name = None
    if lesson_data.get("quiz"):
        quiz_name = create_or_update_quiz(lesson_data["quiz"], course_name)
        
    assignment_name = None
    if lesson_data.get("assignment"):
        assignment_name = create_or_update_assignment(lesson_data["assignment"], course_name)
        
    doc.content = build_editorjs_content(lesson_data.get("sections", []), quiz_name, assignment_name)
    doc.body = "Esta lección usa EditorJS."
    doc.save(ignore_permissions=True)
    return doc.name

def create_or_update_chapter(chapter_data, course_name):
    name = frappe.db.exists("Course Chapter", {"title": chapter_data["title"], "course": course_name})
    if name:
        doc = frappe.get_doc("Course Chapter", name)
    else:
        doc = frappe.new_doc("Course Chapter")
        doc.title = chapter_data["title"]
        doc.course = course_name
        doc.save(ignore_permissions=True)
        
    lesson_data = chapter_data.get("lesson")
    if lesson_data:
        create_or_update_lesson(lesson_data, doc.name, course_name)
        
    return doc.name

def rebuild_course_chapters(course_name, chapters_data):
    for c_data in chapters_data:
        create_or_update_chapter(c_data, course_name)

def run():
    print("=======================================")
    print("INICIANDO SETUP DE CURSO GENERADO...")
    print("=======================================")
    
    cat_name = create_or_update_category(COURSE_DATA.get("category", "Uncategorized"))
    course_name = create_or_update_course(COURSE_DATA, cat_name)
    
    rebuild_course_chapters(course_name, COURSE_DATA.get("chapters", []))
    
    if COURSE_DATA.get("final_project"):
        print("Creando Proyecto Final...")
        create_or_update_assignment(COURSE_DATA["final_project"], course_name)
        
    frappe.db.commit()
    print("=======================================")
    print(f"CURSO CREADO CON ÉXITO: {course_name}")
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
