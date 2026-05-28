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
    "category": "Emprendimiento Digital, Creadores de Contenido e Inteligencia Artificial",
    "title": "Crea tu Influencer Virtual con IA: De Cero a Monetizar en un Fin de Semana",
    "short_introduction": "Domina la creación de modelos hiperrealistas con rostros consistentes y construye un negocio digital altamente rentable de forma 100% anónima.",
    "description": "<p>Aprende el método definitivo para diseñar, posicionar y monetizar tu propia influencer virtual con Inteligencia Artificial. Resuelve el mayor reto del sector: lograr que el rostro de tu modelo se mantenga idéntico en cualquier pose, outfit o escenario, sin necesidad de conocimientos técnicos avanzados.</p><ul><li>Genera imágenes hiperrealistas con prompts de alto rendimiento optimizados para copiar y pegar.</li><li>Crea un feed automatizado en Instagram y TikTok que atraiga miles de seguidores de forma orgánica.</li><li>Monetiza la presencia de tu modelo mediante marcas, marketing de afiliados y plataformas de contenido exclusivo.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza la comprensión, la aplicación real, la claridad y la creatividad antes que la perfección técnica. Valora respuestas naturales, ejemplos útiles y el esfuerzo real. Penaliza respuestas vacías, copiadas, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, áreas de mejora, nota final y el estado: Aprobado (7 o más) o Desaprobado (menor a 7).",
    "chapters": [
        {
            "title": "Módulo 1: El Modelo de Negocio de las Influencers de IA",
            "lessons": [
                {
                    "title": "El Mapa de Ruta: Cómo Facturar de Forma Anónima",
                    "objective": "Comprender el modelo de negocio de las influencers creadas con inteligencia artificial, identificar sus principales vías de ingresos y trazar un plan de acción para lanzar tu proyecto con éxito.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¿Te imaginas gestionar una modelo que trabaja las 24 horas del día, nunca se cansa y puede posar en las playas de Bali o en las calles de Nueva York sin salir de tu computadora? Las influencers de Inteligencia Artificial están revolucionando la economía digital, facturando miles de dólares mensuales y colaborando con marcas de renombre internacional.",
                                "Lo mejor de este negocio es que es 100% accesible. No necesitas costosos equipos fotográficos, viajes caros ni exponerte frente a la cámara. Desde el anonimato y con herramientas gratuitas, puedes diseñar un personaje digital único, construir una audiencia fiel y convertir su presencia en una máquina de generar ingresos pasivos."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "El negocio de las modelos de IA funciona de manera similar al marketing de influencia tradicional, pero con una ventaja competitiva brutal: el control absoluto del tiempo, el espacio y los costos de producción. En lugar de organizar costosas sesiones de fotos, puedes recrear cualquier escenario con un par de líneas de texto (prompts) bien estructuradas.",
                                "Para rentabilizar este activo digital, nos enfocamos en tres fuentes de ingresos principales:",
                                "1. Patrocinios y Publicidad de Marcas: Las empresas buscan constantemente formas innovadoras de anunciarse. Una influencer virtual con un público segmentado es un imán de marketing. Te pagarán por mostrar sus productos, recomendar su app o simular que visita sus instalaciones.",
                                "2. Marketing de Afiliados Estético: Consiste en recomendar productos de terceros a través de enlaces personalizados (como Amazon, Shein o marcas de belleza). Tu influencer muestra cómo luce un outfit o accesorio, y tú te llevas una comisión por cada venta generada.",
                                "3. Contenido Premium y Suscripciones: Plataformas como Patreon o Fanvue permiten ofrecer imágenes exclusivas, sesiones de fotos inéditas o interacción simulada por chat a cambio de una membresía mensual, abriendo un canal de ingresos recurrentes altamente rentable."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Analicemos el caso de 'Aitana López', una de las influencers virtuales pioneras en España. Creada por una agencia de modelos virtuales, Aitana cuenta con más de 300,000 seguidores en Instagram. Su perfil muestra una vida vibrante: va al gimnasio, asiste a eventos y comparte sus outfits diarios.",
                                "¿Cómo factura? Aitana cobra más de 1,000 dólares por publicación patrocinada. Marcas de suplementos deportivos le pagan para que aparezca sosteniendo digitalmente su producto en un entorno de gimnasio realista. Detrás de ella no hay sesiones de fotos caras; solo hay un creador de prompts que diseña sus imágenes de forma consistente desde su escritorio."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave de los principiantes es obsesionarse únicamente con el físico de la modelo y descuidar su personalidad. Una cara bonita hecha con IA abunda en internet, pero la audiencia sigue a personajes por su historia, su estilo de vida y su carisma.",
                                "Otro fallo común es la inconsistencia visual. Si tu influencer cambia drásticamente de facciones entre una publicación y otra, perderás la confianza de tu audiencia al instante. La consistencia del rostro es la regla de oro.",
                                "Finalmente, muchos creen que necesitan software de pago costoso para comenzar. Esto es falso. Puedes validar tu idea de negocio y conseguir tus primeros miles de seguidores optimizando herramientas gratuitas al máximo."
                            ]
                        },
                        {
                            "heading": "Resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Crear una influencer virtual es un modelo de negocio altamente escalable, de bajo costo y anónimo. La monetización llega de forma orgánica mediante patrocinios, afiliados y contenido premium una vez que construyes consistencia visual y comunidad.",
                                "Tu acción recomendada: Dedica 15 minutos a buscar en Instagram o TikTok tres cuentas de influencers virtuales existentes (puedes buscar términos como 'virtual influencer' o analizar perfiles como @fit_aitana). Observa qué tipo de contenido suben, cómo interactúan en los comentarios y qué productos promocionan en su biografía. Anota el nicho que más te llame la atención."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: El Negocio de las Influencers Virtuales",
                        "questions": [
                            {
                                "question": "Según la lección, ¿cuáles son las tres vías más lucrativas para monetizar una influencer de IA?",
                                "options": [
                                    "Venta de cursos en línea, regalías por música de IA y consultoría digital.",
                                    "Patrocinios de marcas, marketing de afiliados estético y contenido premium por suscripción.",
                                    "Desarrollo de software, venta de ropa física propia y donaciones en transmisiones en vivo.",
                                    "Alquiler de servidores, servicios de diseño web y publicidad en motores de búsqueda."
                                ],
                                "answer": 1,
                                "explanation": "El texto detalla que las marcas pagan por publicidad, se ganan comisiones por recomendar productos mediante enlaces de afiliados y se cobra membresía mensual por contenido exclusivo."
                            },
                            {
                                "question": "Para evitar perder la confianza de la audiencia rápidamente, ¿cuál es la regla de oro que debes seguir con la imagen de tu modelo?",
                                "options": [
                                    "La consistencia visual, asegurándote de no cambiar drásticamente sus facciones en cada publicación.",
                                    "Modificar su rostro constantemente para adaptarte a las tendencias del día.",
                                    "Invertir obligatoriamente en las herramientas de generación de imágenes más costosas desde el día uno.",
                                    "Hacer que tu modelo luzca diferente cada día para mantener el misterio de la cuenta."
                                ],
                                "answer": 0,
                                "explanation": "Mantener las facciones físicas estables y coherentes (consistencia visual) es vital para que la audiencia perciba al personaje como alguien real y confiable."
                            },
                            {
                                "question": "En el caso práctico de la influencer virtual 'Aitana López', ¿qué recurso es el que realmente genera sus imágenes diarias?",
                                "options": [
                                    "Un costoso equipo de fotógrafos que viajan con una modelo de carne y hueso.",
                                    "Un creador de prompts que diseña las imágenes desde su escritorio.",
                                    "Un sistema robótico que captura imágenes de videojuegos en tendencia.",
                                    "Un software secreto y exclusivo que solo agencias de moda tradicionales pueden adquirir."
                                ],
                                "answer": 1,
                                "explanation": "Aitana demuestra que no se necesitan costosas sesiones de fotos ni viajes, sino un diseñador que domine la creación de imágenes mediante prompts desde su computadora."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu Primer Blueprint de Influencer Virtual",
                        "type": "Text",
                        "question": "<p>¡Felicidades por completar la primera lección! Ahora pasaremos de la teoría a la acción. Vas a diseñar el <strong>\"Blueprint de Identidad y Monetización\"</strong> de tu primera influencer virtual.</p><p>Este mapa de ruta inicial será la base para construir tu personaje digital de manera estratégica, asegurando que tenga coherencia visual y un propósito comercial claro desde el primer día.</p><p><strong>Instrucciones:</strong> Copia la plantilla que encontrarás abajo, rellénala con las decisiones estratégicas de tu proyecto (puede ser real o un caso práctico para practicar) y envíala en el cuadro de texto para su evaluación.</p><hr/><p><strong>PLANTILLA PARA ENVIAR:</strong></p><p><strong>1. Identidad de la Modelo:</strong></p><ul><li><strong>Nombre de tu influencer virtual:</strong> [Ej: Sofía Green, Kai Romero]</li><li><strong>Nicho específico:</strong> [Ej: Moda urbana y streetwear, Fitness e higiene mental, Estilo de vida geek y videojuegos]</li><li><strong>Personalidad y Valores (3 adjetivos):</strong> [Ej: Divertida, ecologista y transparente]</li></ul><p><strong>2. Historia de Fondo (Storytelling):</strong></p><ul><li>Escribe un párrafo corto (de 3 a 5 líneas) sobre quién es, qué hace en su día a día y por qué su público objetivo querría seguirla. Evita crear una cara bonita sin alma; dale un propósito a su cuenta.</li></ul><p><strong>3. Estrategia de Monetización (Elige y detalla mínimo 2 de las vías explicadas en la lección):</strong></p><ul><li><strong>Vía 1:</strong> [Describe cómo la aplicarás. Ej: Marketing de afiliados recomendando sets de ropa deportiva low-cost en su biografía]</li><li><strong>Vía 2:</strong> [Describe cómo la aplicarás. Ej: Contenido Premium en Patreon donde compartirá tutoriales de estilo digital y sesiones de fotos inéditas estilo cyberpunk]</li></ul><p><strong>4. Estándar de Consistencia Visual:</strong></p><ul><li>Para evitar que tu modelo cambie drásticamente de apariencia y pierda credibilidad, define sus 3 rasgos físicos innegociables que deberás mantener siempre en tus prompts: [Ej: Cabello pelirrojo rizado, pecas suaves en la nariz, ojos verdes almendrados]</li></ul><hr/><p><em>Consejo para el éxito: Asegúrate de que la estrategia de monetización tenga coherencia con el nicho elegido. ¡El evaluador estará listo para darte feedback detallado de tu propuesta!</em></p>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: ADN de Marca e Identidad de Impacto",
            "lessons": [
                {
                    "title": "Identidad de Impacto: Diseñando el Estilo de Vida y la Estética de tu Modelo",
                    "objective": "Aprender a definir el nombre, la personalidad, la estética y la narrativa de tu influencer de IA para construir una marca virtual magnética y coherente antes de generar tu primera imagen.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Antes de abrir cualquier herramienta de IA o escribir un solo prompt, debemos entender un principio fundamental: en el mundo de los influencers virtuales, la belleza sin propósito es invisible. Una cara bonita ya no es suficiente para destacar en redes. Lo que realmente detiene el scroll es la identidad, la historia y la vibra que transmite el personaje.",
                                "Piensa en tus creadores favoritos. No los sigues solo por su aspecto; te interesan los lugares que visitan, el café que toman, su estilo al vestir y cómo se comunican. En esta lección, vamos a diseñar el plano de tu modelo virtual, asegurando que cada imagen futura tenga una dirección clara y comercialmente viable."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para crear una identidad de impacto, estructuraremos la marca de tu modelo en tres pilares esenciales: el Perfil Demográfico, el Arquetipo de Estilo de Vida y el Universo Visual.",
                                "1. El Perfil Demográfico define lo básico: su nombre, edad, nacionalidad y ciudad de residencia. Esto le da un anclaje realista. Si tu modelo vive en una ciudad como Madrid, sus fondos naturales serán cafeterías modernas, calles con arquitectura europea y parques urbanos.",
                                "2. El Arquetipo de Estilo de Vida define su nicho y su rutina diaria. ¿Es una entusiasta del fitness que entrena al amanecer, o una nómada digital que trabaja desde playas tropicales? Esto determina el tipo de contenido que publicarás.",
                                "3. El Universo Visual establece su paleta de colores dominante y su estilo de vestir. ¿Usará tonos neutros y minimalistas, o colores vibrantes de estilo urbano? Mantener este universo visual es lo que hará que tu feed se vea profesional y armonioso a primera vista."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imaginemos que creamos a 'Valeria Soler', de 23 años, residente de Barcelona y enfocada en el estilo de vida saludable y la moda sostenible. Su personalidad es alegre, activa y cercana. Su Universo Visual se compone de colores tierra, verdes suaves y luz natural. Vestirá ropa deportiva minimalista y vestidos de lino ligeros.",
                                "Teniendo este mapa claro, al generar imágenes ya no estarás adivinando el prompt. En lugar de pedirle a la IA 'una mujer en la calle', escribirás: 'Valeria, una joven de 23 años con cabello castaño claro, vistiendo un conjunto deportivo beige de alta calidad, sosteniendo un vaso de matcha latte helado mientras camina sonriente por una calle soleada de Barcelona, fotografía de estilo de vida de Instagram, iluminación suave de la mañana'. La identidad dicta el prompt y garantiza la coherencia."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es la inconsistencia de nicho. Mostrar un día a tu modelo en un festival de música techno con ropa futurista, y al día siguiente cocinando pan casero en una cocina rústica confunde al algoritmo y a los seguidores, destruyendo la ilusión de realidad.",
                                "Otro error es elegir una estética demasiado compleja o costosa de replicar visualmente en los prompts (como 'astronauta de moda en Marte') cuando el objetivo real es colaborar con marcas locales de ropa. Mantén la vida de tu modelo aspiracional pero alcanzable."
                            ]
                        },
                        {
                            "heading": "Resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: una influencer virtual exitosa nace de una identidad sólida, no de la aleatoriedad. Al definir su perfil, estilo de vida y universo visual, creas una guía que simplifica la generación de prompts y asegura un feed coherente y atractivo.",
                                "Tu acción recomendada: Diseña la Ficha de Identidad de tu modelo. Escribe en un documento: 1) Nombre y edad. 2) Ciudad donde reside. 3) Nicho principal. 4) Tres adjetivos que describan su personalidad. 5) Estilo de vestir y los tres colores principales de su feed. Este documento será tu brújula visual."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz corto: Identidad de Impacto de tu Modelo de IA",
                        "questions": [
                            {
                                "question": "¿Cuáles son los tres pilares esenciales en los que se debe estructurar la marca de tu modelo virtual para crear una identidad de impacto?",
                                "options": [
                                    "El Perfil Demográfico, el Arquetipo de Estilo de Vida y el Universo Visual.",
                                    "La Plataforma de IA, el Presupuesto de Marketing y la Red Social de Destino.",
                                    "El Nivel de Realismo, los Prompts de Texto y la Edición de Fotografía.",
                                    "La Ficha Técnica, el Número de Hashtags y el Algoritmo de Publicación."
                                ],
                                "answer": 0,
                                "explanation": "La lección establece que para construir una identidad de impacto debemos estructurar la marca en tres pilares: el Perfil Demográfico (quién es y dónde vive), el Arquetipo de Estilo de Vida (su nicho y rutina) y el Universo Visual (colores y estilo de vestir)."
                            },
                            {
                                "question": "De acuerdo con la lección, ¿cuál es el error más grave que cometen los principiantes al crear su modelo virtual?",
                                "options": [
                                    "Usar siempre el mismo prompt para generar todas las imágenes de la modelo.",
                                    "Elegir un nombre de usuario que sea demasiado largo o difícil de pronunciar.",
                                    "La inconsistencia de nicho, como mostrar a la modelo en entornos opuestos e inexplicables de un día para otro.",
                                    "No utilizar hashtags de moda en las primeras publicaciones en redes sociales."
                                ],
                                "answer": 2,
                                "explanation": "La inconsistencia de nicho confunde tanto al algoritmo como a los seguidores, destruyendo la ilusión de que el personaje virtual es una persona real con una vida lógica."
                            },
                            {
                                "question": "¿Cuál es la acción práctica recomendada al final de la lección para comenzar a diseñar tu influencer virtual?",
                                "options": [
                                    "Rellenar la Ficha de Identidad de tu modelo con datos básicos como su nombre, edad, ciudad, nicho, personalidad y estilo visual.",
                                    "Abrir inmediatamente una cuenta de Instagram y comenzar a publicar imágenes aleatorias.",
                                    "Comprar un software de inteligencia artificial avanzado para generar prompts complejos.",
                                    "Buscar patrocinadores locales para tu modelo antes de definir su estilo visual."
                                ],
                                "answer": 0,
                                "explanation": "La acción recomendada para hoy es rellenar la Ficha de Identidad en un bloc de notas (definiendo nombre, edad, ciudad, nicho, personalidad y estilo de vestir con sus colores principales), lo cual servirá como brújula para los siguientes pasos."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña el Plano de Identidad de tu Influencer de IA",
                        "type": "Text",
                        "question": "<p>¡Es hora de dar vida a tu personaje! En esta actividad práctica, vas a diseñar el <strong>Plano de Identidad</strong> de tu influencer virtual. Este documento evitará que generes imágenes aleatorias y te servirá como la guía definitiva para mantener la consistencia estética y narrativa en todas tus futuras publicaciones.</p><p><strong>¿Qué debes entregar?</strong></p><p>Copia la plantilla que aparece a continuación, completa los datos de tu modelo y pégala en el cuadro de texto con tus respuestas:</p><hr/><p><strong>PLANTILLA: FICHA DE IDENTIDAD DE MI MODELO</strong></p><p><strong>1. Perfil Demográfico</strong><br>- Nombre y apellido:<br>- Edad:<br>- Ciudad y país donde reside (esto definirá tus fondos arquitectónicos o naturales):</p><p><strong>2. Arquetipo de Estilo de Vida</strong><br>- Nicho principal (ej. fitness, moda urbana, tecnología/gaming, viajes de lujo):<br>- Tres adjetivos de personalidad (ej. carismática, introvertida, enérgica, sofisticada):<br>- Rutina o actividad diaria típica (ej. tomar un café frío mientras trabaja en su laptop, entrenar al amanecer):</p><p><strong>3. Universo Visual</strong><br>- Estilo de vestir dominante (ej. ropa deportiva minimalista, streetwear colorido, trajes de lino neutros):<br>- Tres colores predominantes de su feed de Instagram:<br>- Tipo de iluminación preferida (ej. luz natural de tarde, luces de neón nocturnas, iluminación suave de estudio):</p><p><strong>4. Tu Primer 'Prompt de Oro'</strong><br>- Escribe un prompt detallado (en español o inglés) de 3 o 4 líneas que describa la primera foto de tu modelo aplicando su identidad. Recuerda incluir: su descripción básica, su ropa, la acción que realiza, el entorno y el estilo de iluminación.</p><hr/><p><strong>Instrucciones para la evaluación:</strong></p><ul><li>Asegúrate de que el estilo de vestir y los colores coincidan con el nicho elegido (por ejemplo, tonos tierra y lino para moda sostenible).</li><li>Evita las contradicciones (ej. una modelo de estilo de vida campestre y rústico en un entorno de rascacielos futuristas).</li><li>El 'Prompt de Oro' debe ser tan descriptivo que cualquier persona (o IA) pueda visualizar exactamente la misma escena al leerlo.</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: Fotografía Hiperrealista y Consistencia Facial",
            "lessons": [
                {
                    "title": "Método Express: Fotos Profesionales con Consistencia Facial",
                    "objective": "Aprender a estructurar prompts de alto rendimiento y dominar técnicas de consistencia facial para generar fotos hiperrealistas de alta calidad en segundos.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Uno de los mayores obstáculos al crear una influencer virtual es lograr que se vea como la misma persona en cada publicación. Al cambiar el escenario o la ropa, el rostro suele cambiar por completo, lo que destruye la credibilidad de tu cuenta de inmediato.",
                                "En esta lección vas a dominar el Método de Generación Express. Te daremos las estructuras de prompt exactas y la lógica técnica para que puedas vestir, trasladar y hacer posar a tu modelo en cualquier lugar del mundo, manteniendo su identidad facial intacta y con un acabado fotorrealista profesional."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para lograr consistencia visual y realismo extremo, nos apoyamos en dos pilares: un prompt base perfectamente estructurado y una herramienta de transferencia de identidad (como IP-Adapter en Midjourney, Fooocus o InsightFace). La IA necesita indicaciones muy específicas para no inventar rasgos nuevos cada vez.",
                                "Un prompt optimizado para redes sociales sigue un orden estricto: 1) Sujeto y rasgos clave (edad, etnia, cabello), 2) Acción o pose natural, 3) Outfit detallado, 4) Entorno o fondo, y 5) Estilo de cámara e iluminación. En lugar de usar palabras vacías como «fotorrealista» o «8k», utilizamos términos técnicos de fotografía como «iluminación natural difusa», «lente de 35mm» o «textura de piel visible». Esto le indica a la IA que emule una cámara profesional real, no un render de videojuego."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que necesitas publicar una foto de tu modelo tomando un café por la mañana. El proceso consiste en cargar la imagen de referencia de tu modelo (tu «áncora facial») en tu generador de IA preferido y aplicar el siguiente prompt adaptado:",
                                "«Usa nuestra modelo IA de referencia. Fotografía de estilo de vida en redes sociales de una mujer de 24 años, cabello castaño claro con ondas naturales, vistiendo un blazer de lino beige y una camiseta blanca. Sentada en la terraza de una cafetería urbana moderna, sosteniendo una taza de café, mirando de reojo con una sonrisa sutil. Iluminación de mañana suave, profundidad de campo desenfocada, tomada con lente de 50mm, textura de piel realista, calidad de publicación de Instagram.»",
                                "Este prompt proporciona a la IA las coordenadas exactas de vestuario, actitud y fotografía para clonar el rostro de tu modelo sobre una escena hiperrealista y cotidiana."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error número uno es usar palabras de relleno como «ultra detallado», «obra maestra» o «perfecto». Esto satura el algoritmo de la IA y hace que ignore las instrucciones de consistencia facial. Mantén tus prompts descriptivos pero directos.",
                                "Otro fallo clásico es cambiar radicalmente la etnia, la estructura ósea o la edad en el texto del prompt mientras aplicas la cara de referencia. Si tu modelo base es una joven de 20 años y en el prompt describes una «mujer de 45 años», la IA generará un híbrido extraño y poco natural. La coherencia textual debe respaldar a la visual."
                            ]
                        },
                        {
                            "heading": "Resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, el secreto de las imágenes consistentes está en la estructura del prompt (sujeto, acción, outfit, fondo y cámara) combinada con una imagen de referencia facial fija. Al hablar el lenguaje de la fotografía real, la IA entrega resultados humanizados y listos para publicar.",
                                "Tu acción recomendada: Elige tu generador de imágenes de IA preferido (como Fooocus, SeaArt o Midjourney), selecciona la foto principal de tu modelo como referencia facial (usando face-swap o IP-Adapter) y copia el prompt del ejemplo práctico. Genera 3 variaciones cambiando únicamente el color del outfit o el fondo, y guarda la más natural."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: El Método de Generación Express",
                        "questions": [
                            {
                                "question": "¿Cuál es el orden estricto que debe seguir un prompt ultra optimizado para redes sociales según la lección?",
                                "options": [
                                    "1) Sujeto y rasgos, 2) Acción o pose, 3) Outfit, 4) Entorno o fondo, y 5) Cámara e iluminación.",
                                    "1) Cámara e iluminación, 2) Outfit, 3) Sujeto, 4) Entorno o fondo, y 5) Acción.",
                                    "1) Entorno o fondo, 2) Acción, 3) Outfit, 4) Cámara e iluminación, y 5) Sujeto.",
                                    "1) Outfit, 2) Sujeto y rasgos, 3) Entorno o fondo, 4) Cámara e iluminación, y 5) Acción."
                                ],
                                "answer": 0,
                                "explanation": "Para que la IA no invente rasgos nuevos, el prompt debe seguir un orden lógico y estricto: primero el sujeto, luego su acción, el vestuario, el fondo y, finalmente, las especificaciones de la cámara y la luz."
                            },
                            {
                                "question": "¿Por qué se debe evitar el uso de palabras de relleno como «ultra detallado» o «obra maestra»?",
                                "options": [
                                    "Because they cost more to generate in premium engines.",
                                    "Porque saturan el algoritmo de la IA y hacen que ignore las instrucciones de consistencia facial.",
                                    "Porque modifican de manera aleatoria el género del personaje principal.",
                                    "Porque hacen que la imagen se exporte en un formato no compatible con Instagram."
                                ],
                                "answer": 1,
                                "explanation": "Las palabras vacías confunden al algoritmo. En su lugar, el texto recomienda usar términos descriptivos y técnicos de fotografía para obtener un resultado realista y consistente."
                            },
                            {
                                "question": "¿Qué ocurre si en el prompt de texto describes rasgos físicos que contradicen por completo a tu imagen de referencia?",
                                "options": [
                                    "La IA generará un híbrido extraño y poco natural, ya que la coherencia textual debe respaldar a la visual.",
                                    "El generador de IA se bloqueará de inmediato y mostrará un mensaje de error.",
                                    "La IA ignorará por completo el texto y solo usará los datos de la imagen de referencia.",
                                    "La imagen final saldrá perfecta gracias al autoajuste del IP-Adapter."
                                ],
                                "answer": 0,
                                "explanation": "Si intentas cruzar datos opuestos (como describir a una mujer de rasgos nórdicos usando la referencia de una joven de rasgos asiáticos), la IA intentará fusionar ambas instrucciones, creando un resultado deforme y poco creíble."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Crea el Primer 'Lookbook' Coherente de tu Influencer Virtual",
                        "type": "Text",
                        "question": "<p>¡Es hora de crear las primeras imágenes profesionales de tu influencer virtual! En esta actividad, diseñarás dos escenarios completamente diferentes para tu modelo (uno profesional y uno casual) aplicando la <strong>estructura de prompt en 5 pasos</strong> para asegurar la consistencia y el hiperrealismo visual.</p><p><strong>Tu objetivo:</strong> Definir el perfil de tu modelo y redactar dos prompts optimizados listos para usar en tu generador de IA preferido, usando una imagen de referencia facial.</p><p><strong>Instrucciones para tu entrega:</strong></p><ol><li><strong>Define tu Modelo Base:</strong> Describe brevemente la edad, rasgos clave, etnia y estilo general de tu personaje (esta será tu ancla visual).</li><li><strong>Diseña el Prompt 1 (Perfil Profesional - Oficina/Negocios):</strong> Escribe un prompt siguiendo estrictamente la estructura de 5 pasos: Sujeto, Acción, Vestuario, Entorno, y Cámara e iluminación profesional (sin usar términos genéricos como '8k' o 'ultradetallado').</li><li><strong>Diseña el Prompt 2 (Perfil Casual - Fin de Semana/Estilo de vida):</strong> Mantén exactamente el mismo sujeto y rasgos del paso anterior, pero cambia la acción, el outfit, el fondo y la iluminación para simular una foto de día libre (ej. en una cafetería o parque).</li><li><strong>Estrategia técnica:</strong> Explica qué herramienta de transferencia de identidad (como Face-Swap, IP-Adapter o InsightFace) planeas utilizar para lograr un rostro idéntico.</li></ol><p><strong>Formato de entrega:</strong> Copia y pega tu respuesta en el cuadro de texto siguiendo esta estructura:</p><pre>- Perfil de la Modelo Base: [Edad, etnia, rasgos]\n- Prompt 1 (Profesional): [Sujeto + Acción + Outfit + Fondo + Cámara]\n- Prompt 2 (Casual): [Sujeto + Acción + Outfit + Fondo + Cámara]\n- Herramienta y estrategia de consistencia: [Tu explicación de 2 o 3 líneas]</pre>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Crecimiento Acelerado en Instagram y TikTok",
            "lessons": [
                {
                    "title": "Algoritmo Viral: Planificación y Retención Orgánica",
                    "objective": "Comprender el funcionamiento de los algoritmos de Instagram Reels y TikTok para estructurar, programar y viralizar el contenido de tu influencer de IA de forma orgánica.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Tener las fotos más fotorrealistas de tu influencer de IA no sirve de nada si se quedan guardadas en tu computadora. El éxito en redes sociales no depende solo de la calidad visual, sino de entender cómo distribuyen el contenido las plataformas. Al no ser una persona real, la curiosidad de la audiencia es tu mayor aliada para viralizar de forma orgánica.",
                                "En esta lección aprenderás a estructurar tus publicaciones de manera estratégica, optimizando el tiempo de visualización y la interacción para que los algoritmos de Instagram y TikTok distribuyan tu contenido de manera masiva y automática."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Las redes sociales priorizan una métrica por encima de todas: el tiempo de retención (watch time). Si un usuario ve tu video hasta el final, la plataforma asume que es contenido valioso y lo muestra a un público mayor. Para lograr esto con una modelo de IA, convertimos las imágenes estáticas en videos cortos dinámicos (usando sutiles efectos de zoom 3D o transiciones estéticas) acompañados de audios en tendencia.",
                                "La estructura de un video corto de alto impacto consta de tres partes esenciales:",
                                "1. El gancho (hook): Un texto llamativo en los primeros 2 segundos que detenga el scroll y despierte intriga.",
                                "2. El cuerpo: Un fragmento visualmente estético de tu modelo que mantenga al usuario enganchado de 5 a 8 segundos.",
                                "3. La llamada a la acción (CTA): Una instrucción clara en el video o la descripción que invite a comentar, guardar o compartir. Los compartidos e interacciones multiplican el alcance viral de inmediato.",
                                "La consistencia es clave. El algoritmo premia la constancia porque quiere retener a los usuarios activos. Lo ideal para una cuenta nueva es publicar un video corto al día en horarios estratégicos, utilizando herramientas de programación nativas para automatizar el proceso."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que vas a lanzar tu primer video para tu modelo de IA enfocada en el estilo de vida saludable. En lugar de subir una foto simple, creas un video de 6 segundos usando una imagen de ella en el gimnasio, aplicando un efecto de movimiento lento de cámara (3D Zoom en CapCut) y un audio en tendencia.",
                                "En pantalla colocas un texto: 'El secreto que cambió mi rutina matutina en 5 días (léelo abajo)...'. En la descripción escribes un texto breve pero de mucho valor con 3 tips de mentalidad, y cierras con una pregunta. Al dirigir al usuario a la descripción, este pasará 10 segundos leyendo mientras el video de 6 segundos se repite en bucle tres veces de fondo. Para el algoritmo esto representa una retención del 300%, impulsando tu publicación a la sección de sugeridos y explorar de inmediato."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es el síndrome de 'publicar y huir'. Subir el contenido y cerrar la aplicación reduce el alcance. Las plataformas miden la actividad de tu cuenta justo después de publicar; debes quedarte al menos 15 minutos interactuando con cuentas de tu nicho y respondiendo comentarios para validar tu actividad.",
                                "Otro fallo común es publicar videos con marcas de agua de otras aplicaciones (como editar en TikTok y resubirlo con la marca a Instagram). Los algoritmos penalizan de forma severa el contenido con logos de la competencia. Exporta tus videos limpios desde herramientas externas como CapCut e integra los audios nativos dentro de cada app."
                            ]
                        },
                        {
                            "heading": "Resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen, el crecimiento orgánico es una ciencia de retención y constancia. Estructura tus videos cortos con ganchos visuales potentes, redirige al usuario al caption para generar reproducciones en bucle y automatiza tus publicaciones diariamente.",
                                "Tu acción recomendada: Elige las 3 mejores imágenes de tu modelo. Importalas en CapCut y conviértelas en videos de 6 segundos con efectos de movimiento suave. Busca un audio en tendencia en redes, escribe un gancho atractivo de texto para pantalla y programa estas publicaciones para los próximos 3 días usando las herramientas nativas."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Domina el Algoritmo y Viraliza tu Influencer de IA",
                        "questions": [
                            {
                                "question": "¿Cuál es la métrica principal que priorizan tanto Instagram Reels como TikTok para distribuir tu contenido?",
                                "options": [
                                    "El tiempo de retención (watch time) y el porcentaje de finalización.",
                                    "El número de hashtags y etiquetas de geolocalización.",
                                    "La cantidad de seguidores acumulados en la cuenta.",
                                    "La resolución exacta en píxeles del video exportado."
                                ],
                                "answer": 0,
                                "explanation": "El algoritmo asume que un video es de alta calidad y merece ser mostrado a más personas si los usuarios lo ven hasta el final o lo reproducen en bucle."
                            },
                            {
                                "question": "En el ejemplo práctico, ¿qué estrategia se utiliza para lograr una retención del 300% con un video de 6 segundos?",
                                "options": [
                                    "Configurar una reproducción automática en cámara ultra lenta.",
                                    "Dirigir al usuario a leer una descripción (caption) valiosa que le tome unos 10 segundos leer mientras el video corre de fondo.",
                                    "Pagar una campaña de publicidad de bajo costo para forzar las vistas.",
                                    "Colocar un temporizador visual en la pantalla para retrasar al espectador."
                                ],
                                "answer": 1,
                                "explanation": "Al invitar al usuario a leer tips en el caption, pasa más tiempo interactuando con tu post mientras el video corto se reproduce varias veces en bucle de forma automática."
                            },
                            {
                                "question": "¿En qué consiste el error de 'publicar y huir' mencionado en la lección?",
                                "options": [
                                    "Subir contenido y cerrar la aplicación de inmediato, perdiendo la oportunidad de interactuar en los primeros 15 minutos clave.",
                                    "Publicar contenido sin usar filtros o efectos de movimiento visual.",
                                    "Subir un video y borrarlo a los pocos minutos si no tiene me gustas.",
                                    "Utilizar videos editados con marcas de agua de plataformas de la competencia."
                                ],
                                "answer": 0,
                                "explanation": "Las plataformas miden la actividad de tu cuenta justo después de publicar. Quedarte al menos 15 minutos interactuando y respondiendo comentarios le indica al algoritmo que tu cuenta está activa y saludable."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: Diseño de un Reel de Retención Infinita",
                        "type": "Text",
                        "question": "<p>¡Es hora de poner a trabajar el algoritmo a tu favor! Vas a diseñar la estructura de tu primer Reel o TikTok de alto impacto aplicando la <strong>técnica de retención infinita (bucle de visualización)</strong>.</p><p>Para completar la actividad, escribe tu propuesta en el cuadro de texto desarrollando los siguientes 4 puntos clave:</p><ul><li><strong>1. El Gancho Visual (Hook):</strong> Describe en un párrafo cómo será el video de tu influencer de 6 segundos (ej. imagen de tu modelo usando zoom 3D en CapCut con un audio en tendencia). Escribe el <em>texto exacto</em> que aparecerá en pantalla los primeros 2 segundos (ej: 'El truco de productividad que me salvó la semana...').</li><li><strong>2. El Copia de la Descripción (Caption de Bucle):</strong> Redacta el texto completo que irá en el pie de foto. Debe contener valor real escrito de forma atractiva para que al usuario le tome entre 10 y 15 segundos leerlo mientras el video se reproduce en bucle.</li><li><strong>3. Llamada a la Acción (CTA):</strong> Escribe la frase final de tu descripción diseñada para incentivar la interacción (guardados, comentarios o compartidos).</li><li><strong>4. Plan 'Anti-Huida':</strong> Enumera 3 acciones específicas que realizarás dentro de la plataforma durante los 15 minutos posteriores a publicar tu video para impulsar el algoritmo.</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: Monetización Inteligente y Alianzas",
            "lessons": [
                {
                    "title": "Canales de Ingreso: Configuración y Venta Estratégica",
                    "objective": "Configurar y activar los tres canales de monetización más rentables para tu modelo de IA (afiliados, contenido premium y patrocinios) de manera estratégica.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "La creación de la modelo de IA es sumamente creativa, pero aquí es donde separamos a los aficionados de los profesionales: en la monetización. Una influencer virtual no es solo un portafolio de imágenes atractivas, es un activo digital diseñado para generar ingresos recurrentes.",
                                "La gran ventaja de este modelo es que no necesitas un millón de seguidores para empezar a facturar. Con una audiencia pequeña pero altamente segmentada y los canales de venta correctos, puedes ver tus primeros ingresos desde las primeras semanas tras el lanzamiento."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "La monetización de una modelo de IA se divide en tres pilares de alta conversión que puedes activar progresivamente a medida que creces:",
                                "1. Marketing de Afiliados Estético: Consiste en recomendar productos de moda, belleza o tecnología que tu modelo «usa» en sus publicaciones. A través de plataformas como Amazon Afiliados o LTK, colocas enlaces personalizados en su biografía. Cuando los seguidores compran el artículo que vieron en la foto, tú te llevas una comisión directa.",
                                "2. Contenido Premium (Suscripciones): Plataformas como Fanvue o Patreon te permiten ofrecer material exclusivo bajo un muro de pago mensual. Fanvue es amigable con modelos de IA, permitiendo monetizar imágenes temáticas premium o incluso habilitar chats privados automatizados.",
                                "3. Patrocinios de Marcas: A las empresas les encantan las influencers de IA por el control absoluto del contenido. Puedes ofrecer publicaciones patrocinadas donde tu modelo interactúe digitalmente con el producto de la marca. Lo ideal es comenzar contactando a marcas pequeñas o locales de tu nicho ofreciendo tarifas accesibles para armar tu portafolio."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina que tu modelo se enfoca en el estilo de vida deportivo. Para activar sus ingresos, diseñas una publicación donde aparece saliendo de un gimnasio sosteniendo un termo de diseño y vistiendo un outfit deportivo.",
                                "En el pie de foto, tu modelo escribe: 'Muchos me preguntaron por mensaje directo de dónde es este conjunto deportivo que usé hoy. Es comodísimo y tiene descuento con el link de mi biografía'. El enlace dirige directamente a Amazon con tu código de afiliado. Si la publicación recibe visitas y el 1% de la audiencia compra el conjunto, generas ingresos estables sin haber manejado inventario ni stock físico."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más grave es intentar vender de forma agresiva desde el primer día. Si tu feed parece un catálogo lleno de enlaces de afiliado y spam sin aportar valor estético, la gente se irá. La regla de oro es: 80% contenido de entretenimiento y estilo de vida, y 20% contenido de venta o recomendación.",
                                "Otro fallo clásico es no ser transparente con el origen de la modelo o los enlaces. La honestidad con tu audiencia consolida la confianza digital y fomenta la conversión de compras a largo plazo.",
                                "Finalmente, evita la saturación de canales. No intentes abrir una tienda, un Patreon, tres redes de afiliados y un canal de YouTube al mismo tiempo. Domina un solo canal de monetización, hazlo rentable y luego expande tu ecosistema financiero."
                            ]
                        },
                        {
                            "heading": "Resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: monetizar una modelo de IA consiste en posicionar el producto correcto frente a la audiencia adecuada de forma sutil. Al conectar la imagen aspiracional de tu influencer virtual con enlaces directos o suscripciones de contenido premium, conviertes la atención en ingresos netos.",
                                "Tu acción recomendada: Regístrate gratis en Beacons.ai o Linktree y personalízalo con los colores de tu modelo. Únete al programa de Amazon Afiliados de tu país, selecciona tres productos estéticos que encajen con tu nicho (un termo, unos lentes de sol o un accesorio) y colócalos hoy mismo en tu enlace de biografía."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz corto: Máquina de Facturar",
                        "questions": [
                            {
                                "question": "¿Cuál es la \"regla de oro\" para balancear el contenido y evitar perder el interés de tu audiencia con ventas agresivas?",
                                "options": [
                                    "Publicar un 50% de estilo de vida y un 50% de enlaces de afiliado.",
                                    "Mantener un 80% de contenido de entretenimiento y estilo de vida, y un 20% de venta o recomendación.",
                                    "Dedicar el 100% del feed a catálogos de venta para maximizar clics.",
                                    "Compartir un 90% de promociones y solo un 10% de historias de la modelo."
                                ],
                                "answer": 1,
                                "explanation": "La lección enseña que vender agresivamente espanta al público. Para mantener una comunidad interesada y activa, la regla de oro es mantener un balance de 80% entretenimiento/estilo de vida y un 20% de venta."
                            },
                            {
                                "question": "¿Cuáles son los tres pilares de monetización recomendados para activar en el modelo de tu influencer virtual?",
                                "options": [
                                    "Marketing de afiliados estético, contenido premium (suscripciones) y patrocinios de marcas.",
                                    "Minería de criptomonedas, venta de NFTs y consultoría de marca.",
                                    "Publicidad de banners, monetización de YouTube y tiendas físicas.",
                                    "E-commerce de productos propios, cursos grabados y eventos presenciales."
                                ],
                                "answer": 0,
                                "explanation": "El modelo se basa en activar de forma progresiva el marketing de afiliados (enlaces de productos que usa), contenido premium bajo muros de pago (suscripciones) y colaboraciones o patrocinios con marcas de nicho."
                            },
                            {
                                "question": "Para no saturar tu negocio desde el inicio, ¿qué error clásico debes evitar al configurar tus canales?",
                                "options": [
                                    "Utilizar plataformas de enlaces múltiples como Beacons o Linktree.",
                                    "Ser transparente y honesto con tu audiencia sobre los enlaces de afiliado.",
                                    "Intentar abrir y gestionar demasiados canales de monetización al mismo tiempo en lugar de dominar uno primero.",
                                    "Contactar a marcas pequeñas para armar tu portafolio de colaboraciones."
                                ],
                                "answer": 2,
                                "explanation": "Intentar abrir una tienda online, Patreon, afiliados y YouTube todo a la vez genera saturación. La lección recomienda dominar primero un solo canal de monetización, hacerlo rentable y luego expandirse."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Diseña el Embudo de Monetización para tu Modelo de IA",
                        "type": "Text",
                        "question": "<p>¡Es momento de activar los canales de ingreso de tu avatar! Diseñarás la estructura de monetización de tu influencer virtual para asegurar un propósito comercial claro desde el primer día.</p><p>Copia la siguiente plantilla y completa cada sección en el cuadro de texto:</p><ol><li><strong>Identidad y Nicho:</strong> Nombre de tu modelo de IA y su nicho de mercado.</li><li><strong>Selección de Productos (Afiliados):</strong> Nombra 3 productos estéticos coherentes con su estilo que colocarás en su biografía.</li><li><strong>Publicación con Regla 80/20:</strong> Redacta un caption para una publicación donde muestres a tu modelo recomendando uno de los productos de forma sutil.</li><li><strong>Oferta Premium (Suscripción):</strong> Describe brevemente qué tipo de contenido de valor o experiencia exclusiva ofrecerías en una plataforma como Patreon o Fanvue.</li><li><strong>Mensaje para Marcas (Pitch):</strong> Redacta una propuesta de 4 líneas para enviar a marcas locales sugiriendo una colaboración con tu modelo de IA.</li></ol>"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto final: Lanzamiento y Plan de Monetización de tu Influencer de IA",
        "type": "Document",
        "question": "<p>¡Ha llegado el momento de consolidar lo aprendido y estructurar el dossier de lanzamiento de tu propia influencer virtual! Este proyecto integrará cada elemento estratégico y técnico para dejar tu activo listo para operar de manera profesional y 100% anónima.</p><p><strong>Instrucciones para el proyecto:</strong></p><p>Copia el siguiente formato, completa cada uno de los bloques y envíalo en el cuadro de texto para tu evaluación final:</p><h3>BLOQUE 1: Ficha de Identidad y ADN de la Modelo</h3><ul><li><strong>Nombre y Edad de tu Influencer:</strong> [Ej: Isabella Rossi, 23 años]</li><li><strong>Nicho de Mercado y Ciudad Base:</strong> [Ej: Estilo de vida saludable y moda sustentable en Barcelona]</li><li><strong>Propósito y Storytelling:</strong> [Escribe de 3 a 5 líneas sobre por qué su público objetivo querrá seguirla. ¿Cuál es su rutina y qué valores defiende?]</li></ul><h3>BLOQUE 2: Lookbook de Consistencia Facial (Prompts de Oro)</h3><p>Redacta 2 prompts de alto rendimiento aplicando la estructura de 5 pasos aprendida (Sujeto, Acción, Outfit, Entorno, Cámara/Luz):</p><ul><li><strong>Prompt 1 (Foto Casual/Estilo de vida):</strong> [Describe a tu modelo en una situación cotidiana]</li><li><strong>Prompt 2 (Foto Profesional/Sesión de fotos):</strong> [Mantén la misma descripción física pero llévala a un set de estudio o locación minimalista]</li><li><strong>Herramienta seleccionada:</strong> [Especifica la herramienta de IA (Fooocus, Midjourney, SeaArt, etc.) y la técnica de consistencia que utilizarás]</li></ul><h3>BLOQUE 3: Reel Viral de Retención Infinita</h3><p>Diseña la estructura de tu primer video corto de alto impacto para crecer de forma orgánica:</p><ul><li><strong>Gancho en pantalla (Hook):</strong> [Frase exacta de los primeros 2 segundos]</li><li><strong>Descripción (Caption) de Bucle:</strong> [Texto de valor de 4 o 5 líneas para mantener al usuario leyendo mientras el video corre de fondo]</li><li><strong>Llamada a la Acción (CTA):</strong> [La frase diseñada para incentivar comentarios o guardados]</li></ul><h3>BLOQUE 4: El Plan de Facturación</h3><p>Establece tus canales de ingresos iniciales:</p><ul><li><strong>Marketing de Afiliados:</strong> [Nombra 2 productos específicos y estéticos que enlazarás en tu biografía]</li><li><strong>Canal Premium:</strong> [Describe brevemente el contenido de suscripción que ofrecerás a tus seguidores exclusivos]</li><li><strong>Mensaje para Colaboraciones:</strong> [Escribe un pitch directo de 3 líneas para proponer colaboraciones a marcas de tu nicho]</li></ul>"
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
