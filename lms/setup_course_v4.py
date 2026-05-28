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
    "title": "Creadores de Modelos de IA: Tu Negocio de Influencer Virtual Ético y Rentable",
    "short_introduction": "Crea, diseña y monetiza tu primera modelo virtual con inteligencia artificial con un enfoque 100% ético, consistente y sin complicaciones técnicas.",
    "description": "<p>Aprende paso a paso a construir la identidad, el rostro consistente y la estrategia de negocio de un modelo virtual. Descubre cómo entrar en un mercado multimillonario posicionando una marca digital respetuosa, transparente y lista para facturar.</p><ul><li>Domina la consistencia de rostro en múltiples poses y entornos sin saber programar.</li><li>Activa canales de monetización éticos y recurrentes alineados con las políticas de las plataformas digitales.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza la comprensión, la aplicación real, la claridad y la creatividad antes que la perfección técnica. Valora respuestas naturales, ejemplos útiles y el esfuerzo real del estudiante. Penaliza respuestas vacías, copiadas de internet, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Indica siempre puntos fuertes, áreas de mejora, nota final y estado: Aprobado si la nota es 7 o más, Desaprobado si es menor a 7.",
    "chapters": [
        {
            "title": "Módulo 1: Conceptualización y Ética de la Modelo de IA",
            "lessons": [
                {
                    "title": "Diseño de Identidad: Creando el Alma de tu Modelo de IA",
                    "objective": "Definir el concepto, personalidad y valores de tu modelo de IA, estableciendo un marco ético de transparencia que genere confianza y credibilidad desde el primer día.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Entrar en el mercado de los creadores virtuales no se trata simplemente de generar imágenes atractivas con inteligencia artificial; se trata de construir una marca con propósito. Cualquiera puede presionar un botón y generar un rostro, pero el verdadero valor comercial radica en darle un alma, un nicho claro y una base ética que atraiga a marcas y comunidades reales.",
                                "En esta lección, aprenderás a transformar una idea abstracta en una identidad virtual sólida. Definiremos quién es tu modelo, qué valores representa y cómo posicionarla de manera ética en un ecosistema digital que valora la transparencia por encima de todo."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para destacar en el saturado mundo digital, tu modelo de IA necesita un concepto único. Esto incluye su nombre, edad, origen cultural, intereses y un tono de voz definido. En lugar de intentar agradar a todo el mundo, debes elegir un nicho específico: ¿será una entusiasta de la moda sostenible, una nómada digital apasionada por la tecnología, o una entrenadora de bienestar y mindfulness? Cuanto más delimitado sea su enfoque, más fácil será conectar con una audiencia real y monetizar su presencia.",
                                "Aquí radica la regla de oro del posicionamiento ético: la transparencia es tu activo más valioso. Nunca intentes hacer pasar a tu modelo de IA por una persona de carne y hueso. Hacerlo infringe las políticas de las principales redes sociales y destruye la confianza del público. Al declarar abiertamente en su biografía que es una 'Creadora Virtual' o 'Modelo de IA', eliminas el engaño y posicionas el proyecto como una propuesta innovadora, artística y tecnológica con la que las marcas modernas desean asociarse.",
                                "Finalmente, debemos diseñar su mapa de valores. ¿Qué causas apoya? ¿De qué temas habla? Si tu modelo promueve la vida saludable, su estética visual y sus mensajes de texto deben reflejar esa coherencia. Esta consistencia de marca es lo que transforma un conjunto de píxeles generados por computadora en un activo digital con un valor comercial real."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina a 'Alma', una modelo virtual creada para el nicho del estilo de vida consciente y la tecnología limpia. En lugar de publicar fotos aleatorias en la playa, la biografía de Alma dice claramente: 'Creadora Virtual | Explorando la moda sostenible y el futuro de la tecnología verde 🌿 | Creada con IA'.",
                                "El contenido visual de Alma combina tonos tierra y estética futurista. Sus textos no fingen que 'probó' una comida, sino que analizan las tendencias de ingredientes orgánicos y entrevistan a emprendedores reales del sector ecológico. Gracias a este enfoque transparente, una marca de cosmética natural la patrocinó para mostrar su nuevo empaque biodegradable, valorando su estética vanguardista sin incurrir en publicidad engañosa."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave y frecuente es 'La Mentira Humana': intentar engañar a la audiencia inventando historias de vida falsas, dramas personales o fingiendo que la modelo sufre problemas humanos reales. Tarde o temprano la audiencia descubre la verdad, lo que genera un rechazo absoluto hacia la marca y penalizaciones en las plataformas sociales.",
                                "Otro error común es la falta de nicho. Crear una modelo genérica que un día promociona videojuegos, al día siguiente trajes de baño y al otro consejos financieros. Sin un enfoque claro, la audiencia no se identifica con ella y las marcas no encontrarán un público objetivo claro al cual dirigir sus patrocinios."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, una modelo virtual exitosa se sostiene sobre tres pilares: un nicho de mercado muy específico, una biografía transparente que declare su naturaleza de IA y una voz coherente con sus valores. La confianza es la moneda de cambio en la economía digital, incluso para los personajes virtuales.",
                                "Tu acción recomendada para hoy es rellenar la ficha de identidad de tu modelo: define su nombre, su nicho principal (ej. fitness, tecnología, moda retro), 3 rasgos de su personalidad y redacta su biografía de Instagram o TikTok en menos de 150 caracteres, asegurándote de incluir la etiqueta 'Creador Virtual' o 'AI Model'."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz de Identidad y Ética: El Alma de tu Modelo de IA",
                        "questions": [
                            {
                                "question": "Según la lección, ¿cuál es la regla de oro para el posicionamiento ético de tu modelo de IA en las redes sociales?",
                                "options": [
                                    "Mantener una total transparencia declarando abiertamente en la biografía que es una 'Creadora Virtual' o 'Modelo de IA'.",
                                    "Ocultar su naturaleza tecnológica hasta alcanzar un número mínimo de seguidores orgánicos.",
                                    "Cambiar su origen biológico en cada publicación para generar misterio y debate en los comentarios.",
                                    "No mencionar que es una IA para evitar que los algoritmos de las redes sociales limiten el alcance de la cuenta."
                                ],
                                "answer": 0,
                                "explanation": "La transparencia es tu activo más valioso. Declarar su naturaleza tecnológica evita el engaño, protege la confianza de tu audiencia y posiciona tu proyecto como una propuesta innovadora y artística muy atractiva para las marcas modernas."
                            },
                            {
                                "question": "¿En qué consiste el error común denominado 'La Mentira Humana'?",
                                "options": [
                                    "En olvidarse de interactuar con los seguidores reales a través de mensajes directos.",
                                    "En inventar historias de vida falsas, dramas personales o fingir que el modelo virtual sufre problemas humanos reales.",
                                    "En promocionar marcas que no coinciden exactamente con la paleta de colores del perfil.",
                                    "En usar herramientas de generación de imágenes que no alcancen la calidad fotográfica fotorrealista."
                                ],
                                "answer": 1,
                                "explanation": "Intentar engañar al público simulando una existencia humana real tarde o temprano se descubre, destruyendo la credibilidad de tu proyecto y provocando el rechazo absoluto de tu comunidad y posibles penalizaciones en plataformas."
                            },
                            {
                                "question": "¿Por qué es fundamental que tu modelo de IA se enfoque en un nicho de mercado específico en lugar de ser genérica?",
                                "options": [
                                    "Because así se requiere menor cantidad de texto en los prompts de generación de imágenes.",
                                    "Porque los algoritmos de las plataformas solo permiten un máximo de dos temáticas por perfil de creador.",
                                    "Porque facilita una conexión real y enfocada con la audiencia, haciendo que las marcas encuentren un público objetivo claro para sus patrocinios.",
                                    "Porque limita el número de comentarios negativos que la cuenta puede recibir de cuentas de usuarios reales."
                                ],
                                "answer": 2,
                                "explanation": "Intentar agradar a todo el mundo diluye el mensaje. Un enfoque bien delimitado (como la moda sostenible o el bienestar) te diferencia de la saturación del mercado y le da un valor comercial e identitario real a tu activo digital."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseño de la Ficha de Identidad y Manifiesto Ético de tu Modelo de IA",
                        "type": "Text",
                        "question": "<p>¡Es momento de dar vida a tu propuesta! En esta actividad práctica vas a diseñar la base de tu modelo de IA, asegurándote de que tenga un propósito claro, un nicho rentable y una política de transparencia impecable. Este documento será tu guía de ruta para la creación de contenido y futuras colaboraciones con marcas.</p><p>Para completar esta actividad, por favor copia la siguiente plantilla, complétala con la información de tu modelo y pégala en el cuadro de texto de entrega:</p><hr/><p><strong>PLANTILLA DE ENTREGA:</strong></p><pre><code>1. PERFIL BÁSICO:\n- Nombre del modelo:\n- Nicho específico (Ej: Moda circular vintage, Fitness científico, Gaming retro):\n- Audiencia objetivo (¿A quién le habla?): \n\n2. PERSONALIDAD Y VALORES:\n- 3 Rasgos de personalidad (Ej: Analítica, entusiasta, sarcástica, empática):\n- 2 Valores clave o causas que apoya (Ej: Sostenibilidad, salud mental, educación tecnológica):\n\n3. LA BIOGRAFÍA DE LA TRANSPARENCIA (Máximo 150 caracteres):\n[Escribe aquí la biografía para Instagram/TikTok. Debe incluir obligatoriamente una etiqueta como 'Creador Virtual', 'AI Model' o 'Creado con IA' y reflejar la personalidad elegida].\n\n4. DECLARACIÓN DE COMPROMISO ÉTICO (Máximo 100 palabras):\n[Explica brevemente cómo evitarás caer en 'La Mentira Humana' cuando tu modelo interactúe con su comunidad o recomiende productos].</code></pre><hr/><p><strong>¿Qué evaluaremos en tu entrega?</strong></p><ul><li><strong>Coherencia de Nicho:</strong> Que el nicho no sea genérico y que los valores estén alineados con la temática elegida.</li><li><strong>Transparencia Explícita:</strong> Que la biografía no supere los 150 caracteres y que declare abiertamente la naturaleza de IA del modelo de forma creativa y atractiva.</li><li><strong>Enfoque Ético:</strong> Que la declaración de compromiso muestre una estrategia clara para construir una relación honesta y de confianza con la audiencia, evitando engaños sobre la condición humana del personaje.</li></ul>"
                    },
                    "image": {
                        "url": "https://images.pexels.com/photos/12203156/pexels-photo-12203156.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                        "caption": "Foto: Andriall / Pexels",
                        "alt": "Drone shot capturing a coastal scene with boats and greenery in Una-Una, Indonesia.",
                        "source": "Pexels",
                        "photographer": "Andriall",
                        "pexels_url": "https://www.pexels.com/photo/bird-s-eye-view-of-boats-on-shore-12203156/"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: El Gran Reto Técnico: Rostros Consistentes",
            "lessons": [
                {
                    "title": "Consistencia Facial: El Método para Evitar el 'Efecto Camaleón'",
                    "objective": "Aprenderás a estructurar prompts de alta precisión y a utilizar herramientas clave para mantener el rostro de tu modelo virtual idéntico en diferentes poses, ropas y escenarios.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Si alguna vez has intentado crear un personaje con inteligencia artificial, seguro que te has enfrentado al 'efecto camaleón': en una imagen tu modelo es una persona y en la siguiente parece su primo lejano. Este es el talón de Aquiles de la mayoría de los creadores de modelos virtuales y el principal obstáculo para construir una marca creíble.",
                                "Para que las marcas confíen en tu modelo y la audiencia conecte con ella, la consistencia no es negociable. En esta lección, vamos a dominar la fórmula exacta para resolver este reto técnico de raíz, combinando la ingeniería de prompts con las herramientas de referencia más potentes del mercado sin necesidad de instalar programas complejos."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "La consistencia facial no se logra por azar, sino aplicando un método que llamamos 'La Receta Genética'. Consiste en definir un ADN visual único para tu modelo mediante un prompt descriptor muy específico que la IA pueda replicar matemáticamente. En lugar de usar términos genéricos como 'mujer hermosa', mezclamos rasgos étnicos exactos, características asimétricas y detalles fijos (como una cicatriz sutil, pecas en el puente de la nariz o un corte de cabello muy específico).",
                                "Una vez que tienes esta base, entra en juego la tecnología de transferencia de identidad. Herramientas como Midjourney (con el parámetro --cref) o Fooocus (mediante Image Prompt/FaceSwap) permiten tomar esa primera imagen perfecta de tu modelo y usarla como 'ancla'. La IA ya no inventará un rostro desde cero; usará tu ancla y solo adaptará la expresión, la iluminación y el ángulo al nuevo escenario que le pidas."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que queremos crear a 'Elena', una modelo de estilo de vida saludable. En lugar de escribir un prompt simple, estructuramos su ADN visual de la siguiente manera: 'A 24-year-old woman, 70% Spanish and 30% Japanese ancestry, almond-shaped dark eyes, a small distinct mole under her left eye, shoulder-length straight dark hair with curtain bangs, soft natural lighting'.",
                                "Paso 1: Generamos este retrato base y elegimos la mejor versión. Paso 2: Copiamos el enlace de esa imagen. Paso 3: Para la siguiente escena (por ejemplo, Elena tomando un café), escribimos: 'Elena drinking a matcha latte in a cozy Tokyo cafe --cref [URL_DE_TU_IMAGEN] --cw 80'. El parámetro '--cw 80' le dice a la IA que mantenga un 80% de fidelidad al rostro original, permitiendo que la pose y la ropa cambien de forma natural."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más habitual es confiar únicamente en el nombre del personaje. Escribir 'Sofía sentada en el parque' esperando que la IA recuerde quién es Sofía es un billete de ida a la frustración; la IA no tiene memoria a largo plazo de tus creaciones si no le das la referencia visual.",
                                "Otro fallo clásico es sobrecargar el prompt con demasiados accesorios cambiantes en la imagen de referencia (como gafas de sol grandes o sombreros). Si tu imagen base tiene estos elementos, la IA intentará replicarlos en todas las fotos futuras, limitando drásticamente tu flexibilidad para crear contenido variado."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, la consistencia facial se domina definiendo un ADN visual ultra-específico y utilizando funciones de referencia de personajes (como --cref o FaceSwap) para anclar la identidad de tu modelo en cada nueva generación.",
                                "Tu acción recomendada para hoy: Escribe la 'Receta Genética' de tu modelo combinando dos orígenes étnicos y al menos un rasgo físico distintivo e inamovible (pecas, un lunar, un corte de pelo único). Genera sus primeras 4 variantes y selecciona la imagen que se convertirá en tu imagen de referencia oficial."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz de Consistencia Facial: Domina tu ADN Visual",
                        "questions": [
                            {
                                "question": "¿En qué consiste el método de 'La Receta Genética' mencionado en la lección?",
                                "options": [
                                    "Definir un ADN visual único mediante un prompt descriptor muy específico con rasgos étnicos exactos y detalles fijos.",
                                    "Generar cientos de imágenes aleatorias hasta encontrar dos que se parezcan por coincidencia.",
                                    "Instalar un software complejo de diseño 3D para renderizar la cara del personaje.",
                                    "Escribir únicamente términos genéricos como 'mujer hermosa' para darle libertad creativa a la IA."
                                ],
                                "answer": 0,
                                "explanation": "La 'Receta Genética' consiste en definir un ADN visual detallado con rasgos étnicos específicos, características asimétricas y detalles fijos que la IA pueda replicar matemáticamente."
                            },
                            {
                                "question": "En el ejemplo práctico de Midjourney, ¿qué indica el parámetro '--cw 80'?",
                                "options": [
                                    "Que la imagen tardará un 80% menos de tiempo en generarse.",
                                    "Que la IA debe mantener un 80% de fidelidad al rostro original, permitiendo cambios naturales en pose y ropa.",
                                    "Que el rostro del personaje debe verse un 80% más joven que en la imagen de referencia.",
                                    "Que solo se utilizará el 80% de la iluminación original del café de la escena."
                                ],
                                "answer": 1,
                                "explanation": "El parámetro '--cw 80' le dice a la IA que mantenga un 80% de fidelidad con respecto al rostro de referencia, lo que permite que el resto del cuerpo, la ropa y la pose fluyan de forma natural."
                            },
                            {
                                "question": "¿Cuál es uno de los errores comunes más habituales al buscar la consistencia facial?",
                                "options": [
                                    "Mezclar más de un origen étnico en la descripción del prompt de tu modelo.",
                                    "Utilizar el parámetro --cref en Midjourney o la función FaceSwap en Fooocus.",
                                    "Usar una imagen de referencia clara y libre de accesorios para anclar la identidad de la IA.",
                                    "Confiar únicamente en el nombre del personaje (como 'Sofía') esperando que la IA lo recuerde sin darle una referencia visual."
                                ],
                                "answer": 3,
                                "explanation": "Dado que la IA no tiene memoria a largo plazo de tus creaciones anteriores, confiar únicamente en el nombre del personaje es un error común que no mantendrá la consistencia sin una referencia visual."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña el ADN Visual y Escena Consistente de tu Modelo",
                        "type": "Text",
                        "question": "<p>¡Ha llegado el momento de dar vida a tu primera modelo virtual sin que pierda su identidad por el camino! Para esta actividad, asumirás el rol de Director Creativo de <strong>\"Aura Active\"</strong>, una marca de ropa deportiva sostenible. Tu misión es diseñar el ADN visual de su nueva embajadora virtual y preparar los prompts de consistencia para su primera campaña publicitaria.</p><p>Para completar esta actividad con éxito, debes redactar una propuesta que incluya los siguientes tres puntos:</p><ul><li><strong>1. La \"Receta Genética\" (Prompt Base):</strong> Crea el prompt de retrato para tu modelo en inglés. Debe mezclar exactamente dos orígenes étnicos (ej. 60% Swedish, 40% Korean ancestry), definir una edad y añadir un rasgo físico distintivo e inamovible (un lunar, pecas específicas, un corte de cabello muy particular). <em>Recuerda no incluir accesorios temporales como gafas o sombreros para no limitar tus futuras imágenes.</em></li><li><strong>2. El Prompt de Escena (Consistencia de Personaje):</strong> Redacta el prompt para la segunda foto de la campaña (ej. tu modelo trotando en un parque urbano o tomando un smoothie). Incorpora la estructura de consistencia explicada en clase usando el parámetro de Midjourney <code>--cref [URL_DE_TU_IMAGEN] --cw 80</code> (o la lógica equivalente de FaceSwap de Fooocus).</li><li><strong>3. Justificación del ADN y Parámetros:</strong> Explica brevemente por qué elegiste ese rasgo físico distintivo y por qué el peso de consistencia seleccionado (como <code>--cw 80</code>) es el ideal para permitir que la ropa deportiva y la pose cambien de forma natural sin deformar su rostro.</li></ul><p><strong>Formato de entrega:</strong> Copia y pega tu propuesta en el cuadro de texto respetando la siguiente estructura:</p><p><code>- PROMPT BASE: [Tu prompt aquí]<br>- PROMPT DE ESCENA: [Tu prompt aquí]<br>- JUSTIFICACIÓN: [Tu breve explicación aquí]</code></p>"
                    },
                    "image": {
                        "url": "https://images.pexels.com/photos/12203156/pexels-photo-12203156.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                        "caption": "Foto: Andriall / Pexels",
                        "alt": "Drone shot capturing a coastal scene with boats and greenery in Una-Una, Indonesia.",
                        "source": "Pexels",
                        "photographer": "Andriall",
                        "pexels_url": "https://www.pexels.com/photo/bird-s-eye-view-of-boats-on-shore-12203156/"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: Construcción de Marca e Impacto Digital",
            "lessons": [
                {
                    "title": "Estrategia de Lanzamiento: De Cero a Comunidad Activa",
                    "objective": "Aprender a lanzar las redes sociales de tu modelo de IA utilizando una narrativa visual coherente y una estrategia de transparencia que conecte con el público de forma orgánica y ética.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Lanzar las redes de tu modelo virtual no consiste solo en subir imágenes bonitas y esperar a que el algoritmo haga magia. En un ecosistema digital saturado, la diferencia entre un perfil que pasa desapercibido y una marca virtual que genera una comunidad real radica en la narrativa y en la honestidad desde el primer día.",
                                "Muchos creadores cometen el error de intentar engañar a la audiencia haciendo pasar a su modelo por una persona real. Esto, además de ser éticamente cuestionable, destruye la confianza y suele terminar en penalizaciones por parte de las plataformas. Hoy aprenderás a posicionar a tu modelo como un influencer virtual orgulloso de serlo, construyendo una conexión orgánica sólida y duradera."
                            ]
                        },
                        {
                            "heading": "La Estrategia de Narrativa y Transparencia",
                            "paragraphs": [
                                "El primer paso para un lanzamiento exitoso es la transparencia activa. Integrar en la biografía de la cuenta frases como 'Creadora Virtual' o el hashtag #VirtualInfluencer no resta valor; al contrario, atrae a una audiencia fascinada por la tecnología, el arte digital y la innovación. Esta claridad te blinda ante críticas y te posiciona como un creador de vanguardia ante posibles marcas patrocinadoras.",
                                "El segundo pilar es la consistencia visual y el storytelling. Tu cuadrícula de Instagram o feed de TikTok debe contar una historia. Si tu modelo es una entusiasta de la moda sostenible, sus publicaciones, paleta de colores y descripciones deben reflejar ese universo. No compartas imágenes aleatorias: planifica tus primeros 9 posts como una carta de presentación donde se note su personalidad, estilo de vida y valores.",
                                "Por último, el algoritmo premia la interacción humana. Aunque el personaje sea virtual, detrás estás tú. Responde a los comentarios con cercanía, comparte en historias el proceso de 'detrás de cámaras' de cómo creas las imágenes y genera dinámicas donde la audiencia ayude a decidir el próximo outfit o destino de tu modelo."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico: El lanzamiento de 'Aura'",
                            "paragraphs": [
                                "Imagina que has creado a 'Aura', una modelo virtual enfocada en estilo de vida digital y tecnología. Para su lanzamiento en Instagram, planificamos sus primeros tres contenidos clave:",
                                "Post 1 (El Saludo): Una imagen en plano medio de Aura sonriendo en un espacio de trabajo moderno. El texto dice: 'Hola mundo digital. Soy Aura, una creadora de contenido impulsada por IA. Estoy aquí para explorar la intersección entre tecnología, moda y futuro. ¿Te unes al viaje?'.",
                                "Post 2 (Detrás de cámaras - Reel): Un video rápido mostrando el proceso de generación de Aura en tu software de IA, acelerado y con música en tendencia. Texto: 'Creando a Aura: así cobro vida pixel a pixel. ¿Qué estilo deberíamos probar en el próximo post?'.",
                                "Post 3 (Estilo de vida): Aura en una cafetería futurista sosteniendo un café con un look cyberpunk casual. El texto abre un debate sobre el futuro del trabajo remoto. Este mix demuestra que Aura tiene una identidad visual consistente, una voz clara y un propósito definido."
                            ]
                        },
                        {
                            "heading": "Errores comunes y cómo evitarlos",
                            "paragraphs": [
                                "El juego del 'Catfish': Evita a toda costa fingir que es una persona real. Tarde o temprano la audiencia lo descubrirá y la reputación de tu proyecto se desplomará. La honestidad es tu mayor activo comercial.",
                                "Incoherencia estética: Subir hoy una foto fotorrealista hiperdetallada y mañana una que parece un dibujo animado destruye la identidad de tu modelo. Mantén un mismo motor de renderizado, prompts de estilo consistentes y la misma paleta de color en tus publicaciones.",
                                "Ignorar la interacción: Un perfil que solo publica fotos y nunca responde comentarios parece un bot frío. Aunque tu modelo sea de IA, tu gestión de comunidad debe ser 100% humana, cálida y activa."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: El éxito en el lanzamiento de tu modelo virtual se basa en la transparencia, una narrativa temática bien definida y una interacción humana constante detrás de la pantalla. Ser honesto sobre el origen de tu modelo no limita su alcance; potencia su atractivo como innovación tecnológica.",
                                "Tu acción recomendada para hoy: Redacta la biografía de Instagram o TikTok de tu modelo de IA incluyendo un aviso de transparencia (ej. 'Digital Creator | Virtual Muse 🤖'). Diseña el concepto de tus primeros 3 posts de lanzamiento siguiendo el esquema del ejemplo práctico (Presentación, Detrás de cámaras y Estilo de vida) y déjalos listos para publicar."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Lanzamiento de Redes y Conexión Orgánica",
                        "questions": [
                            {
                                "question": "¿Según la lección, por qué es fundamental evitar el juego del 'Catfish' o intentar engañar a la audiencia haciendo pasar a tu modelo por una persona real?",
                                "options": [
                                    "Porque destruye la confianza de la comunidad, daña la reputación del proyecto y suele terminar en penalizaciones por parte de las plataformas.",
                                    "Porque las plataformas de redes sociales cobran una tarifa adicional si detectan que una cuenta simula ser una persona real.",
                                    "Porque es técnicamente imposible que una inteligencia artificial mantenga el fotorrealismo en más de tres publicaciones.",
                                    "Porque las marcas patrocinadoras solo están interesadas en contratar modelos que usen filtros exagerados y obvios."
                                ],
                                "answer": 0,
                                "explanation": "La honestidad es tu mayor activo. Intentar engañar al público destruye la confianza y la reputación a largo plazo, además de exponerte a penalizaciones en las plataformas. Ser un influencer virtual orgulloso atrae a una audiencia apasionada por la innovación."
                            },
                            {
                                "question": "¿Qué estrategia recomienda la lección para evitar el error común de la 'incoherencia estética' en el perfil de tu modelo?",
                                "options": [
                                    "Subir una gran variedad de estilos, desde dibujos animados hasta fotos fotorrealistas, para mostrar versatilidad.",
                                    "Cambiar de paleta de colores en cada publicación para mantener al algoritmo de las plataformas interesado.",
                                    "Mantener un mismo motor de renderizado, prompts de estilo consistentes y una paleta de color definida.",
                                    "Publicar imágenes generadas por diferentes creadores sin un control de calidad para acelerar el ritmo de publicación."
                                ],
                                "answer": 2,
                                "explanation": "Para construir una identidad visual sólida y creíble, es crucial mantener la coherencia estética utilizando el mismo motor de renderizado, prompts de estilo consistentes y una paleta de color unificada."
                            },
                            {
                                "question": "En el ejemplo práctico de 'Aura', ¿cuál es la estructura de contenido propuesta para los primeros tres posts de lanzamiento?",
                                "options": [
                                    "Un post de moda de alta costura, un sorteo de tecnología y un enlace de afiliado para comprar ropa.",
                                    "El Saludo (presentación), el Detrás de cámaras (proceso de creación en video) y el Estilo de vida (con debate).",
                                    "Una comparativa con un influencer real, un post humorístico y una imagen abstracta de arte digital.",
                                    "Un video bailando una tendencia, una infografía técnica sobre IA y una foto de perfil en primer plano."
                                ],
                                "answer": 1,
                                "explanation": "La estrategia de Aura demuestra personalidad, innovación y cercanía a través de un saludo honesto, un reel mostrando cómo cobra vida pixel a pixel y una escena de estilo de vida que invita a la conversación."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña el Kit de Lanzamiento de tu Influencer Virtual",
                        "type": "Text",
                        "question": "<p>¡Ha llegado el momento de dar vida y voz a tu modelo de IA en el mundo real! En esta actividad práctica, diseñarás el <strong>Kit de Lanzamiento Digital</strong> de tu influencer virtual. El objetivo es estructurar una carta de presentación impecable, transparente y altamente atractiva para tu comunidad de lanzamiento.</p><p>Para completar esta actividad, imagina que vas a abrir la cuenta de Instagram o TikTok de tu modelo hoy mismo. Debes redactar y estructurar los siguientes elementos:</p><ul><li><strong>1. Biografía del Perfil:</strong> Redacta una bio de máximo 150 caracteres que defina la personalidad de tu modelo, su propósito y que incluya de forma creativa y clara el descargo de transparencia (ej. 'Creadora digital impulsada por IA', 'Virtual Muse', etc.).</li><li><strong>2. Post 1 (El Saludo - Presentación):</strong> Describe la imagen (pose, vestuario, entorno) y redacta el copy de presentación donde tu modelo se presenta al mundo de forma honesta y cercana.</li><li><strong>3. Post 2 (Detrás de Cámaras - Innovación):</strong> Describe el concepto del video corto (Reel/TikTok) donde mostrarás el proceso de creación digital de tu modelo y redacta un copy interactivo que invite a la audiencia a participar.</li><li><strong>4. Post 3 (Estilo de Vida - Conexión):</strong> Describe una escena cotidiana que refuerce la temática de tu modelo (moda, tecnología, fitness, etc.) y redacta el copy que abra un debate o conversación orgánica con tus seguidores.</li><li><strong>5. Coherencia Estética:</strong> Define 3 colores predominantes de su paleta y el estilo visual (ej. fotorrealismo cyberpunk, estética minimalista pastel, etc.) para mantener un feed armónico.</li></ul><p><strong>Formato de entrega recomendado (copia, completa y envía este esquema):</strong></p><pre>- Nombre del Modelo: \n- Nicho/Temática: \n- Biografía de Instagram (con aviso de IA): \n- Paleta de Colores y Estilo Visual: \n\n- POST 1 (Saludo):\n  * Descripción visual:\n  * Copy/Texto:\n\n- POST 2 (Detrás de Cámaras):\n  * Idea del video/proceso:\n  * Copy/Texto:\n\n- POST 3 (Estilo de Vida):\n  * Descripción visual:\n  * Copy/Texto (con pregunta de interacción):</pre><p><em>Consejo de éxito: No tengas miedo de mostrar que es una IA. El público de hoy valora el arte, la innovación y la honestidad por encima de la falsedad. ¡Crea una identidad que deje huella!</em></p>"
                    },
                    "image": {
                        "url": "https://images.pexels.com/photos/12203156/pexels-photo-12203156.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                        "caption": "Foto: Andriall / Pexels",
                        "alt": "Drone shot capturing a coastal scene with boats and greenery in Una-Una, Indonesia.",
                        "source": "Pexels",
                        "photographer": "Andriall",
                        "pexels_url": "https://www.pexels.com/photo/bird-s-eye-view-of-boats-on-shore-12203156/"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Monetización Transparente y Rentable",
            "lessons": [
                {
                    "title": "Vías de Monetización: Cómo Facturar con tu Modelo Virtual",
                    "objective": "Aprender a implementar las tres vías de ingresos más efectivas (patrocinios, marketing de afiliados y contenido premium) para tu modelo virtual, asegurando la transparencia y la confianza de tu audiencia.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Una vez que has dominado la consistencia visual de tu modelo y has comenzado a construir una comunidad activa en redes sociales, es el momento de transformar esa atención en un negocio digital rentable. La monetización de modelos de inteligencia artificial es un terreno fértil y lleno de oportunidades, pero requiere un enfoque inteligente y transparente.",
                                "Existe la falsa creencia de que las modelos de IA solo pueden generar ingresos a través de plataformas de contenido explícito. La realidad es mucho más corporativa: las marcas reales buscan asociarse con creadores virtuales porque ofrecen un control creativo total, cero riesgos reputacionales y una estética impecable. En esta lección aprenderás a activar tres fuentes de ingresos legítimas y escalables."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para construir un modelo de negocio sostenible, utilizaremos tres pilares fundamentales que puedes activar de forma progresiva. El primero es el Marketing de Afiliados, que consiste en recomendar productos que encajen con el estilo de vida de tu modelo de IA. Utilizando enlaces personalizados, recibirás una comisión por cada venta. La clave aquí es la coherencia: si tu modelo es fitness, promociona suplementos o ropa deportiva; si es una viajera, promueve maletas o software de planificación.",
                                "El segundo pilar son los Patrocinios de Marcas. A medida que tu tasa de interacción crezca, las marcas te pagarán tarifas fijas por integrar sus productos en las imágenes de tu modelo. Para mantener la ética y cumplir con las políticas, siempre debes indicar claramente que la publicación está patrocinada (#Ad, #Patrocinio) y que se trata de un avatar de IA. La transparencia no aleja a las marcas; atrae a empresas serias que valoran la honestidad.",
                                "El tercer pilar es el Contenido Premium y las Membresías. Plataformas como Patreon o Ko-fi te permiten ofrecer experiencias exclusivas a tus seguidores más fieles (acceso a imágenes en ultra-alta definición, fondos de pantalla, o el poder de votar para decidir el próximo outfit de tu modelo). Tus seguidores pagan una suscripción mensual para ser parte activa del proyecto."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que tu modelo de IA se llama 'Aitana', una creadora virtual apasionada por la moda urbana y la tecnología. Para activar tus primeros ingresos de forma rápida, te registras en el programa de afiliados de una tienda de ropa digital o de una marca de gadgets tecnológicos.",
                                "Creas una publicación donde Aitana posa sosteniendo un smartphone de última generación con una estética cyberpunk. En la descripción escribes: 'Organizando mi semana con mi gadget favorito 💜. Puedes conseguir el tuyo con un descuento especial en el enlace de mi biografía #EnlaceAfiliado'.",
                                "Paralelamente, abres un perfil en Ko-fi donde por $3 USD al mes, tus suscriptores acceden a un canal de Discord exclusivo para votar qué marca de ropa debería vestir Aitana en su siguiente sesión fotográfica. Con solo 50 suscriptores recurrentes, ya habrás cubierto los costos de tus herramientas de software y generado tu primera ganancia neta."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "Intentar engañar a la audiencia: El error más grave es tratar de hacer pasar a tu modelo por una persona real de carne y hueso. Tarde o temprano se darán cuenta, te denunciarán por fraude y perderás toda credibilidad. Di siempre con orgullo que es una modelo creada con IA; hoy en día, la tecnología genera curiosidad y admiración.",
                                "Saturar el feed de publicidad: Si cada publicación de tu modelo de IA es un anuncio de venta, la gente dejará de seguirte de inmediato. Mantén siempre la regla del 80/20: 80% de contenido estético, narrativo y de entretenimiento, y solo un 20% enfocado en la monetización directa.",
                                "Promocionar productos de dudosa reputación: Solo porque una marca sospechosa te ofrezca dinero por un patrocinio no significa que debas aceptarlo. Si tu modelo promociona algo que resulta ser una estafa, la marca personal que has construido se destruirá al instante. Investiga siempre a tus socios comerciales."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, monetizar un modelo virtual se reduce a transferir la atención que generas hacia productos y experiencias que aporten valor real. La combinación de marketing de afiliados, patrocinios transparentes y membresías te dará la estabilidad financiera necesaria para escalar tu proyecto.",
                                "Tu acción recomendada para hoy: Elige el primer canal de monetización para tu modelo de IA. Regístrate en un programa de afiliados que encaje con su nicho (como Amazon afiliados, plataformas de moda o herramientas de software) y coloca tu primer enlace en su biografía usando Linktree o Beacons. Diseña y publica un post creativo que integre ese producto de forma natural."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Monetización Ética de Modelos de IA",
                        "questions": [
                            {
                                "question": "Para evitar saturar el feed de tu modelo de IA con publicidad y ahuyentar a tu audiencia, ¿qué regla de distribución de contenido se recomienda seguir?",
                                "options": [
                                    "La regla 50/50: mitad contenido de entretenimiento y mitad anuncios pagados.",
                                    "La regla 80/20: 80% de contenido estético, narrativo y de entretenimiento, y solo un 20% enfocado en monetización directa.",
                                    "Publicar un 100% de contenido de monetización durante los primeros meses para recuperar la inversión.",
                                    "La regla de la discreción: publicar publicidad oculta sin avisar para no alterar el feed estético."
                                ],
                                "answer": 1,
                                "explanation": "La lección establece que para mantener una comunidad saludable debes aplicar la regla del 80/20, asegurando que la gran mayoría de tus posts aporten valor visual o narrativo sin abrumar con ventas."
                            },
                            {
                                "question": "Al trabajar con patrocinios de marcas, ¿cuál es la práctica correcta para mantener la ética y cumplir con las políticas de las redes sociales?",
                                "options": [
                                    "Hacer pasar al modelo por una persona de carne y hueso para generar mayor empatía.",
                                    "Ocultar los hashtags de patrocinio en comentarios secundarios para que el post parezca 100% orgánico.",
                                    "Indicar claramente que la publicación es patrocinada (#Ad, #Patrocinio) y que se trata de un avatar de IA.",
                                    "Aceptar marcas de dudosa reputación siempre que el pago sea por adelantado."
                                ],
                                "answer": 2,
                                "explanation": "La transparencia es fundamental. Indicar con orgullo que tu modelo es un avatar de IA y etiquetar claramente la publicidad mediante hashtags como #Ad o #Patrocinio genera confianza y atrae a marcas serias."
                            },
                            {
                                "question": "Dentro de la vía de ingresos de 'Contenido Premium y Membresías', ¿qué valor se le ofrece a los suscriptores en plataformas como Patreon o Ko-fi?",
                                "options": [
                                    "Acceso a imágenes en ultra-alta definición, el 'detrás de escena' técnico y el poder de votar en decisiones de la narrativa.",
                                    "La propiedad legal y los derechos de autor de las imágenes del modelo de IA.",
                                    "La promesa de que el modelo de IA interactuará físicamente en eventos reales con los suscriptores.",
                                    "Soporte técnico ilimitado para que los suscriptores creen sus propios modelos de IA competidores."
                                ],
                                "answer": 0,
                                "explanation": "Las membresías premium permiten monetizar a tu audiencia más fiel dándoles beneficios exclusivos como fondos de pantalla, acceso a tus métodos de creación técnica y participación activa en el destino o vestuario del avatar."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña tu Estrategia de Monetización Ética",
                        "type": "Text",
                        "question": "<p>¡Es hora de pasar de la teoría a la acción y estructurar el plan financiero de tu modelo de IA! En esta actividad práctica, vas a diseñar una estrategia de monetización real, ética y lista para lanzar al mercado.</p><p><strong>Tu entregable:</strong> Redacta un documento estructurado que responda a los siguientes 4 puntos clave utilizando el editor de texto:</p><ul><li><strong>1. Ficha del Modelo y Nicho:</strong> Indica el nombre de tu modelo de IA, su estilo visual y su público objetivo (ejemplo: 'Aria', apasionada del senderismo y la vida sostenible, dirigida a jóvenes aventureros).</li><li><strong>2. Campaña de Marketing de Afiliados:</strong> Elige un producto o servicio real que encaje con tu nicho. Redacta el copy (texto) de la publicación de Instagram o TikTok donde tu modelo recomiende el producto. Recuerda aplicar la regla del 80/20 (aporta valor visual antes de vender) e incluir de forma visible el hashtag ético (ejemplo: #EnlaceAfiliado).</li><li><strong>3. Estructura de Membresía Premium (Ko-fi / Patreon):</strong> Define dos niveles de suscripción mensual para tus fans más leales. Ponles un precio (en USD) y detalla exactamente qué beneficios exclusivos recibirá el suscriptor en cada nivel (ejemplo: votaciones de vestuario, prompts utilizados, imágenes inéditas en HD).</li><li><strong>4. Publicación Patrocinada 100% Transparente:</strong> Redacta el copy para un patrocinio pagado con una marca ficticia de tu nicho. El texto debe integrar el producto de forma orgánica pero declarando explícitamente y con orgullo que tu modelo es un avatar creado con IA y que es una colaboración pagada (ejemplo: usando #Ad, #CreadoConIA, #Patrocinio).</li></ul><p>Escribe tu propuesta de forma clara, profesional y persuasiva. Esta estructura te servirá como plantilla de negocio para tu proyecto real.</p>"
                    },
                    "image": {
                        "url": "https://images.pexels.com/photos/12203156/pexels-photo-12203156.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                        "caption": "Foto: Andriall / Pexels",
                        "alt": "Drone shot capturing a coastal scene with boats and greenery in Una-Una, Indonesia.",
                        "source": "Pexels",
                        "photographer": "Andriall",
                        "pexels_url": "https://www.pexels.com/photo/bird-s-eye-view-of-boats-on-shore-12203156/"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: Plan de Lanzamiento y Flujo Diario Sostenible",
            "lessons": [
                {
                    "title": "Operación Sostenible: Plan de 7 Días y Rutina de 45 Minutos",
                    "objective": "Diseñar un plan de lanzamiento de 7 días y estructurar una rutina diaria de menos de 45 minutos para gestionar tu modelo de IA de forma constante, ética y sin agotamiento.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¡Ha llegado el momento de la verdad! Tienes la identidad de tu modelo de IA, las imágenes consistentes y tus canales listos. Ahora, el gran reto no es solo publicar, sino hacerlo de una manera organizada que capte la atención del público desde el primer segundo sin consumir todo tu tiempo libre.",
                                "Muchos creadores cometen el error de lanzar su modelo sin un plan, publicando de forma caótica para luego abandonar por frustración o falta de tiempo. En esta lección, aprenderás a estructurar un lanzamiento express de 7 días y a dominar un flujo de trabajo diario tan optimizado que solo te tomará unos minutos al día mantener activo tu nuevo activo digital."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Un lanzamiento exitoso se divide en dos fases críticas: la expectativa y la consistencia. Para la primera fase, utilizaremos el 'Calendario Express de 7 Días'. Durante los primeros tres días, no reveles todo; publica detalles, siluetas o primeros planos de tu modelo con textos que generen curiosidad. Del día 4 al 7, realiza la revelación oficial, comparte su declaración de identidad (dejando claro de forma ética que es una modelo virtual) y lanza tu primer llamado a la acción hacia tu canal de monetización.",
                                "Para la segunda fase, la gestión diaria, debes evitar el agotamiento automatizando y bloqueando tu tiempo. El método de los 45 minutos diarios se divide así: 15 minutos para generar y retocar un lote de imágenes para los próximos días; 15 minutos para programar la publicación del día con sus respectivos copys y hashtags; y 15 minutos finales para interactuar con la audiencia, responder comentarios y conectar con otras cuentas del nicho.",
                                "Recuerda que la transparencia es tu mejor aliada para construir una comunidad leal. Colocar etiquetas como #AIModel, #VirtualInfluencer o aclararlo directamente en la biografía no reduce el interés; al contrario, genera un espacio de confianza y protege tus cuentas de posibles penalizaciones en las plataformas digitales."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que lanzas a 'Elena Tech', una influencer virtual enfocada en productividad y teletrabajo. Tu plan de 7 días se ve así: Día 1 al 3: Publicas un plano detalle de sus manos sobre un teclado estético y un texto que dice: 'Creando algo que cambiará tu forma de organizar el día. ¿Adivinas quién soy?'. Día 4 (El Estreno): Publicas su primer retrato oficial de plano medio, presentándose: '¡Hola! Soy Elena, tu nueva compañera virtual de productividad creada con IA...'.",
                                "A partir del Día 5, aplicas la rutina de 45 minutos. Cada mañana, de 8:00 a 8:45 AM, generas dos nuevas imágenes de Elena en su escritorio usando tus prompts guardados, dejas programado el post del día siguiente usando herramientas gratuitas como Meta Business Suite, y dedicas los últimos minutos a responder de forma empática los comentarios de tus primeros seguidores. En una semana, el proceso se vuelve automático."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es el 'spam de inicio': publicar 10 fotos el primer día y luego desaparecer una semana entera por falta de material. El algoritmo y tu audiencia prefieren la constancia diaria sobre la saturación repentina.",
                                "Otro tropiezo común es jugar al misterio excesivo o engañar a la audiencia haciendo pasar a la modelo por una persona real. Tarde o temprano la comunidad lo descubre, lo que genera rechazo, denuncias y la pérdida total de credibilidad de tu marca virtual.",
                                "Por último, no dejes la creación de contenido para el último momento. Si intentas generar la imagen, editarla, escribir el texto y publicarla justo en el momento en que debes subirla, la prisa arruinará la calidad de tu trabajo."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, un lanzamiento exitoso no requiere de semanas de preparación compleja, sino de un plan de expectativa de 7 días bien ejecutado y de una rutina diaria blindada de 45 minutos que combine generación, programación e interacción honesta.",
                                "Tu acción recomendada para hoy: Define las fechas de tu lanzamiento de 7 días y agenda en tu calendario personal un bloque diario de 45 minutos para la gestión de tu modelo. Prepara hoy mismo las primeras 3 imágenes de expectativa para dar el primer paso sin presiones."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz Express: Lanzamiento y Rutina de tu Modelo de IA",
                        "questions": [
                            {
                                "question": "¿Cómo se estructuran las fases dentro del 'Calendario Express de 7 Días' para garantizar un lanzamiento con impacto?",
                                "options": [
                                    "Días 1 al 3 para generar expectativa (detalles o siluetas) y días 4 al 7 para la revelación oficial y el llamado a la acción.",
                                    "Días 1 al 5 para publicar todo el catálogo de imágenes y días 6 y 7 para responder dudas del público.",
                                    "Los 7 días se dedican a publicar contenido misterioso sin revelar la identidad de la modelo para mantener el interés.",
                                    "Días 1 al 3 de inactividad total y del día 4 al 7 para subir 10 imágenes diarias de golpe."
                                ],
                                "answer": 0,
                                "explanation": "El éxito radica en dividir el lanzamiento en dos fases: los primeros 3 días generas curiosidad con detalles visuales, y del día 4 al 7 haces la revelación oficial aclarando de forma ética que es un modelo virtual."
                            },
                            {
                                "question": "Para gestionar tu modelo de IA en solo 45 minutos al día sin agotarte, ¿cómo debes distribuir este tiempo?",
                                "options": [
                                    "30 minutos buscando referentes en redes y 15 minutos intentando editar imágenes de último minuto.",
                                    "15 minutos para generar y retocar un lote de imágenes, 15 minutos para programar el post del día con copys/hashtags, y 15 minutos para interactuar con la audiencia.",
                                    "45 minutos dedicados exclusivamente a programar publicaciones automáticas para todo el mes.",
                                    "15 minutos de interacción en redes y 30 minutos creando prompts complejos desde cero cada día."
                                ],
                                "answer": 1,
                                "explanation": "El método de los 45 minutos divide tu rutina en tres bloques de 15 minutos: generación/retoque, programación/copywriting e interacción activa. Esto asegura constancia y sostenibilidad."
                            },
                            {
                                "question": "De acuerdo con la lección, ¿cuál es un error grave respecto a la identidad del modelo de IA y cómo se previene de forma ética?",
                                "options": [
                                    "No responder los comentarios negativos; se previene bloqueando a cualquier usuario que haga preguntas.",
                                    "Colocar demasiados hashtags de nicho; se previene usando solo etiquetas genéricas de tecnología.",
                                    "Engañar a la audiencia haciéndola pasar por una persona real; se previene siendo transparente en la biografía o usando etiquetas como #AIModel o #VirtualInfluencer.",
                                    "Crear el contenido con días de anticipación; se previene generando las imágenes justo en el minuto antes de publicar."
                                ],
                                "answer": 2,
                                "explanation": "Hacer pasar a un modelo virtual por una persona real genera rechazo y denuncias cuando se descubre la verdad. La transparencia genera confianza y protege tus cuentas de penalizaciones."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña tu Plan de Despegue y Rutina Sostenible de 45 Minutos",
                        "type": "Text",
                        "question": "<p>¡Es momento de dar vida a tu modelo de IA de forma profesional, ética y sostenible! En esta actividad práctica vas a diseñar la hoja de ruta para el gran estreno de tu modelo y a estructurar tu agenda para que gestionarlo no se convierta en un segundo trabajo agotador.</p><p>Para completar esta actividad, copia la siguiente estructura y complétala con los datos de tu modelo (puedes usar un caso real que estés desarrollando o un proyecto hipotético):</p><strong>1. Ficha del Modelo de IA</strong><ul><li><strong>Nombre del modelo:</strong> [Ej. Lucía Fit]</li><li><strong>Nicho/Temática:</strong> [Ej. Vida saludable y entrenamiento en casa]</li><li><strong>Plataforma principal:</strong> [Ej. Instagram]</li><li><strong>Texto de transparencia para la Biografía:</strong> [Escribe cómo aclarará de forma honesta que es un modelo virtual, incluyendo etiquetas éticas]</li></ul><strong>2. Plan de Lanzamiento Express (7 Días)</strong><ul><li><strong>Días 1 a 3 (Fase de Expectativa):</strong> Describe brevemente qué imágenes conceptuales, siluetas o pistas publicarás y qué dirá el texto para generar curiosidad.</li><li><strong>Día 4 (El Gran Estreno):</strong> Redacta el post de revelación oficial. Debe incluir su presentación de identidad, un toque humano y el descargo ético (que es IA) de forma amigable.</li><li><strong>Días 5 a 7 (Consistencia y CTA):</strong> Describe la temática de las siguientes publicaciones y cuál será el primer llamado a la acción (ej. invitarlos a seguir la cuenta, comentar para recibir un recurso, etc.).</li></ul><strong>3. Bloqueo de Tiempo: Tu Rutina de 45 Minutos</strong><ul><li><strong>Tu bloque horario diario:</strong> [Ej. De 08:30 a 09:15 AM]</li><li><strong>Minutos 1 a 15 (Generación y Retoque):</strong> ¿Qué herramientas usarás y qué lote de imágenes prepararás para tener ventaja?</li><li><strong>Minutos 16 a 30 (Programación y Copy):</strong> ¿Con qué herramienta programarás el post del día siguiente?</li><li><strong>Minutos 31 a 45 (Interacción y Comunidad):</strong> ¿Cómo interactuarás con tu nicho para ganar visibilidad orgánica en esos 15 minutos?</li></ul><p><em>Consejo de éxito: Sé específico con los copys y los horarios. La claridad en esta fase es lo que diferencia a un creador amateur de uno que construye un activo digital escalable sin sufrir burnout.</em></p>"
                    },
                    "image": {
                        "url": "https://images.pexels.com/photos/12203156/pexels-photo-12203156.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                        "caption": "Foto: Andriall / Pexels",
                        "alt": "Drone shot capturing a coastal scene with boats and greenery in Una-Una, Indonesia.",
                        "source": "Pexels",
                        "photographer": "Andriall",
                        "pexels_url": "https://www.pexels.com/photo/bird-s-eye-view-of-boats-on-shore-12203156/"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Dossier de Lanzamiento y Monetización de tu Modelo de IA",
        "type": "Document",
        "question": "<p>¡Felicidades por llegar a la gran prueba final! Has adquirido las habilidades clave para resolver el mayor reto técnico (la consistencia facial) y el mayor reto de negocio (la monetización ética). Ahora es momento de consolidar todo este conocimiento en un único documento estratégico: el <strong>Dossier de Marca y Monetización de tu Modelo de IA</strong>.</p><p>Este proyecto final simula el portafolio profesional que presentarías a marcas aliadas o el plan de ruta que usarás para operar tu negocio digital de forma independiente. Al completarlo, tendrás un activo digital listo para salir al mercado, captar una comunidad real y generar ingresos recurrentes de manera honesta.</p><hr/><h3>PLANTILLA DE ENTREGA:</h3><p>Para realizar tu entrega, copia la siguiente plantilla, completa cada sección con los datos reales de tu proyecto (o un caso hipotético bien estructurado) y pégala en el cuadro de texto de entrega:</p><pre><code>=== SECCIÓN 1: IDENTIDAD Y MARCO ÉTICO ===\n1. Nombre de la Modelo de IA: [Ej. Naomi Jin]\n2. Nicho de mercado específico: [Ej. Nómada digital, entusiasta de la tecnología y el café de especialidad]\n3. Audiencia objetivo: [Ej. Jóvenes profesionales remotos de 22 a 35 años que buscan equilibrar productividad y viajes]\n4. Biografía de Lanzamiento (Máx. 150 caracteres - debe incluir etiqueta de transparencia): [Escribe la biografía aquí]\n5. Compromiso Ético contra la 'Mentira Humana' (Máx. 80 palabras): [Explica cómo responderás si la audiencia pregunta si eres real, o cómo manejarás de forma transparente la promoción de productos].\n\n=== SECCIÓN 2: BLUEPRINT DE CONSISTENCIA VISUAL (La Fórmula Técnica) ===\n1. La 'Receta Genética' (Prompt Base en Inglés para retrato): [Escribe el prompt ultra-específico mezclando dos etnias, edad y rasgo físico inamovible. Sin accesorios temporales].\n2. Escena 1 de Campaña (Prompt de consistencia en inglés): [Escribe el prompt para una foto de acción/estilo de vida usando el parámetro de consistencia --cref o equivalente, ej: Naomi sipping an espresso in a retro Tokyo cafe --cref [URL] --cw 80]\n3. Escena 2 de Campaña (Prompt de consistencia en inglés): [Escribe un segundo prompt en un entorno completamente diferente, ej: Naomi working on her laptop in a co-working space in Bali --cref [URL] --cw 80]\n4. Justificación de Parámetros: [Explica brevemente por qué usaste ese valor de consistencia (como --cw 80) para dar flexibilidad al cuerpo/ropa sin deformar su rostro].\n\n=== SECCIÓN 3: ESTRATEGIA DE CONTENIDO Y REDES (Primeros 3 Posts) ===\n- POST 1: EL SALUDO (Presentación honesta)\n  * Descripción visual de la imagen:\n  * Copy/Texto del post (incluyendo llamado a interactuar):\n\n- POST 2: EL DETRÁS DE CÁMARAS (Innovación y tecnología)\n  * Idea del video/proceso a mostrar:\n  * Copy/Texto del post (invitando a participar/votar):\n\n- POST 3: ESTILO DE VIDA (Conexión temática)\n  * Descripción visual de la imagen:\n  * Copy/Texto del post (con pregunta para abrir debate en el nicho):\n\n=== SECCIÓN 4: MODELO DE NEGOCIO Y OPERACIÓN SOSTENIBLE ===\n1. Canal de Monetización Principal Elegido: [Elige entre Marketing de Afiliados, Patrocinios de Marcas o Membresía Premium (Patreon/Ko-fi)].\n2. Propuesta Comercial (Copy de venta ético): [Redacta el texto de una publicación donde promocionas un producto de afiliado o patrocinado. Debe aportar valor visual, usar el formato 80/20 y tener los hashtags éticos transparentes como #EnlaceAfiliado, #Ad o #ColaboraciónIA].\n3. Beneficios Premium (Si aplica): [Si elegiste membresía, detalla qué ofreces en tu nivel de suscripción mensual de $3-$5 USD].\n4. Tu Rutina Sostenible de 45 Minutos: [Detalla tu horario diario elegido y qué harás exactamente en los bloques de 15 min de Generación, Programación e Interacción].</code></pre><hr/><p><strong>¿Qué evaluará la Inteligencia Artificial en tu entrega?</strong></p><ul><li><strong>Consistencia de Nicho y Marca:</strong> Que el nombre, la biografía, las escenas visuales y la propuesta de monetización estén alineados bajo una identidad y un propósito lógico de mercado.</li><li><strong>Precisión de Ingeniería de Prompts:</strong> Que tu 'Receta Genética' no sea genérica (que use rasgos asimétricos o etnias específicas) y que los prompts de escena apliquen correctamente los parámetros de consistencia como <code>--cref</code> o swap.</li><li><strong>Transparencia Ética Activa:</strong> Que en la biografía y en las copias de venta se declare con orgullo e innovación que es un avatar/creación de IA, cumpliendo las políticas vigentes de las redes sociales.</li><li><strong>Viabilidad de la Operación:</strong> Que tu plan de 45 minutos sea una rutina equilibrada, realizable para un principiante y que prevenga el agotamiento creativo.</li></ul>"
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


def image_block(image_data):
    image_data = image_data or {}
    url = str(image_data.get("url") or "").strip()
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


def build_editorjs_content(lesson_data, quiz_name=None, assignment_name=None):
    blocks = []

    blocks.append(header_block("Objetivo de la lectura", 2))
    blocks.append(paragraph_block(
        lesson_data.get("objective")
        or "Lee esta sección con una idea práctica: al terminar, tendrás una pieza concreta para avanzar en tu proyecto."
    ))

    img = image_block(lesson_data.get("image"))
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
