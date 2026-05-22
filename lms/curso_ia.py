# -*- coding: utf-8 -*-
"""
Crea un curso completo en Frappe Learning/LMS con:
- 1 categoría
- 1 curso publicado
- 5 capítulos
- 10 lecciones
- 10 asignaciones
- 5 quizzes con preguntas de opción múltiple
- contenido moderno en Course Lesson.content usando formato EditorJS JSON

Uso recomendado desde frappe-bench:
    python apps/lms/setup_course_ia_negocios_avanzado.py studybadge.localhost

También puedes cambiar el site:
    python apps/lms/setup_course_ia_negocios_avanzado.py nombre_de_tu_site

Notas:
- Está hecho para ser idempotente: si lo ejecutas de nuevo, actualiza el contenido y evita duplicar capítulos/lecciones/tareas/quizzes.
- Usa bloques "quiz" y "assignment" dentro de Course Lesson.content para que se rendericen en la interfaz moderna.
"""

import os
import sys
import json
import time
import traceback

# Evita que el directorio del script haga shadowing de imports cuando se ejecuta directo.
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)
apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

import frappe


INSTRUCTOR_NAME = "Administrator"

COURSE_DATA = {'card_gradient': 'Blue',
 'category': 'Tecnología y Negocios',
 'chapters': [{'lessons': [{'assignment': {'question': '<p>Elige un negocio real o ficticio. Escribe entre 180 y 250 '
                                                       'palabras explicando:</p><ul><li>Qué tareas repetitivas tiene '
                                                       'ese negocio.</li><li>Cuáles de esas tareas podría apoyar la '
                                                       'IA.</li><li>Qué tareas NO debería hacer la IA sin supervisión '
                                                       'humana.</li></ul><p>Cierra con una conclusión breve sobre cómo '
                                                       'usarías IA sin perder control del negocio.</p>',
                                           'title': 'Actividad 1: Diagnóstico de uso de IA en un negocio',
                                           'type': 'Text'},
                            'preview': True,
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'En esta primera lección vas a entender la diferencia entre usar IA '
                                                  'como juguete y usarla como herramienta de negocio. La IA puede '
                                                  'ayudarte a escribir, ordenar ideas, resumir información, crear '
                                                  'borradores, analizar opciones y preparar respuestas. Pero no '
                                                  'reemplaza tu criterio. Si le das poca información, normalmente '
                                                  'devuelve respuestas genéricas. Si le das buen contexto, puede '
                                                  'convertirse en un asistente muy potente.'},
                                         {'heading': 'La idea principal',
                                          'text': 'Un error común es pensar que la IA “hace todo”. En realidad, la IA '
                                                  'trabaja mejor cuando tú defines el objetivo. Por ejemplo, no es lo '
                                                  'mismo pedir: “dame ideas de negocio” que pedir: “tengo 18 años, '
                                                  'vivo en Perú, tengo S/ 800 de capital, sé hacer páginas web y '
                                                  'quiero vender a negocios pequeños; dame 10 ideas realistas con '
                                                  'costos, dificultad y primer paso”. La segunda instrucción tiene '
                                                  'contexto y permite una respuesta mucho más útil.'},
                                         {'heading': 'Cómo se aplica a un negocio real',
                                          'text': 'Imagina una cafetería pequeña. La IA no puede atender físicamente, '
                                                  'preparar café ni cerrar la caja. Pero sí puede redactar respuestas '
                                                  'para clientes, crear promociones semanales, analizar comentarios, '
                                                  'proponer combos, organizar publicaciones, resumir ventas por día y '
                                                  'preparar una lista de tareas. La ventaja está en reducir trabajo '
                                                  'repetitivo y mejorar la velocidad con la que pruebas ideas.'},
                                         {'heading': 'Errores que debes evitar',
                                          'text': 'No tomes cada respuesta como verdad absoluta. La IA puede inventar '
                                                  'datos, simplificar demasiado o sonar convincente aunque esté '
                                                  'equivocada. Por eso, cuando uses IA para precios, temas legales, '
                                                  'salud, pagos, impuestos o decisiones importantes, verifica con una '
                                                  'fuente confiable. La regla práctica es: úsala para producir '
                                                  'borradores y ordenar pensamiento; no para delegar decisiones '
                                                  'críticas sin revisar.'}],
                            'title': '1. Qué puede y qué no puede hacer la IA en un negocio'},
                           {'assignment': {'question': '<p>Sube un documento con un prompt maestro para un negocio '
                                                       'real o ficticio. Debe incluir:</p><ul><li>Rol que tendrá la '
                                                       'IA.</li><li>Contexto del negocio.</li><li>Tarea '
                                                       'concreta.</li><li>Restricciones de tono, extensión o '
                                                       'público.</li><li>Formato de salida esperado.</li></ul><p>Luego '
                                                       'agrega una breve explicación de por qué cada parte del prompt '
                                                       'mejora la respuesta.</p>',
                                           'title': 'Actividad 2: Construye tu prompt maestro',
                                           'type': 'Document'},
                            'quiz': {'passing_percentage': 80,
                                     'questions': [{'answer': 1,
                                                    'explanation': 'Un buen prompt guía a la IA con contexto, tarea, '
                                                                   'restricciones y formato.',
                                                    'options': ['Decorar la conversación con la IA',
                                                                'Dar contexto e instrucciones claras para obtener una '
                                                                'respuesta útil',
                                                                'Evitar que la IA responda',
                                                                'Convertir cualquier respuesta en una verdad absoluta'],
                                                    'question': '¿Cuál es la función principal de un prompt bien '
                                                                'escrito?'},
                                                   {'answer': 0,
                                                    'explanation': 'El rol define desde qué perspectiva debe responder '
                                                                   'la IA.',
                                                    'options': ['El rol',
                                                                'El color de la pantalla',
                                                                'La hora del día',
                                                                'El nombre del archivo'],
                                                    'question': '¿Qué elemento ayuda a que la IA responda desde una '
                                                                'perspectiva específica?'},
                                                   {'answer': 2,
                                                    'explanation': 'La IA es muy útil para borradores, pero las '
                                                                   'decisiones importantes deben revisarse.',
                                                    'options': ['Aceptar cualquier dato sin revisar',
                                                                'Usarla para borrar toda supervisión humana',
                                                                'Usarla para crear borradores y luego verificar lo '
                                                                'importante',
                                                                'Usarla solo para tareas imposibles'],
                                                    'question': '¿Cuál es un uso responsable de IA en un negocio?'},
                                                   {'answer': 1,
                                                    'explanation': 'Sin contexto suficiente, la IA tiende a responder '
                                                                   'con ideas generales.',
                                                    'options': ['La IA deja de funcionar',
                                                                'La respuesta suele ser genérica y poco aplicable',
                                                                'La respuesta siempre será ilegal',
                                                                'El curso se elimina'],
                                                    'question': '¿Qué problema aparece cuando das un prompt demasiado '
                                                                'general?'},
                                                   {'answer': 2,
                                                    'explanation': 'Pedir supuestos ayuda a identificar vacíos o '
                                                                   'riesgos en la respuesta.',
                                                    'options': ['Responde sin explicar nada',
                                                                'No me hagas preguntas',
                                                                'Al final, dime qué supuestos estás haciendo',
                                                                'Solo dame una palabra'],
                                                    'question': '¿Qué frase ayuda a detectar supuestos de la IA?'}],
                                     'title': 'Quiz 1: Fundamentos y prompts'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Un prompt es la instrucción que le das a la IA. La calidad del '
                                                  'prompt define gran parte de la calidad de la respuesta. En '
                                                  'negocios, un buen prompt no solo pide algo; también explica el '
                                                  'contexto, el público, el objetivo, el tono y el formato esperado. '
                                                  'Mientras más claro seas, menos tendrás que corregir después.'},
                                         {'heading': 'La fórmula simple',
                                          'text': 'Usa esta estructura: rol, contexto, tarea, restricciones y formato. '
                                                  'Por ejemplo: “Actúa como asesor de marketing para pequeños '
                                                  'negocios. Tengo una tienda de ropa urbana en Lima y quiero atraer '
                                                  'clientes de 18 a 25 años. Crea 5 ideas de publicaciones para '
                                                  'Instagram. Usa un tono natural, no exagerado, y entrégalo en una '
                                                  'tabla con idea, texto sugerido y objetivo de la publicación”.'},
                                         {'heading': 'Por qué funciona',
                                          'text': 'La IA responde mejor cuando sabe desde dónde debe mirar el '
                                                  'problema. El rol le da enfoque; el contexto evita respuestas '
                                                  'genéricas; la tarea aclara qué debe producir; las restricciones '
                                                  'reducen errores; y el formato hace que el resultado sea fácil de '
                                                  'usar. Esta estructura sirve para marketing, ventas, estudio, '
                                                  'atención al cliente, análisis de documentos y planificación.'},
                                         {'heading': 'Verificación',
                                          'text': 'Un prompt profesional también debe pedir revisión. Puedes agregar: '
                                                  '“Antes de responder, hazme 3 preguntas si falta información” o “al '
                                                  'final, dime qué supuestos estás haciendo”. Esto ayuda a detectar '
                                                  'cuando la IA está rellenando vacíos. En negocios, los supuestos '
                                                  'importan porque pueden cambiar costos, precios, público objetivo y '
                                                  'viabilidad.'}],
                            'title': '2. Cómo escribir prompts claros y verificables'}],
               'title': 'Módulo 1: Fundamentos de IA útil para negocios'},
              {'lessons': [{'assignment': {'question': '<p>Elige un público objetivo específico y redacta un mapa de '
                                                       'dolores. Incluye:</p><ul><li>Quién es el cliente.</li><li>Qué '
                                                       'problema tiene.</li><li>Qué consecuencias le '
                                                       'genera.</li><li>Qué frases podría decir ese cliente cuando '
                                                       'describe su problema.</li><li>Qué información todavía debes '
                                                       'validar con personas reales.</li></ul>',
                                           'title': 'Actividad 3: Mapa de dolores del cliente',
                                           'type': 'Text'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Antes de vender, necesitas entender qué problema tiene tu cliente. '
                                                  'Muchos negocios fallan porque empiezan por el producto y no por la '
                                                  'necesidad. La IA puede ayudarte a ordenar hipótesis, crear '
                                                  'encuestas, simular conversaciones y convertir respuestas '
                                                  'desordenadas en patrones útiles.'},
                                         {'heading': 'Problema, deseo y urgencia',
                                          'text': 'Un cliente compra cuando siente que algo le duele, le falta o le '
                                                  'conviene mejorar. El problema puede ser práctico, como ahorrar '
                                                  'tiempo; emocional, como verse mejor; o económico, como vender más. '
                                                  'La urgencia aparece cuando el cliente siente que no resolverlo le '
                                                  'cuesta dinero, energía, tranquilidad o reputación.'},
                                         {'heading': 'Cómo usar IA para investigar',
                                          'text': 'Puedes pedirle a la IA que te ayude a crear preguntas para '
                                                  'entrevistas. Por ejemplo: “Tengo una idea de servicio de diseño de '
                                                  'páginas web para barberías. Crea 12 preguntas para descubrir si los '
                                                  'dueños realmente necesitan más reservas, mejor imagen o automatizar '
                                                  'mensajes”. Luego puedes pegar respuestas reales y pedirle que '
                                                  'agrupe dolores, frases repetidas y oportunidades.'},
                                         {'heading': 'Cuidado con imaginar demasiado',
                                          'text': 'La IA puede ayudarte a pensar, pero no reemplaza hablar con '
                                                  'personas reales. Si solo conversas con la IA, puedes terminar '
                                                  'validando una fantasía. La investigación mínima debería incluir '
                                                  'conversaciones, observación de comentarios, revisión de '
                                                  'competidores y pruebas pequeñas.'}],
                            'title': '3. Detectar problemas reales del cliente'},
                           {'assignment': {'question': '<p>Sube un documento con una oferta para un producto o '
                                                       'servicio. Debe contener:</p><ul><li>Nombre de la '
                                                       'oferta.</li><li>Cliente ideal.</li><li>Problema que '
                                                       'resuelve.</li><li>Promesa principal.</li><li>3 beneficios '
                                                       'concretos.</li><li>Una versión corta de máximo 25 '
                                                       'palabras.</li></ul>',
                                           'title': 'Actividad 4: Rediseña una oferta',
                                           'type': 'Document'},
                            'quiz': {'passing_percentage': 80,
                                     'questions': [{'answer': 0,
                                                    'explanation': 'La investigación reduce suposiciones y ayuda a '
                                                                   'crear mensajes más relevantes.',
                                                    'options': ['Porque así puedes hablar de problemas reales y no '
                                                                'solo de lo que imaginas',
                                                                'Porque evita tener que vender',
                                                                'Porque reemplaza el producto',
                                                                'Porque hace innecesario probar la oferta'],
                                                    'question': '¿Por qué conviene investigar al cliente antes de '
                                                                'crear contenido o vender?'},
                                                   {'answer': 2,
                                                    'explanation': 'Es específica: dice qué hace, para quién y en qué '
                                                                   'plazo.',
                                                    'options': ['Soluciones integrales de alto impacto',
                                                                'Te ayudamos con todo',
                                                                'Creamos una página de pedidos por WhatsApp para '
                                                                'restaurantes pequeños en 7 días',
                                                                'Innovación total para clientes modernos'],
                                                    'question': '¿Cuál de estas opciones es una oferta más clara?'},
                                                   {'answer': 1,
                                                    'explanation': 'El beneficio traduce una característica en valor '
                                                                   'para el cliente.',
                                                    'options': ['Una palabra técnica del producto',
                                                                'El resultado o mejora que recibe el cliente',
                                                                'Una sección decorativa',
                                                                'El nombre interno del servicio'],
                                                    'question': '¿Qué es un beneficio?'},
                                                   {'answer': 1,
                                                    'explanation': 'La IA no reemplaza el contacto con clientes '
                                                                   'reales.',
                                                    'options': ['Que la IA no escriba en español',
                                                                'Que termines confirmando una idea sin evidencia real',
                                                                'Que el archivo pese demasiado',
                                                                'Que el cliente compre automáticamente'],
                                                    'question': '¿Qué riesgo existe si solo validas una idea '
                                                                'conversando con IA?'},
                                                   {'answer': 2,
                                                    'explanation': 'La claridad ayuda a que el cliente entienda rápido '
                                                                   'por qué le conviene.',
                                                    'options': ['Ser extensa',
                                                                'Parecer compleja',
                                                                'Ser entendible y mostrar valor',
                                                                'Usar palabras técnicas'],
                                                    'question': '¿Qué debe lograr una oferta en pocos segundos?'}],
                                     'title': 'Quiz 2: Cliente y oferta'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Una oferta no es solo el producto. Es la promesa clara de valor que '
                                                  'el cliente entiende rápido. Una buena oferta responde tres '
                                                  'preguntas: qué me das, qué resultado obtengo y por qué debería '
                                                  'elegirte a ti.'},
                                         {'heading': 'La estructura de una oferta clara',
                                          'text': 'Puedes construir una oferta con esta fórmula: problema específico + '
                                                  'solución concreta + resultado esperado + reducción de riesgo. Por '
                                                  'ejemplo: “Creamos una página web sencilla para restaurantes '
                                                  'pequeños que quieren recibir pedidos por WhatsApp, lista en 7 días, '
                                                  'con textos incluidos y una guía para actualizar precios”. Es mejor '
                                                  'que decir simplemente: “Hacemos páginas web”.'},
                                         {'heading': 'Cómo ayuda la IA',
                                          'text': 'La IA puede generar versiones de una oferta, comparar mensajes y '
                                                  'detectar si una promesa suena confusa. También puede ayudarte a '
                                                  'convertir características en beneficios. Una característica es '
                                                  '“incluye formulario”; un beneficio es “recibes solicitudes sin '
                                                  'perseguir clientes por mensajes”.'},
                                         {'heading': 'Prueba de claridad',
                                          'text': 'Si una persona no entiende tu oferta en menos de 10 segundos, '
                                                  'necesitas simplificar. La claridad vende más que la exageración. '
                                                  'Evita frases vacías como “solución innovadora integral”. Usa '
                                                  'palabras concretas, resultados observables y límites honestos.'}],
                            'title': '4. Diseñar una oferta simple que la gente entienda'}],
               'title': 'Módulo 2: Investigación de clientes y creación de oferta'},
              {'lessons': [{'assignment': {'question': '<p>Escribe 3 textos de venta usando la fórmula PAS para una '
                                                       'oferta concreta. Cada texto debe '
                                                       'tener:</p><ul><li>Problema.</li><li>Agitación o '
                                                       'consecuencia.</li><li>Solución.</li><li>Llamada a la '
                                                       'acción.</li></ul><p>Evita frases exageradas. El tono debe '
                                                       'sonar natural y creíble.</p>',
                                           'title': 'Actividad 5: Tres textos de venta con PAS',
                                           'type': 'Text'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'La IA puede escribir textos de venta, pero si no la guías puede '
                                                  'sonar exagerada, artificial o igual a todos. El objetivo es '
                                                  'aprender a pedir mensajes que suenen naturales, conecten con un '
                                                  'problema real y mantengan credibilidad.'},
                                         {'heading': 'Persuasión simple',
                                          'text': 'Un buen mensaje comercial no necesita gritar. Debe mostrar que '
                                                  'entiendes al cliente, explicar el problema, presentar una solución '
                                                  'y dar un siguiente paso. Una estructura útil es PAS: problema, '
                                                  'agitación y solución. Primero nombras el problema; luego explicas '
                                                  'por qué importa; finalmente presentas tu oferta como salida.'},
                                         {'heading': 'Ejemplo práctico',
                                          'text': 'Para un servicio de gestión de WhatsApp para negocios: “¿Pierdes '
                                                  'ventas porque respondes tarde? Cuando un cliente espera demasiado, '
                                                  'suele escribirle a otro negocio. Te ayudamos a ordenar respuestas '
                                                  'rápidas, preguntas frecuentes y seguimiento para que no pierdas '
                                                  'oportunidades por desorden”. El mensaje es directo, no promete '
                                                  'magia y se entiende.'},
                                         {'heading': 'Cómo pedirle esto a la IA',
                                          'text': 'Pídele varias versiones con límites: “Escribe 5 textos de venta '
                                                  'usando PAS. No uses frases exageradas como ‘revoluciona tu vida’. '
                                                  'Que suene peruano, cercano y profesional. Cada texto debe tener '
                                                  'máximo 70 palabras y cerrar con una llamada a la acción suave”.'}],
                            'title': '5. Crear mensajes persuasivos sin sonar falso'},
                           {'assignment': {'question': '<p>Sube un calendario de contenido de 30 días para un negocio. '
                                                       'Debe incluir:</p><ul><li>Objetivo del mes.</li><li>Público '
                                                       'objetivo.</li><li>12 ideas de publicaciones.</li><li>Categoría '
                                                       'de cada publicación: educación, prueba social, detrás de '
                                                       'cámaras, oferta u objeciones.</li><li>Una métrica que '
                                                       'revisarás para saber si funciona.</li></ul>',
                                           'title': 'Actividad 6: Calendario de contenido de 30 días',
                                           'type': 'Document'},
                            'quiz': {'passing_percentage': 80,
                                     'questions': [{'answer': 1,
                                                    'explanation': 'PAS organiza un mensaje persuasivo en problema, '
                                                                   'agitación y solución.',
                                                    'options': ['Precio, anuncio y servicio',
                                                                'Problema, agitación y solución',
                                                                'Producto, audiencia y sistema',
                                                                'Plan, acción y seguimiento'],
                                                    'question': '¿Qué significa la fórmula PAS?'},
                                                   {'answer': 2,
                                                    'explanation': 'Las promesas exageradas reducen credibilidad.',
                                                    'options': ['Usa ejemplos concretos',
                                                                'Explica un problema real',
                                                                'Promete resultados mágicos o exagerados',
                                                                'Tiene una llamada a la acción clara'],
                                                    'question': '¿Cuál es una señal de que un texto de venta puede '
                                                                'sonar falso?'},
                                                   {'answer': 0,
                                                    'explanation': 'Responder objeciones ayuda al cliente a decidir '
                                                                   'con más confianza.',
                                                    'options': ['Para responder dudas que frenan la compra',
                                                                'Para ocultar el precio siempre',
                                                                'Para eliminar la necesidad de vender',
                                                                'Para copiar competidores'],
                                                    'question': '¿Para qué sirve el contenido de objeciones?'},
                                                   {'answer': 0,
                                                    'explanation': 'Sin objetivo ni métrica, no sabes si el contenido '
                                                                   'ayuda al negocio.',
                                                    'options': ['Un objetivo y una métrica de revisión',
                                                                'Solo frases bonitas',
                                                                'Solo imágenes',
                                                                'Únicamente hashtags'],
                                                    'question': '¿Qué debe tener un plan de contenidos además de '
                                                                'ideas?'},
                                                   {'answer': 0,
                                                    'explanation': 'La voz real del cliente hace que el contenido sea '
                                                                   'más específico y creíble.',
                                                    'options': ['Frases reales de clientes y preguntas frecuentes',
                                                                'Solo emojis',
                                                                'El color favorito del dueño',
                                                                'Publicar sin revisar'],
                                                    'question': '¿Qué información suele mejorar mucho los contenidos '
                                                                'creados con IA?'}],
                                     'title': 'Quiz 3: Marketing y contenido'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Publicar por publicar no es una estrategia. Un plan de contenidos '
                                                  'debe cumplir objetivos: atraer personas nuevas, educar, generar '
                                                  'confianza, mostrar resultados y convertir interesados en clientes. '
                                                  'La IA ayuda a ordenar ideas y convertirlas en un calendario '
                                                  'aplicable.'},
                                         {'heading': 'Tipos de contenido',
                                          'text': 'Para un negocio pequeño, puedes trabajar cinco categorías: '
                                                  'educación, prueba social, detrás de cámaras, oferta y objeciones. '
                                                  'Educación enseña algo útil; prueba social muestra casos o '
                                                  'testimonios; detrás de cámaras humaniza; oferta presenta el '
                                                  'producto; objeciones responde dudas que frenan la compra.'},
                                         {'heading': 'Cómo usar IA sin copiar contenido genérico',
                                          'text': 'Primero define tu público, oferta y objetivo mensual. Luego pide a '
                                                  'la IA ideas por categoría. Después ajusta con tu experiencia real. '
                                                  'La IA puede darte estructura, pero los mejores detalles salen de '
                                                  'tus clientes: preguntas frecuentes, comentarios, frases que repiten '
                                                  'y problemas específicos.'},
                                         {'heading': 'Calendario mínimo',
                                          'text': 'No necesitas publicar 5 veces al día. Puedes empezar con 3 '
                                                  'publicaciones semanales y 3 historias simples. Lo importante es '
                                                  'mantener consistencia, medir qué temas generan mensajes y mejorar '
                                                  'con base en señales reales.'}],
                            'title': '6. Crear un plan de contenidos para 30 días'}],
               'title': 'Módulo 3: Marketing y contenido con IA'},
              {'lessons': [{'assignment': {'question': '<p>Crea un banco con 8 respuestas para clientes. '
                                                       'Incluye:</p><ul><li>2 respuestas sobre precio.</li><li>2 sobre '
                                                       'confianza o garantía.</li><li>2 sobre tiempos de '
                                                       'entrega.</li><li>2 para cerrar con una llamada a la acción '
                                                       'suave.</li></ul><p>Las respuestas deben sonar humanas, cortas '
                                                       'y útiles.</p>',
                                           'title': 'Actividad 7: Banco de respuestas para clientes',
                                           'type': 'Text'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Una venta muchas veces no se pierde por el producto, sino por la '
                                                  'conversación. Responder tarde, sonar frío o no saber manejar dudas '
                                                  'puede hacer que un cliente interesado se vaya. La IA puede ayudarte '
                                                  'a preparar respuestas claras y humanas.'},
                                         {'heading': 'Objeciones comunes',
                                          'text': 'Las objeciones no siempre son rechazo. A veces son señales de '
                                                  'interés con duda. Las más comunes son precio, confianza, tiempo, '
                                                  'comparación con otra opción y miedo a equivocarse. La respuesta '
                                                  'correcta no debe presionar; debe aclarar, reducir riesgo y guiar el '
                                                  'siguiente paso.'},
                                         {'heading': 'Sistema de respuestas',
                                          'text': 'Puedes crear una biblioteca de respuestas para preguntas '
                                                  'frecuentes: precio, horarios, garantía, formas de pago, tiempos de '
                                                  'entrega y beneficios. Luego la IA puede ayudarte a adaptar cada '
                                                  'respuesta al tono del cliente. La clave es mantener un lenguaje '
                                                  'natural, breve y orientado a resolver.'},
                                         {'heading': 'Ejemplo',
                                          'text': 'Si un cliente dice “está caro”, una mala respuesta sería discutir. '
                                                  'Una mejor respuesta sería: “Te entiendo. La diferencia está en que '
                                                  'incluimos diagnóstico, configuración y una guía para que puedas '
                                                  'usarlo sin depender de nosotros. Si quieres, te puedo pasar una '
                                                  'opción más simple para empezar con menor presupuesto”.'}],
                            'title': '7. Responder clientes y manejar objeciones'},
                           {'assignment': {'question': '<p>Sube un documento con el mapa de un proceso de negocio. '
                                                       'Debe incluir:</p><ul><li>Entrada del proceso.</li><li>Pasos '
                                                       'actuales.</li><li>Salida esperada.</li><li>3 tareas '
                                                       'repetitivas.</li><li>2 errores posibles.</li><li>Una propuesta '
                                                       'de automatización simple usando plantillas, formularios o '
                                                       'IA.</li></ul>',
                                           'title': 'Actividad 8: Mapa de automatización simple',
                                           'type': 'Document'},
                            'quiz': {'passing_percentage': 80,
                                     'questions': [{'answer': 1,
                                                    'explanation': 'Una objeción suele ser una duda que necesita '
                                                                   'respuesta clara.',
                                                    'options': ['Siempre una pérdida definitiva',
                                                                'Una duda o freno que puede aclararse',
                                                                'Una señal de que el negocio debe cerrar',
                                                                'Un problema técnico sin solución'],
                                                    'question': '¿Qué representa una objeción en ventas?'},
                                                   {'answer': 2,
                                                    'explanation': 'La respuesta debe aclarar valor y reducir '
                                                                   'fricción, no presionar.',
                                                    'options': ['Discutir con el cliente',
                                                                'Ignorar el mensaje',
                                                                'Explicar el valor y ofrecer una alternativa si aplica',
                                                                'Cambiar de tema'],
                                                    'question': '¿Cuál es una buena práctica al responder “está '
                                                                'caro”?'},
                                                   {'answer': 0,
                                                    'explanation': 'Mapear entrada, pasos y salida permite ordenar el '
                                                                   'flujo.',
                                                    'options': ['Entrada, pasos y salida',
                                                                'Logo, color y nombre',
                                                                'Precio, descuento y suerte',
                                                                'Idea, emoción y música'],
                                                    'question': '¿Qué elementos básicos tiene un proceso?'},
                                                   {'answer': 0,
                                                    'explanation': 'Las plantillas reducen trabajo repetitivo y '
                                                                   'errores.',
                                                    'options': ['Tener una plantilla de cotización reutilizable',
                                                                'Responder todo desde cero siempre',
                                                                'No registrar pedidos',
                                                                'Cambiar de negocio cada semana'],
                                                    'question': '¿Cuál es un ejemplo de automatización simple?'},
                                                   {'answer': 0,
                                                    'explanation': 'Sin mapa del proceso, es difícil saber qué '
                                                                   'conviene mejorar.',
                                                    'options': ['Porque permite detectar pasos repetitivos y puntos de '
                                                                'error',
                                                                'Porque hace más lento el negocio',
                                                                'Porque evita vender',
                                                                'Porque reemplaza al cliente'],
                                                    'question': '¿Por qué conviene escribir un flujo antes de '
                                                                'automatizar?'}],
                                     'title': 'Quiz 4: Ventas y automatización'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Automatizar no significa crear un sistema enorme. En un negocio '
                                                  'pequeño, automatizar puede ser tan simple como tener plantillas, '
                                                  'checklist, formularios, respuestas guardadas y un flujo claro. La '
                                                  'IA ayuda a diseñar esos pasos y detectar dónde se pierde tiempo.'},
                                         {'heading': 'Mapa de proceso',
                                          'text': 'Todo proceso tiene entrada, pasos y salida. Por ejemplo, en '
                                                  'atención de pedidos: entra un mensaje del cliente, se confirma '
                                                  'producto, se calcula precio, se registra pago, se coordina entrega '
                                                  'y se hace seguimiento. Si ese flujo está desordenado, aparecen '
                                                  'errores. Si lo escribes, puedes mejorarlo.'},
                                         {'heading': 'Qué puede automatizarse',
                                          'text': 'Puedes automatizar recordatorios, respuestas iniciales, formularios '
                                                  'de pedido, plantillas de cotización, resúmenes diarios y checklists '
                                                  'de entrega. No necesitas empezar con herramientas complejas. A '
                                                  'veces un Google Form, una hoja de cálculo y textos preparados ya '
                                                  'reducen bastante carga.'},
                                         {'heading': 'Cómo pedir ayuda a la IA',
                                          'text': 'Un prompt útil sería: “Analiza este proceso de atención por '
                                                  'WhatsApp. Detecta tareas repetitivas, posibles errores y crea un '
                                                  'flujo de 6 pasos con plantillas de mensaje”. La IA puede darte un '
                                                  'borrador de proceso que luego adaptas a tu realidad.'}],
                            'title': '8. Automatizar procesos simples sin programar'}],
               'title': 'Módulo 4: Ventas, atención y automatización simple'},
              {'lessons': [{'assignment': {'question': '<p>Sube un documento o tabla con un tablero mínimo para un '
                                                       'negocio. Debe incluir:</p><ul><li>5 métricas '
                                                       'básicas.</li><li>Qué significa cada métrica.</li><li>Cómo se '
                                                       'registrará.</li><li>Qué decisión podrías tomar si esa métrica '
                                                       'sube o baja.</li></ul><p>Agrega una breve explicación de cuál '
                                                       'métrica revisarías primero y por qué.</p>',
                                           'title': 'Actividad 9: Tablero mínimo de métricas',
                                           'type': 'Document'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'Un negocio no mejora solo por trabajar más. Mejora cuando mide lo '
                                                  'correcto y toma decisiones con información. La IA puede ayudarte a '
                                                  'interpretar datos simples, crear resúmenes y sugerir preguntas para '
                                                  'revisar resultados.'},
                                         {'heading': 'Métricas mínimas',
                                          'text': 'No necesitas un dashboard avanzado al inicio. Puedes empezar con '
                                                  'métricas básicas: número de mensajes recibidos, número de '
                                                  'cotizaciones, ventas cerradas, ticket promedio, costo de producto, '
                                                  'margen aproximado y clientes que repiten. Con eso ya puedes '
                                                  'detectar si el problema está en atraer, convertir o retener.'},
                                         {'heading': 'Cómo analizar con IA',
                                          'text': 'Puedes copiar una tabla simple y pedir: “Resume qué pasó esta '
                                                  'semana, detecta el mayor problema y sugiere 3 acciones de mejora”. '
                                                  'La IA puede señalar patrones, pero tú debes revisar si los datos '
                                                  'están completos. Si registras mal, la conclusión también puede '
                                                  'salir mal.'},
                                         {'heading': 'Priorizar',
                                          'text': 'Una regla útil es elegir acciones por impacto y esfuerzo. Si algo '
                                                  'tiene alto impacto y bajo esfuerzo, va primero. Por ejemplo, crear '
                                                  'respuestas rápidas para preguntas frecuentes puede tomar poco '
                                                  'tiempo y mejorar cierres. En cambio, rediseñar toda la marca puede '
                                                  'verse bonito, pero quizá no sea urgente.'}],
                            'title': '9. Medir ventas, costos y prioridades con ayuda de IA'},
                           {'assignment': {'question': '<p>Sube un documento final de 3 a 5 páginas. Debe '
                                                       'incluir:</p><ul><li>Nombre del negocio o idea.</li><li>Cliente '
                                                       'ideal y problema principal.</li><li>Oferta clara.</li><li>3 '
                                                       'textos de venta.</li><li>Calendario resumido de '
                                                       'contenido.</li><li>Banco de respuestas para '
                                                       'clientes.</li><li>Proceso que automatizarías.</li><li>5 '
                                                       'métricas para revisar.</li><li>Prompt maestro final que '
                                                       'usarías con IA.</li></ul><p>El documento debe sonar natural, '
                                                       'ordenado y aplicable. No se evaluará por ser perfecto, sino '
                                                       'por ser claro y útil.</p>',
                                           'title': 'Actividad 10: Entrega del proyecto final',
                                           'type': 'Document'},
                            'quiz': {'passing_percentage': 80,
                                     'questions': [{'answer': 1,
                                                    'explanation': 'El proyecto final integra todo el sistema de '
                                                                   'negocio trabajado en el curso.',
                                                    'options': ['Solo frases de motivación',
                                                                'Cliente, oferta, contenido, ventas, automatización y '
                                                                'métricas',
                                                                'Únicamente un logo',
                                                                'Solo una lista de herramientas'],
                                                    'question': '¿Qué debe unir el proyecto final?'},
                                                   {'answer': 0,
                                                    'explanation': 'Mensajes y ventas cerradas ayudan a revisar '
                                                                   'atracción y conversión.',
                                                    'options': ['Número de mensajes recibidos y ventas cerradas',
                                                                'Color favorito del cliente',
                                                                'Cantidad de emojis usados',
                                                                'Número de archivos en la computadora'],
                                                    'question': '¿Cuál es una métrica básica para revisar ventas?'},
                                                   {'answer': 0,
                                                    'explanation': 'Las respuestas rápidas ahorran tiempo y mejoran '
                                                                   'consistencia.',
                                                    'options': ['Crear respuestas rápidas para preguntas frecuentes',
                                                                'Cambiar todo el negocio cada día',
                                                                'Eliminar todos los precios',
                                                                'No responder mensajes'],
                                                    'question': '¿Qué acción suele tener alto impacto y bajo esfuerzo '
                                                                'en atención al cliente?'},
                                                   {'answer': 1,
                                                    'explanation': 'La IA apoya el proceso, pero el criterio y la '
                                                                   'validación siguen siendo humanos.',
                                                    'options': ['Decidir todo sin revisión',
                                                                'Ser asistente para investigar, redactar, ordenar y '
                                                                'mejorar',
                                                                'Reemplazar toda validación real',
                                                                'Ocultar los problemas'],
                                                    'question': '¿Qué papel debe cumplir la IA en el proyecto final?'},
                                                   {'answer': 1,
                                                    'explanation': 'Un sistema aplicable tiene pasos claros y puede '
                                                                   'usarse en la práctica.',
                                                    'options': ['Que use palabras difíciles',
                                                                'Que una persona pueda ejecutarlo con pasos claros',
                                                                'Que sea lo más largo posible',
                                                                'Que no tenga métricas'],
                                                    'question': '¿Qué significa que el sistema sea aplicable?'}],
                                     'title': 'Quiz 5: Proyecto final y mejora continua'},
                            'sections': [{'heading': 'Objetivo de la lección',
                                          'text': 'En el proyecto final vas a unir todo: cliente, oferta, contenido, '
                                                  'ventas, automatización y métricas. La idea es que termines con un '
                                                  'sistema simple que una persona pueda aplicar en un negocio real sin '
                                                  'perderse.'},
                                         {'heading': 'Qué debe contener el sistema',
                                          'text': 'Tu sistema debe empezar con un cliente específico y un problema '
                                                  'claro. Luego debe presentar una oferta entendible, un plan de '
                                                  'contenido básico, respuestas para clientes, un proceso '
                                                  'automatizable y métricas de revisión. No busques hacerlo perfecto; '
                                                  'busca hacerlo aplicable.'},
                                         {'heading': 'Rol de la IA',
                                          'text': 'La IA debe aparecer como asistente en cada parte: investigación, '
                                                  'redacción, revisión, organización y mejora. Pero el criterio final '
                                                  'debe ser humano. Debes explicar dónde usarías IA, qué revisarías '
                                                  'manualmente y qué información necesitarías validar con clientes '
                                                  'reales.'},
                                         {'heading': 'Resultado esperado',
                                          'text': 'Al terminar, tendrás un documento de trabajo que puede servir como '
                                                  'base para lanzar o mejorar un negocio pequeño. También tendrás una '
                                                  'metodología: entender el problema, crear una oferta clara, '
                                                  'comunicarla, responder dudas, ordenar procesos y medir '
                                                  'resultados.'}],
                            'title': '10. Proyecto final: sistema completo de IA para un negocio'}],
               'title': 'Módulo 5: Métricas, mejora continua y proyecto final'}],
 'course_title': 'IA aplicada para emprendedores: de cero a un sistema de ventas',
 'description': '<p>Este curso está diseñado para personas que quieren usar IA de manera práctica, sin tecnicismos y '
                'sin depender de saber programar. El estudiante aprenderá a convertir una idea de negocio en un '
                'sistema básico de investigación, oferta, contenido, ventas y seguimiento.</p><p>La meta no es usar IA '
                'por moda, sino usarla como una herramienta diaria para pensar mejor, ahorrar tiempo y tomar mejores '
                'decisiones. Cada lección incluye una tarea aplicable y los cuestionarios ayudan a verificar que el '
                'estudiante entendió lo importante.</p>',
 'short_introduction': 'Aprende a usar IA para investigar clientes, crear ofertas, producir contenido, vender mejor, '
                       'atender mensajes y organizar un sistema de trabajo simple para un negocio real.'}


def has_field(doctype, fieldname):
    """Devuelve True si el DocType tiene el campo. Ayuda a soportar pequeñas variaciones entre versiones."""
    try:
        return bool(frappe.get_meta(doctype).has_field(fieldname))
    except Exception:
        return False


def filter_fields(doctype, values):
    """Evita errores por campos que no existan en alguna versión de Frappe LMS."""
    meta = frappe.get_meta(doctype)
    valid = set([df.fieldname for df in meta.fields])
    cleaned = {"doctype": doctype}
    for key, value in values.items():
        if key == "name" or key in valid:
            cleaned[key] = value
    return cleaned


def set_if_has(doc, fieldname, value):
    if has_field(doc.doctype, fieldname):
        doc.set(fieldname, value)


def save_doc(doc):
    doc.flags.ignore_permissions = True
    doc.flags.ignore_mandatory = True
    doc.save(ignore_permissions=True)
    return doc


def insert_doc(doctype, values):
    doc = frappe.get_doc(filter_fields(doctype, values))
    doc.flags.ignore_permissions = True
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    return doc


def upsert_doc(doctype, filters, values):
    """Busca por filtros. Si existe, actualiza. Si no existe, crea."""
    name = frappe.db.exists(doctype, filters)
    if name:
        doc = frappe.get_doc(doctype, name)
        for key, value in filter_fields(doctype, values).items():
            if key != "doctype":
                doc.set(key, value)
        save_doc(doc)
        return doc

    return insert_doc(doctype, values)


def ensure_category(category_name):
    """Crea o recupera LMS Category."""
    filters = {"category": category_name}
    existing = frappe.db.exists("LMS Category", filters)
    if existing:
        return existing

    doc = insert_doc("LMS Category", {"category": category_name})
    return doc.name


def ensure_course(course_data, category_name):
    course_values = {
        "title": course_data["course_title"],
        "short_introduction": course_data["short_introduction"],
        "description": course_data["description"],
        "published": 1,
        "category": category_name,
        "card_gradient": course_data.get("card_gradient", "Blue"),
        "enable_certification": 1,
    }

    course = upsert_doc("LMS Course", {"title": course_data["course_title"]}, course_values)

    # Asegura instructor sin duplicar.
    existing_instructors = [row.instructor for row in course.get("instructors") or [] if getattr(row, "instructor", None)]
    if INSTRUCTOR_NAME not in existing_instructors:
        course.append("instructors", {"instructor": INSTRUCTOR_NAME})
        save_doc(course)

    return course


def ensure_assignment(course_name, assignment):
    values = {
        "title": assignment["title"],
        "type": assignment.get("type", "Text"),
        "question": assignment["question"],
        "course": course_name,
    }

    if values["type"] == "Text":
        values["grade_assignment"] = 1
        values["show_answer"] = 0

    doc = upsert_doc("LMS Assignment", {"title": assignment["title"], "course": course_name}, values)
    return doc.name


def ensure_question(question_data):
    options = question_data["options"]
    answer_index = int(question_data["answer"])
    explanation = question_data.get("explanation", "Respuesta correcta.")

    values = {
        "question": question_data["question"],
        "type": "Choices",
        "multiple": 0,
    }

    for idx in range(4):
        number = idx + 1
        values[f"option_{number}"] = options[idx] if idx < len(options) else ""
        values[f"is_correct_{number}"] = 1 if idx == answer_index else 0
        values[f"explanation_{number}"] = explanation if idx == answer_index else ""

    doc = upsert_doc("LMS Question", {"question": question_data["question"]}, values)
    return doc.name


def ensure_quiz(quiz_data):
    values = {
        "title": quiz_data["title"],
        "passing_percentage": quiz_data.get("passing_percentage", 80),
        "max_attempts": quiz_data.get("max_attempts", 3),
        "show_answers": 1,
        "show_submission_history": 1,
        "shuffle_questions": 0,
        "duration": quiz_data.get("duration", "10"),
    }

    quiz = upsert_doc("LMS Quiz", {"title": quiz_data["title"]}, values)

    quiz.set("questions", [])
    total_marks = 0
    for question_data in quiz_data["questions"]:
        question_name = ensure_question(question_data)
        marks = int(question_data.get("marks", 1))
        total_marks += marks
        quiz.append("questions", {"question": question_name, "marks": marks})

    if has_field("LMS Quiz", "total_marks"):
        quiz.total_marks = total_marks

    save_doc(quiz)
    return quiz.name


def paragraph_block(text):
    return {
        "type": "paragraph",
        "data": {"text": text},
    }


def header_block(text, level=3):
    return {
        "type": "header",
        "data": {"text": text, "level": level},
    }


def make_lesson_content(lesson, assignment_name=None, quiz_name=None):
    blocks = []
    blocks.append(header_block("Bienvenida y objetivo", 2))

    for section in lesson.get("sections", []):
        blocks.append(header_block(section["heading"], 3))
        blocks.append(paragraph_block(section["text"]))

    if assignment_name:
        blocks.append(header_block("Actividad práctica", 3))
        blocks.append(
            paragraph_block(
                "Completa la actividad de esta lección. La idea es que no solo leas, sino que construyas una pieza real de tu sistema de negocio."
            )
        )
        blocks.append({
            "type": "assignment",
            "data": {"assignment": assignment_name},
        })

    if quiz_name:
        blocks.append(header_block("Comprobación rápida", 3))
        blocks.append(
            paragraph_block(
                "Responde el cuestionario para comprobar que entendiste las ideas principales antes de continuar."
            )
        )
        blocks.append({
            "type": "quiz",
            "data": {"quiz": quiz_name},
        })

    return json.dumps({
        "time": int(time.time() * 1000),
        "blocks": blocks,
        "version": "2.29.1",
    }, ensure_ascii=False)


def ensure_chapter(course_name, chapter_title):
    return upsert_doc("Course Chapter", {"title": chapter_title, "course": course_name}, {
        "title": chapter_title,
        "course": course_name,
    })


def ensure_lesson(course_name, chapter_name, lesson, assignment_name=None, quiz_name=None):
    content_json = make_lesson_content(lesson, assignment_name=assignment_name, quiz_name=quiz_name)

    values = {
        "title": lesson["title"],
        "chapter": chapter_name,
        "course": course_name,
        "body": "",
        "content": content_json,
        "include_in_preview": 1 if lesson.get("preview") else 0,
    }

    if quiz_name and has_field("Course Lesson", "quiz_id"):
        values["quiz_id"] = quiz_name

    lesson_doc = upsert_doc("Course Lesson", {"title": lesson["title"], "chapter": chapter_name}, values)
    return lesson_doc.name


def link_quiz_to_lesson(quiz_name, lesson_name, course_name):
    """No es obligatorio para el bloque EditorJS, pero ayuda a que el quiz quede mejor relacionado en algunas vistas."""
    if not quiz_name:
        return

    try:
        quiz = frappe.get_doc("LMS Quiz", quiz_name)
        set_if_has(quiz, "lesson", lesson_name)
        set_if_has(quiz, "course", course_name)
        save_doc(quiz)
    except Exception:
        print(f"Advertencia: no se pudo enlazar el quiz {quiz_name} con la lección {lesson_name}.")
        traceback.print_exc()


def run():
    frappe.set_user("Administrator")
    print("Iniciando creación del curso completo...")

    category_name = ensure_category(COURSE_DATA["category"])
    course = ensure_course(COURSE_DATA, category_name)
    course_name = course.name

    course_chapter_names = []
    total_lessons = 0
    total_assignments = 0
    total_quizzes = 0

    for chapter in COURSE_DATA["chapters"]:
        chapter_doc = ensure_chapter(course_name, chapter["title"])
        chapter_doc.set("lessons", [])

        for lesson in chapter["lessons"]:
            assignment_name = None
            quiz_name = None

            if lesson.get("assignment"):
                assignment_name = ensure_assignment(course_name, lesson["assignment"])
                total_assignments += 1

            if lesson.get("quiz"):
                quiz_name = ensure_quiz(lesson["quiz"])
                total_quizzes += 1

            lesson_name = ensure_lesson(
                course_name=course_name,
                chapter_name=chapter_doc.name,
                lesson=lesson,
                assignment_name=assignment_name,
                quiz_name=quiz_name,
            )
            link_quiz_to_lesson(quiz_name, lesson_name, course_name)

            chapter_doc.append("lessons", {"lesson": lesson_name})
            total_lessons += 1

        save_doc(chapter_doc)
        course_chapter_names.append(chapter_doc.name)

    # Reconstruye la tabla de capítulos del curso para evitar duplicados y mantener el orden.
    course.reload()
    course.set("chapters", [])
    for chapter_name in course_chapter_names:
        course.append("chapters", {"chapter": chapter_name})
    save_doc(course)

    frappe.db.commit()

    print("✅ Curso importado/actualizado correctamente.")
    print(f"Curso: {COURSE_DATA['course_title']}")
    print(f"Capítulos: {len(course_chapter_names)}")
    print(f"Lecciones: {total_lessons}")
    print(f"Asignaciones: {total_assignments}")
    print(f"Quizzes: {total_quizzes}")


if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    frappe.init(site=site)
    frappe.connect()
    try:
        run()
    finally:
        frappe.destroy()
