# -*- coding: utf-8 -*-
"""
Crea un curso completo en Frappe Learning/LMS:
- 1 categoría
- 1 curso publicado
- 10 secciones/capítulos
- 10 lecturas/lecciones largas y claras
- 10 quizzes cortos, uno por lectura
- 10 actividades finales, una por sección
- contenido moderno en Course Lesson.content usando bloques tipo EditorJS

Curso: Vende más con TikTok, Reels y WhatsApp usando IA

Uso desde frappe-bench:
    python apps/lms/setup_course_tiktok_whatsapp_ia.py studybadge.localhost

Notas:
- Script idempotente: si lo vuelves a ejecutar, actualiza en lugar de duplicar.
- Usa bloques "quiz" y "assignment" dentro de Course Lesson.content para renderizar contenido interactivo.
- Usa tipos de asignación válidos en Frappe Learning: Text y Document.
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

COURSE_DATA = {'category': 'Marketing y Ventas con IA',
 'title': 'Vende más con TikTok, Reels y WhatsApp usando IA',
 'short_introduction': 'Aprende a crear contenido corto que atrae clientes, convertir mensajes en ventas y usar IA sin '
                       'sonar robótico.',
 'description': '<p>Este curso está diseñado para emprendedores, creadores, freelancers y negocios pequeños que '
                'quieren vender más usando videos cortos, mensajes directos y WhatsApp. No necesitas ser experto en '
                'edición, marketing ni programación.</p>\n'
                '<p>Vas a aprender a encontrar un nicho, construir una oferta clara, escribir guiones para '
                'TikTok/Reels, organizar un calendario de contenido, responder clientes por WhatsApp y crear un embudo '
                'simple de venta con apoyo de IA.</p>\n'
                '<p>El curso está pensado para que cada sección termine con una actividad práctica. Así, el estudiante '
                'no solo lee: termina con piezas reales que puede usar en su negocio.</p>',
 'card_gradient': 'Purple',
 'chapters': [{'title': 'Sección 1: Elegir un nicho que sí tenga demanda',
               'lesson': {'title': '1. Nicho, cliente ideal y problema urgente',
                          'sections': [{'heading': 'Por qué empezar por el nicho',
                                        'paragraphs': ['Muchos negocios empiezan creando contenido sin saber '
                                                       'exactamente a quién le hablan. Publican frases generales, '
                                                       'promociones sueltas o videos que podrían servir para cualquier '
                                                       'persona. El problema es que, cuando intentas hablarle a todo '
                                                       'el mundo, casi nadie siente que el mensaje fue hecho para él. '
                                                       'Un nicho no limita tu negocio; al contrario, te ayuda a ser '
                                                       'más claro y más recordable.',
                                                       'Un buen nicho combina tres cosas: una persona específica, un '
                                                       'problema real y una razón para actuar pronto. Por ejemplo, no '
                                                       'es lo mismo decir “vendo asesorías de marketing” que decir '
                                                       '“ayudo a barberías de Lima a conseguir más reservas por '
                                                       'WhatsApp usando Reels simples”. La segunda frase es más '
                                                       'concreta, permite crear contenido más directo y hace que el '
                                                       'cliente se reconozca rápido.',
                                                       'La IA puede ayudarte a ordenar ideas de nicho, comparar '
                                                       'públicos y detectar problemas frecuentes. Pero no debe '
                                                       'reemplazar la validación real. Puedes pedirle hipótesis, '
                                                       'preguntas de entrevista y ejemplos de dolores; luego debes '
                                                       'contrastarlo con comentarios, conversaciones, reseñas, grupos, '
                                                       'TikTok, Instagram y clientes reales. La IA te acelera, pero el '
                                                       'mercado confirma.']},
                                       {'heading': 'Cómo detectar si un nicho puede atraer gente',
                                        'paragraphs': ['Un nicho atractivo suele tener señales visibles: personas '
                                                       'haciendo preguntas, negocios pagando soluciones, competidores '
                                                       'vendiendo, comentarios repetidos y contenido parecido '
                                                       'funcionando. Si nadie habla del problema, puede ser que el '
                                                       'mercado aún no lo entienda o que no sea tan urgente. Si hay '
                                                       'demasiados competidores, no significa que sea malo; significa '
                                                       'que hay dinero, pero necesitarás un ángulo distinto.',
                                                       'Para analizar un nicho con IA, puedes usar este prompt: “Actúa '
                                                       'como estratega de negocios digitales. Quiero crear contenido '
                                                       'para vender [producto o servicio]. Analiza 5 posibles nichos, '
                                                       'dime qué problema tiene cada uno, qué tan urgente parece, qué '
                                                       'contenido podría atraerlos y qué oferta inicial sería más '
                                                       'fácil de vender”. Después, toma la mejor opción y vuelve a '
                                                       'pedir ejemplos más específicos.',
                                                       'La meta de esta sección no es encontrar el nicho perfecto para '
                                                       'siempre. La meta es elegir un punto de partida claro. Luego, '
                                                       'con los resultados, podrás ajustar. En marketing digital, la '
                                                       'claridad inicial es mejor que la perfección imaginaria.']}],
                          'quiz': {'title': 'Quiz corto 1: Nicho y cliente ideal',
                                   'questions': [{'question': '¿Por qué es importante elegir un nicho específico?',
                                                  'options': ['Porque evita vender',
                                                              'Porque permite hablarle con claridad a una persona '
                                                              'concreta',
                                                              'Porque elimina la competencia',
                                                              'Porque hace innecesario probar la oferta'],
                                                  'answer': 1,
                                                  'explanation': 'Un nicho claro hace que el mensaje sea más directo y '
                                                                 'fácil de recordar.'},
                                                 {'question': '¿Cuál es una señal de que un nicho puede tener demanda?',
                                                  'options': ['Nadie pregunta nada',
                                                              'Hay comentarios, preguntas y competidores vendiendo '
                                                              'soluciones',
                                                              'Solo le interesa al dueño',
                                                              'No existe ningún contenido relacionado'],
                                                  'answer': 1,
                                                  'explanation': 'La conversación y la competencia suelen indicar '
                                                                 'interés real del mercado.'},
                                                 {'question': '¿Qué papel debe cumplir la IA al elegir un nicho?',
                                                  'options': ['Inventar la verdad final',
                                                              'Ayudar a generar hipótesis y preguntas para validar',
                                                              'Reemplazar a los clientes reales',
                                                              'Decidir precios sin revisar'],
                                                  'answer': 1,
                                                  'explanation': 'La IA sirve para acelerar el análisis, pero el '
                                                                 'mercado debe validar.'}]},
                          'assignment': {'title': 'Actividad final 1: Define tu nicho vendible',
                                         'type': 'Text',
                                         'question': '<p>Elige un producto, servicio o idea de negocio. Escribe una '
                                                     'respuesta de 250 a 350 palabras con:</p><ul><li>Cliente '
                                                     'ideal.</li><li>Problema urgente que tiene.</li><li>Por qué ese '
                                                     'problema le importa ahora.</li><li>3 señales de demanda que '
                                                     'podrías revisar en redes o en conversaciones reales.</li><li>Una '
                                                     'frase de nicho en este formato: “Ayudo a [cliente] a lograr '
                                                     '[resultado] sin [dolor principal]”.</li></ul>'}}},
              {'title': 'Sección 2: Crear una oferta simple que la gente entienda rápido',
               'lesson': {'title': '2. Oferta, promesa y beneficios concretos',
                          'sections': [{'heading': 'La oferta es más que el producto',
                                        'paragraphs': ['Una oferta no es solo lo que vendes. Es la forma en la que '
                                                       'presentas el valor, el resultado esperado, la confianza y el '
                                                       'siguiente paso. Dos negocios pueden vender exactamente lo '
                                                       'mismo, pero uno puede sonar común y el otro puede sonar '
                                                       'urgente, claro y útil. La diferencia está en cómo conecta el '
                                                       'producto con el problema del cliente.',
                                                       'Por ejemplo, “sesión de fotos” es un servicio. Pero “sesión de '
                                                       'fotos para emprendedores que necesitan verse profesionales en '
                                                       'Instagram y WhatsApp en menos de 48 horas” es una oferta más '
                                                       'clara. Le dice al cliente para quién es, qué resultado obtiene '
                                                       'y por qué podría importarle. El cliente no compra solo una '
                                                       'foto; compra percepción, confianza y posibilidad de vender '
                                                       'mejor.',
                                                       'La IA te ayuda a transformar una descripción básica en varias '
                                                       'versiones de oferta. Puedes pedirle que convierta '
                                                       'características en beneficios, que simplifique el lenguaje y '
                                                       'que cree versiones para distintos públicos. Pero siempre debes '
                                                       'revisar que la promesa sea realista. Prometer demasiado puede '
                                                       'atraer clics, pero también puede destruir confianza.']},
                                       {'heading': 'Cómo escribir una promesa fuerte sin exagerar',
                                        'paragraphs': ['Una buena promesa responde tres preguntas: qué cambio obtiene '
                                                       'el cliente, en qué situación se encuentra y qué obstáculo le '
                                                       'vas a quitar. No tiene que sonar agresiva ni falsa. De hecho, '
                                                       'las mejores promesas suelen ser simples: “ordena tus finanzas '
                                                       'personales en una semana”, “crea tus primeros 10 contenidos '
                                                       'sin bloquearte” o “responde clientes por WhatsApp con mensajes '
                                                       'más claros”.',
                                                       'Evita promesas como “hazte millonario en 7 días” o “vende sin '
                                                       'esfuerzo”. Ese tipo de mensaje puede llamar la atención, pero '
                                                       'genera poca confianza y atrae clientes difíciles. Para un '
                                                       'negocio sostenible, es mejor prometer un resultado concreto, '
                                                       'alcanzable y verificable. La claridad vende más que la '
                                                       'exageración cuando el cliente está comparando opciones.',
                                                       'Un prompt útil es: “Convierte esta descripción de producto en '
                                                       '5 ofertas claras. Cada oferta debe incluir cliente ideal, '
                                                       'problema, resultado, beneficio principal y llamada a la '
                                                       'acción. Usa lenguaje natural, sin humo ni promesas '
                                                       'exageradas”.']}],
                          'quiz': {'title': 'Quiz corto 2: Oferta y promesa',
                                   'questions': [{'question': '¿Qué es una oferta en marketing?',
                                                  'options': ['Solo el nombre del producto',
                                                              'La forma en que presentas valor, resultado y siguiente '
                                                              'paso',
                                                              'Un descuento obligatorio',
                                                              'Un logo bonito'],
                                                  'answer': 1,
                                                  'explanation': 'La oferta une producto, valor percibido y acción '
                                                                 'esperada.'},
                                                 {'question': '¿Qué hace que una promesa sea más confiable?',
                                                  'options': ['Exagerar resultados',
                                                              'Ser concreta, realista y verificable',
                                                              'No decir a quién va dirigida',
                                                              'Usar palabras complicadas'],
                                                  'answer': 1,
                                                  'explanation': 'Una promesa concreta genera más confianza que una '
                                                                 'exageración.'},
                                                 {'question': '¿Qué puede hacer la IA con una oferta?',
                                                  'options': ['Transformar características en beneficios',
                                                              'Garantizar ventas automáticamente',
                                                              'Reemplazar el producto',
                                                              'Cobrar al cliente'],
                                                  'answer': 0,
                                                  'explanation': 'La IA ayuda a mejorar el mensaje, pero no garantiza '
                                                                 'resultados por sí sola.'}]},
                          'assignment': {'title': 'Actividad final 2: Diseña tu oferta de entrada',
                                         'type': 'Document',
                                         'question': '<p>Sube un documento con una oferta inicial para tu negocio o '
                                                     'idea. Incluye:</p><ul><li>Nombre de la oferta.</li><li>Cliente '
                                                     'ideal.</li><li>Problema que resuelve.</li><li>Promesa '
                                                     'principal.</li><li>3 beneficios concretos.</li><li>Precio '
                                                     'tentativo o rango.</li><li>Una llamada a la acción para '
                                                     'WhatsApp.</li></ul><p>Debe sentirse clara, natural y '
                                                     'realista.</p>'}}},
              {'title': 'Sección 3: Construir confianza antes de vender',
               'lesson': {'title': '3. Perfil, prueba social y autoridad simple',
                          'sections': [{'heading': 'La confianza se construye antes del mensaje de venta',
                                        'paragraphs': ['En redes, muchas personas no compran la primera vez que te '
                                                       'ven. Primero miran tu perfil, revisan si pareces real, si '
                                                       'entienden qué haces y si hay señales de confianza. Por eso, '
                                                       'antes de hacer muchos videos, conviene ordenar tu perfil. Tu '
                                                       'biografía, foto, publicaciones fijadas, destacados y link de '
                                                       'contacto deben responder rápidamente: quién eres, a quién '
                                                       'ayudas, qué resultado prometes y cómo te pueden escribir.',
                                                       'No necesitas parecer una empresa gigante. De hecho, muchos '
                                                       'negocios pequeños venden más cuando se muestran humanos, '
                                                       'claros y cercanos. Lo importante es que el perfil no genere '
                                                       'dudas básicas. Si alguien ve un Reel tuyo y entra a tu perfil, '
                                                       'debería entender en menos de 10 segundos si tu contenido y tu '
                                                       'oferta son para él.',
                                                       'La prueba social también ayuda: testimonios, capturas de '
                                                       'resultados, antes y después, comentarios de clientes, fotos '
                                                       'del proceso, entregas realizadas o casos simples. Si todavía '
                                                       'no tienes clientes, puedes mostrar ejemplos, prototipos, '
                                                       'prácticas, análisis gratuitos o resultados propios. La '
                                                       'confianza se puede empezar a construir desde el proceso, no '
                                                       'solo desde grandes logros.']},
                                       {'heading': 'Qué poner en un perfil que vende',
                                        'paragraphs': ['Una biografía efectiva suele tener cuatro partes: qué haces, '
                                                       'para quién, qué resultado ayudas a lograr y cómo contactarte. '
                                                       'Ejemplo: “Ayudo a restaurantes pequeños a conseguir más '
                                                       'reservas con Reels y WhatsApp. Ideas simples, contenido real y '
                                                       'mensajes que venden. Escríbeme ‘RESERVAS’ para una evaluación '
                                                       'rápida”. Es directo, específico y accionable.',
                                                       'Tus publicaciones fijadas deberían funcionar como una mini '
                                                       'presentación. Una puede explicar quién eres y qué haces. Otra '
                                                       'puede mostrar un caso, ejemplo o resultado. La tercera puede '
                                                       'responder una duda frecuente o presentar tu oferta. Así, el '
                                                       'perfil no depende de que el usuario vea todo tu contenido; le '
                                                       'das una ruta clara.',
                                                       'Puedes usar IA para revisar tu perfil. Copia tu biografía '
                                                       'actual y pídele: “Evalúa esta bio como si fueras un cliente '
                                                       'nuevo. Dime qué se entiende, qué confunde y dame 5 versiones '
                                                       'más claras para vender sin sonar desesperado”.']}],
                          'quiz': {'title': 'Quiz corto 3: Confianza y perfil',
                                   'questions': [{'question': '¿Qué debería entender alguien al entrar a tu perfil?',
                                                  'options': ['Solo tu nombre',
                                                              'Quién eres, a quién ayudas, qué resultado ofreces y '
                                                              'cómo contactarte',
                                                              'Cuántas apps usas',
                                                              'Tu contraseña'],
                                                  'answer': 1,
                                                  'explanation': 'Un perfil que vende reduce dudas y facilita el '
                                                                 'contacto.'},
                                                 {'question': '¿Qué es prueba social?',
                                                  'options': ['Una señal de que otras personas ya confían o han '
                                                              'obtenido valor',
                                                              'Un examen escolar',
                                                              'Una foto sin contexto',
                                                              'Una promesa sin evidencia'],
                                                  'answer': 0,
                                                  'explanation': 'La prueba social ayuda a reducir desconfianza.'},
                                                 {'question': '¿Qué se puede mostrar si todavía no hay clientes?',
                                                  'options': ['Nada',
                                                              'Ejemplos, prototipos, procesos o resultados propios',
                                                              'Solo memes',
                                                              'Datos inventados'],
                                                  'answer': 1,
                                                  'explanation': 'Puedes construir confianza mostrando proceso y '
                                                                 'ejemplos reales.'}]},
                          'assignment': {'title': 'Actividad final 3: Optimiza tu perfil de venta',
                                         'type': 'Text',
                                         'question': '<p>Escribe la nueva versión de tu perfil para vender mejor. '
                                                     'Incluye:</p><ul><li>Bio de máximo 160 caracteres.</li><li>3 '
                                                     'ideas de publicaciones fijadas.</li><li>3 pruebas de confianza '
                                                     'que podrías mostrar aunque estés empezando.</li><li>Una frase de '
                                                     'llamada a la acción para que te escriban por WhatsApp o '
                                                     'DM.</li></ul>'}}},
              {'title': 'Sección 4: Crear ideas de contenido que atraen clientes',
               'lesson': {'title': '4. Contenido útil, entretenido y vendedor',
                          'sections': [{'heading': 'No todo contenido tiene que vender directamente',
                                        'paragraphs': ['Un error común es publicar solo promociones. Si cada video '
                                                       'dice “compra, compra, compra”, la audiencia se cansa. El '
                                                       'contenido que atrae clientes suele mezclar educación, '
                                                       'identificación, confianza y venta. Primero haces que la '
                                                       'persona piense: “esto me pasa”, “esta persona entiende mi '
                                                       'problema” o “esto me sirve”. Después, la venta se siente más '
                                                       'natural.',
                                                       'Puedes organizar tus ideas en cuatro pilares: problemas del '
                                                       'cliente, errores comunes, soluciones simples y prueba de tu '
                                                       'trabajo. Por ejemplo, si vendes asesorías para negocios, '
                                                       'puedes crear videos sobre errores al responder clientes, '
                                                       'ejemplos de mensajes que venden, antes y después de una oferta '
                                                       'y casos ficticios explicados con claridad.',
                                                       'La IA funciona muy bien como generador de ángulos. En lugar de '
                                                       'pedir “dame ideas para TikTok”, dale más contexto: “mi cliente '
                                                       'ideal es una dueña de tienda de ropa que vende por Instagram, '
                                                       'tiene pocos mensajes y no sabe grabar videos. Dame 30 ideas de '
                                                       'Reels divididas en educación, errores, historias y venta '
                                                       'suave”.']},
                                       {'heading': 'Cómo reconocer una buena idea de video',
                                        'paragraphs': ['Una buena idea de contenido se puede explicar en una frase. Si '
                                                       'necesitas demasiada explicación, probablemente todavía está '
                                                       'confusa. También debe tocar un problema real o una curiosidad '
                                                       'fuerte. Los videos cortos no tienen mucho tiempo para '
                                                       'convencer; por eso, la idea debe sentirse clara desde el '
                                                       'inicio.',
                                                       'Una estructura simple es: situación concreta + tensión + '
                                                       'aprendizaje. Ejemplo: “Si tienes una tienda y nadie te escribe '
                                                       'por Instagram, revisa estos 3 errores”. La situación es la '
                                                       'tienda, la tensión es que nadie escribe y el aprendizaje son '
                                                       'los errores. Este tipo de idea invita a mirar porque promete '
                                                       'claridad rápida.',
                                                       'No busques solo viralidad. Un video con 1,000 vistas de '
                                                       'personas correctas puede ser más valioso que 100,000 vistas de '
                                                       'personas que nunca comprarían. Para negocios pequeños, el '
                                                       'objetivo no es fama vacía; es atraer conversaciones reales.']}],
                          'quiz': {'title': 'Quiz corto 4: Ideas de contenido',
                                   'questions': [{'question': '¿Por qué no conviene publicar solo promociones?',
                                                  'options': ['Porque la audiencia puede cansarse y no construir '
                                                              'confianza',
                                                              'Porque vender está prohibido',
                                                              'Porque los videos no funcionan',
                                                              'Porque la IA no permite promociones'],
                                                  'answer': 0,
                                                  'explanation': 'El contenido debe mezclar valor, confianza y venta.'},
                                                 {'question': '¿Cuál es un pilar útil de contenido?',
                                                  'options': ['Errores comunes del cliente',
                                                              'Contraseñas personales',
                                                              'Datos inventados',
                                                              'Contenido sin tema'],
                                                  'answer': 0,
                                                  'explanation': 'Los errores comunes generan identificación y '
                                                                 'aprendizaje.'},
                                                 {'question': '¿Qué es más importante para un negocio pequeño?',
                                                  'options': ['Solo viralidad',
                                                              'Atraer personas correctas que puedan convertirse en '
                                                              'clientes',
                                                              'Publicar sin estrategia',
                                                              'Cambiar de nicho todos los días'],
                                                  'answer': 1,
                                                  'explanation': 'La calidad del público importa más que la cantidad '
                                                                 'vacía.'}]},
                          'assignment': {'title': 'Actividad final 4: Banco de 20 ideas de contenido',
                                         'type': 'Document',
                                         'question': '<p>Sube un documento con 20 ideas de contenido para tu nicho. '
                                                     'Organízalas en 4 grupos:</p><ul><li>5 ideas sobre problemas del '
                                                     'cliente.</li><li>5 ideas sobre errores comunes.</li><li>5 ideas '
                                                     'educativas o tutoriales.</li><li>5 ideas de confianza o venta '
                                                     'suave.</li></ul><p>Cada idea debe tener título, objetivo y '
                                                     'llamada a la acción.</p>'}}},
              {'title': 'Sección 5: Escribir guiones cortos para TikTok y Reels',
               'lesson': {'title': '5. Hook, desarrollo y llamada a la acción',
                          'sections': [{'heading': 'El guion evita grabar al azar',
                                        'paragraphs': ['Un video corto no necesita parecer una película. Pero sí '
                                                       'necesita intención. El guion te ayuda a no improvisar '
                                                       'demasiado, a mantener el mensaje claro y a terminar con una '
                                                       'acción. La estructura más simple es: hook, desarrollo y '
                                                       'llamada a la acción. El hook captura atención, el desarrollo '
                                                       'entrega valor y la llamada a la acción dice qué hacer después.',
                                                       'El hook debe conectar con una emoción o problema inmediato. '
                                                       'Ejemplos: “Si nadie responde tus historias, puede ser por '
                                                       'esto”, “Tres frases que hacen que un cliente no te compre” o '
                                                       '“Antes de pagar publicidad, arregla esto en tu WhatsApp”. No '
                                                       'se trata de gritar; se trata de mostrar relevancia desde los '
                                                       'primeros segundos.',
                                                       'El desarrollo debe ser corto y concreto. Una idea por video. '
                                                       'Si metes cinco temas, el usuario se pierde. La llamada a la '
                                                       'acción puede ser suave: “guarda este video”, “comenta ‘guía’”, '
                                                       '“escríbeme ‘oferta’ por WhatsApp” o “mira el perfil para ver '
                                                       'el ejemplo completo”.']},
                                       {'heading': 'Cómo pedir guiones a la IA',
                                        'paragraphs': ['La IA puede escribir guiones rápidos, pero debes pedirle '
                                                       'estilo natural. Un prompt útil sería: “Crea 10 guiones para '
                                                       'Reels de 30 segundos para [nicho]. Cada guion debe tener hook, '
                                                       'desarrollo en 3 puntos y CTA. Usa lenguaje peruano neutro, '
                                                       'claro, sin sonar vendedor agresivo”. Mientras más específico '
                                                       'seas, menos genérico será el resultado.',
                                                       'Después de recibir los guiones, no los copies ciegamente. '
                                                       'Léelos en voz alta. Si no suenan como una persona real, '
                                                       'edítalos. Cambia palabras muy formales, reduce frases largas y '
                                                       'agrega ejemplos concretos. La IA da un borrador; tu voz le da '
                                                       'autenticidad.',
                                                       'Un buen guion no siempre busca cerrar una venta inmediata. A '
                                                       'veces busca que la persona te siga, guarde, comente o te '
                                                       'escriba. Cada video debe tener una función dentro del camino '
                                                       'de venta.']}],
                          'quiz': {'title': 'Quiz corto 5: Guiones para videos cortos',
                                   'questions': [{'question': '¿Cuál es una estructura básica de guion para video '
                                                              'corto?',
                                                  'options': ['Hook, desarrollo y llamada a la acción',
                                                              'Saludo largo, historia completa y despedida',
                                                              'Solo música',
                                                              'Título, contraseña y precio'],
                                                  'answer': 0,
                                                  'explanation': 'Esa estructura mantiene atención y guía al usuario.'},
                                                 {'question': '¿Qué debe hacer el hook?',
                                                  'options': ['Capturar atención con un problema o curiosidad '
                                                              'relevante',
                                                              'Explicar toda la empresa',
                                                              'Pedir dinero al inicio',
                                                              'Ser lo más largo posible'],
                                                  'answer': 0,
                                                  'explanation': 'El hook abre el interés en los primeros segundos.'},
                                                 {'question': '¿Qué conviene hacer con un guion generado por IA?',
                                                  'options': ['Copiarlo sin leer',
                                                              'Leerlo en voz alta y adaptarlo a tu voz',
                                                              'Eliminar la CTA',
                                                              'Usarlo aunque suene falso'],
                                                  'answer': 1,
                                                  'explanation': 'La adaptación humana hace que el guion suene '
                                                                 'natural.'}]},
                          'assignment': {'title': 'Actividad final 5: Crea 5 guiones listos para grabar',
                                         'type': 'Document',
                                         'question': '<p>Sube un documento con 5 guiones para TikTok/Reels. Cada guion '
                                                     'debe tener:</p><ul><li>Título del video.</li><li>Hook de máximo '
                                                     '2 líneas.</li><li>Desarrollo en 3 ideas claras.</li><li>Llamada '
                                                     'a la acción.</li><li>Duración estimada.</li></ul><p>El tono debe '
                                                     'sonar natural y fácil de decir en voz alta.</p>'}}},
              {'title': 'Sección 6: Grabar contenido simple con celular',
               'lesson': {'title': '6. Grabación rápida sin equipo profesional',
                          'sections': [{'heading': 'Lo simple funciona si el mensaje es claro',
                                        'paragraphs': ['No necesitas una cámara cara para empezar. Muchos videos que '
                                                       'venden se graban con celular, luz natural y audio entendible. '
                                                       'Lo importante es que el mensaje se vea y se escuche bien. Si '
                                                       'el contenido resuelve una duda real, el usuario tolera una '
                                                       'producción sencilla. Lo que no tolera es un video confuso, '
                                                       'oscuro o con audio imposible de entender.',
                                                       'Busca una fuente de luz frente a ti, no detrás. Limpia la '
                                                       'cámara, usa encuadre vertical y evita fondos demasiado '
                                                       'cargados. Si vas a mostrar un producto, acércalo y enseña '
                                                       'detalles. Si vas a hablar a cámara, mira al lente y usa frases '
                                                       'cortas. Grabar simple no significa grabar descuidado.',
                                                       'También puedes grabar sin mostrar tu cara: manos trabajando, '
                                                       'pantalla, proceso, antes/después, producto en uso, voz en off '
                                                       'o texto en pantalla. Esto ayuda a quienes tienen vergüenza al '
                                                       'inicio. Con práctica, puedes ir apareciendo más.']},
                                       {'heading': 'Plantilla de grabación práctica',
                                        'paragraphs': ['Antes de grabar, prepara tres cosas: idea central, frase '
                                                       'inicial y acción final. No intentes memorizar un texto '
                                                       'gigante. Usa notas pequeñas. Graba varias tomas cortas y elige '
                                                       'la más natural. A veces la toma imperfecta pero clara funciona '
                                                       'mejor que la toma rígida y demasiado ensayada.',
                                                       'La IA puede ayudarte a convertir un guion en lista de tomas. '
                                                       'Por ejemplo: “Convierte este guion en una lista de escenas '
                                                       'para grabar con celular. Indica qué se muestra, qué digo y qué '
                                                       'texto aparece en pantalla”. Esto te evita pensar todo al '
                                                       'momento de grabar.',
                                                       'Recuerda que el objetivo del primer mes no es lograr el video '
                                                       'perfecto. El objetivo es crear ritmo. Publicar, medir, '
                                                       'aprender y mejorar. La consistencia inteligente suele ganar '
                                                       'sobre la perfección lenta.']}],
                          'quiz': {'title': 'Quiz corto 6: Grabación simple',
                                   'questions': [{'question': '¿Qué es más importante al empezar a grabar?',
                                                  'options': ['Tener cámara profesional',
                                                              'Mensaje claro, buena luz y audio entendible',
                                                              'Comprar todo el equipo',
                                                              'Editar durante 10 horas'],
                                                  'answer': 1,
                                                  'explanation': 'La claridad del mensaje y la calidad básica son '
                                                                 'suficientes para empezar.'},
                                                 {'question': '¿Qué opción sirve si alguien no quiere mostrar su cara?',
                                                  'options': ['No publicar nunca',
                                                              'Grabar manos, proceso, producto o voz en off',
                                                              'Inventar testimonios',
                                                              'Usar videos de otros sin permiso'],
                                                  'answer': 1,
                                                  'explanation': 'Hay formatos útiles que no requieren aparecer en '
                                                                 'cámara.'},
                                                 {'question': '¿Para qué puede ayudar la IA antes de grabar?',
                                                  'options': ['Convertir guiones en lista de escenas',
                                                              'Sostener el celular físicamente',
                                                              'Garantizar viralidad',
                                                              'Reemplazar el producto'],
                                                  'answer': 0,
                                                  'explanation': 'La IA puede ordenar ideas y tomas antes de '
                                                                 'grabar.'}]},
                          'assignment': {'title': 'Actividad final 6: Plan de grabación de 3 videos',
                                         'type': 'Text',
                                         'question': '<p>Diseña el plan de grabación de 3 videos. Para cada uno '
                                                     'incluye:</p><ul><li>Idea del video.</li><li>Lugar donde '
                                                     'grabarás.</li><li>Qué se verá en pantalla.</li><li>Qué dirás o '
                                                     'qué texto aparecerá.</li><li>CTA final.</li><li>Qué mejorarás en '
                                                     'luz, audio o encuadre.</li></ul>'}}},
              {'title': 'Sección 7: Crear un calendario de contenido sostenible',
               'lesson': {'title': '7. Publicar con estrategia sin quemarte',
                          'sections': [{'heading': 'La constancia necesita sistema',
                                        'paragraphs': ['Mucha gente abandona el contenido porque intenta crear desde '
                                                       'cero todos los días. Eso agota. Un calendario no es una '
                                                       'cárcel; es una guía para no depender de la inspiración. Te '
                                                       'permite preparar ideas por adelantado, repetir formatos que '
                                                       'funcionan y equilibrar contenido educativo, confianza y venta.',
                                                       'Un calendario simple puede tener tres publicaciones por '
                                                       'semana: una educativa, una de problema/error y una de oferta o '
                                                       'prueba social. Si tienes más energía, puedes subir la '
                                                       'frecuencia. Pero es mejor publicar tres videos sostenibles '
                                                       'durante tres meses que diez videos una semana y desaparecer '
                                                       'después.',
                                                       'La IA puede crear una primera versión del calendario, pero tú '
                                                       'debes ajustarla según tu tiempo real. Si solo tienes dos horas '
                                                       'los domingos, diseña un sistema para grabar varios videos '
                                                       'cortos de una vez. El contenido debe adaptarse a tu vida, no '
                                                       'destruirla.']},
                                       {'heading': 'Cómo reutilizar ideas sin repetirte',
                                        'paragraphs': ['Una misma idea puede convertirse en varios formatos. Por '
                                                       'ejemplo, “errores al responder clientes por WhatsApp” puede '
                                                       'ser un Reel, un carrusel, una historia con encuesta, una '
                                                       'checklist y un mensaje para enviar a leads. Reutilizar no es '
                                                       'copiar; es presentar el mismo aprendizaje de distintas formas.',
                                                       'También puedes crear series. Las series facilitan que la '
                                                       'audiencia entienda qué esperar. Ejemplos: “1 minuto arreglando '
                                                       'tu perfil”, “errores reales de WhatsApp”, “antes y después de '
                                                       'ofertas” o “ideas de Reels para negocios locales”. Las series '
                                                       'reducen el esfuerzo creativo porque mantienen una estructura '
                                                       'repetible.',
                                                       'Un prompt útil: “Con estas 10 ideas, crea un calendario de 30 '
                                                       'días para Instagram Reels y TikTok. Incluye objetivo, hook, '
                                                       'formato, CTA y nivel de esfuerzo. Prioriza ideas fáciles de '
                                                       'grabar con celular”.']}],
                          'quiz': {'title': 'Quiz corto 7: Calendario de contenido',
                                   'questions': [{'question': '¿Para qué sirve un calendario de contenido?',
                                                  'options': ['Para depender menos de la inspiración',
                                                              'Para publicar sin objetivo',
                                                              'Para evitar medir resultados',
                                                              'Para copiar a todos'],
                                                  'answer': 0,
                                                  'explanation': 'El calendario convierte la creación de contenido en '
                                                                 'un sistema.'},
                                                 {'question': '¿Qué es mejor para empezar?',
                                                  'options': ['Publicar demasiado y abandonar',
                                                              'Una frecuencia sostenible que puedas mantener',
                                                              'No publicar hasta tener estudio profesional',
                                                              'Cambiar de tema cada día'],
                                                  'answer': 1,
                                                  'explanation': 'La sostenibilidad importa más que la intensidad '
                                                                 'inicial.'},
                                                 {'question': '¿Qué significa reutilizar contenido?',
                                                  'options': ['Robar contenido',
                                                              'Convertir una idea en varios formatos útiles',
                                                              'Repetir sin mejorar',
                                                              'Eliminar el calendario'],
                                                  'answer': 1,
                                                  'explanation': 'Una buena idea puede vivir en varios formatos.'}]},
                          'assignment': {'title': 'Actividad final 7: Calendario de 14 días',
                                         'type': 'Document',
                                         'question': '<p>Sube un calendario de contenido de 14 días. Debe '
                                                     'incluir:</p><ul><li>Día de publicación.</li><li>Idea o título '
                                                     'del video.</li><li>Pilar de '
                                                     'contenido.</li><li>Hook.</li><li>CTA.</li><li>Dificultad de '
                                                     'grabación: baja, media o alta.</li></ul><p>El calendario debe '
                                                     'ser realista para una persona que trabaja sola o con poco '
                                                     'equipo.</p>'}}},
              {'title': 'Sección 8: Convertir mensajes en ventas por WhatsApp',
               'lesson': {'title': '8. Conversaciones que cierran sin presionar',
                          'sections': [{'heading': 'WhatsApp es parte del embudo, no solo un chat',
                                        'paragraphs': ['En muchos negocios de Latinoamérica, la venta no termina en la '
                                                       'red social: termina en WhatsApp. La persona ve un video, entra '
                                                       'al perfil, pregunta por DM o toca el link. Ahí empieza una '
                                                       'conversación donde se gana o se pierde la venta. Si respondes '
                                                       'tarde, confuso o frío, puedes perder un cliente que ya tenía '
                                                       'interés.',
                                                       'Un buen flujo de WhatsApp no suena robótico. Primero saluda, '
                                                       'confirma el interés, hace una pregunta breve, presenta la '
                                                       'opción adecuada y facilita el siguiente paso. No se trata de '
                                                       'mandar un bloque enorme de texto. Se trata de guiar la '
                                                       'conversación con claridad. El cliente no quiere sentirse '
                                                       'perseguido; quiere sentirse entendido.',
                                                       'Puedes usar WhatsApp Business para ordenar respuestas rápidas, '
                                                       'catálogo, etiquetas y horarios. Aunque no automatices todo, '
                                                       'tener mensajes base mejora muchísimo la atención. La IA puede '
                                                       'ayudarte a redactar esos mensajes en distintos tonos: amable, '
                                                       'directo, juvenil, premium o profesional.']},
                                       {'heading': 'Estructura de respuesta que vende',
                                        'paragraphs': ['Una estructura sencilla es: saludo + reconocimiento + pregunta '
                                                       '+ recomendación + acción. Ejemplo: “Hola, gracias por '
                                                       'escribir. Sí, te puedo ayudar con eso. Para recomendarte bien, '
                                                       '¿tu negocio ya vende por Instagram o recién estás empezando? '
                                                       'Según eso te paso la opción más adecuada”. Esta respuesta no '
                                                       'presiona, pero sí conduce.',
                                                       'También necesitas respuestas para objeciones. Objeciones '
                                                       'comunes: “está caro”, “lo voy a pensar”, “no tengo tiempo”, '
                                                       '“mándame info” o “¿me haces descuento?”. La IA puede ayudarte '
                                                       'a crear respuestas que no suenen defensivas. La clave es '
                                                       'validar la duda y volver al valor.',
                                                       'No prometas cosas falsas por cerrar rápido. Una venta mal '
                                                       'cerrada puede traer reclamos y mala reputación. Es mejor '
                                                       'calificar bien al cliente y ofrecer lo que realmente puedes '
                                                       'cumplir.']}],
                          'quiz': {'title': 'Quiz corto 8: WhatsApp y cierre',
                                   'questions': [{'question': '¿Por qué WhatsApp es importante en muchos negocios?',
                                                  'options': ['Porque suele ser donde se resuelven dudas y se cierra '
                                                              'la venta',
                                                              'Porque reemplaza el producto',
                                                              'Porque elimina la necesidad de contenido',
                                                              'Porque solo sirve para amigos'],
                                                  'answer': 0,
                                                  'explanation': 'WhatsApp suele conectar el interés con la decisión '
                                                                 'de compra.'},
                                                 {'question': '¿Qué debe hacer una buena respuesta inicial?',
                                                  'options': ['Presionar de inmediato',
                                                              'Saludar, entender el interés y guiar el siguiente paso',
                                                              'Enviar 20 párrafos',
                                                              'Ignorar la pregunta'],
                                                  'answer': 1,
                                                  'explanation': 'La conversación debe sentirse clara y humana.'},
                                                 {'question': '¿Qué herramienta de WhatsApp Business ayuda a ordenar '
                                                              'conversaciones?',
                                                  'options': ['Etiquetas y respuestas rápidas',
                                                              'Cambiar el color del teléfono',
                                                              'Borrar clientes',
                                                              'Publicar reels automáticamente'],
                                                  'answer': 0,
                                                  'explanation': 'Las etiquetas y respuestas rápidas mejoran la '
                                                                 'gestión comercial.'}]},
                          'assignment': {'title': 'Actividad final 8: Guion de venta por WhatsApp',
                                         'type': 'Document',
                                         'question': '<p>Sube un documento con un flujo de conversación por WhatsApp. '
                                                     'Incluye:</p><ul><li>Mensaje de bienvenida.</li><li>3 preguntas '
                                                     'para entender al cliente.</li><li>Mensaje para presentar tu '
                                                     'oferta.</li><li>Respuesta a la objeción “está '
                                                     'caro”.</li><li>Respuesta a la objeción “lo voy a '
                                                     'pensar”.</li><li>Mensaje de cierre con siguiente '
                                                     'paso.</li></ul><p>Debe sonar natural, no desesperado.</p>'}}},
              {'title': 'Sección 9: Usar IA para responder sin sonar como robot',
               'lesson': {'title': '9. Mensajes, seguimiento y tono humano',
                          'sections': [{'heading': 'La IA debe sonar como apoyo, no como reemplazo frío',
                                        'paragraphs': ['La IA puede ayudarte a responder más rápido, pero si copias '
                                                       'respuestas genéricas, el cliente lo nota. Un mensaje demasiado '
                                                       'perfecto, largo o rígido puede sentirse falso. La clave es '
                                                       'usar IA para crear borradores y luego ajustar palabras, '
                                                       'contexto y tono. Un buen mensaje comercial debe parecer '
                                                       'escrito por una persona que entiende la situación.',
                                                       'Para lograrlo, dale ejemplos de tu estilo. Puedes decirle: '
                                                       '“Responde como una persona joven, clara y amable. Usa frases '
                                                       'cortas. No uses palabras como ‘estimado cliente’ ni suenes '
                                                       'corporativo. Mantén el mensaje en menos de 70 palabras”. Esto '
                                                       'reduce el tono robótico.',
                                                       'También puedes crear una biblioteca de respuestas. Por '
                                                       'ejemplo: saludo inicial, envío de precios, explicación del '
                                                       'servicio, seguimiento después de 24 horas, recordatorio '
                                                       'amable, cierre y agradecimiento. Con una biblioteca, no tienes '
                                                       'que pensar desde cero cada vez.']},
                                       {'heading': 'Seguimiento sin incomodar',
                                        'paragraphs': ['Muchos clientes no compran en el primer mensaje. A veces están '
                                                       'ocupados, comparando opciones o esperando dinero. Hacer '
                                                       'seguimiento no es molestar si se hace con respeto. Un buen '
                                                       'seguimiento aporta algo: resume la propuesta, recuerda el '
                                                       'beneficio o ofrece resolver una duda. Un mal seguimiento solo '
                                                       'dice “¿vas a comprar?”.',
                                                       'Ejemplo de seguimiento: “Hola, te escribo para saber si te '
                                                       'quedó alguna duda sobre la propuesta. Te resumo rápido: la '
                                                       'idea sería ayudarte a ordenar tu perfil y crear 10 ideas de '
                                                       'contenido para que empieces a recibir más consultas. Si '
                                                       'quieres, hoy puedo separarte un espacio”. Es claro, amable y '
                                                       'vuelve al valor.',
                                                       'La IA puede crear diferentes versiones de seguimiento según el '
                                                       'caso. Pero debes evitar enviar demasiados mensajes. Define una '
                                                       'regla: primer seguimiento al día siguiente, segundo '
                                                       'seguimiento algunos días después y luego cerrar con '
                                                       'respeto.']}],
                          'quiz': {'title': 'Quiz corto 9: IA y tono humano',
                                   'questions': [{'question': '¿Cuál es una buena forma de usar IA en mensajes '
                                                              'comerciales?',
                                                  'options': ['Copiar todo sin revisar',
                                                              'Crear borradores y adaptarlos a tu tono',
                                                              'Enviar textos enormes siempre',
                                                              'Ocultar información'],
                                                  'answer': 1,
                                                  'explanation': 'La IA acelera, pero el ajuste humano mejora '
                                                                 'confianza.'},
                                                 {'question': '¿Qué hace que un mensaje suene menos robótico?',
                                                  'options': ['Frases cortas, contexto y tono natural',
                                                              'Palabras corporativas innecesarias',
                                                              'Promesas exageradas',
                                                              'No responder la duda'],
                                                  'answer': 0,
                                                  'explanation': 'La naturalidad mejora cuando el mensaje es breve y '
                                                                 'específico.'},
                                                 {'question': '¿Cómo debe ser un seguimiento comercial?',
                                                  'options': ['Respetuoso y con valor',
                                                              'Insistente y agresivo',
                                                              'Sin contexto',
                                                              'Cada 5 minutos'],
                                                  'answer': 0,
                                                  'explanation': 'El seguimiento debe recordar valor y abrir espacio '
                                                                 'para dudas.'}]},
                          'assignment': {'title': 'Actividad final 9: Biblioteca de respuestas con IA',
                                         'type': 'Text',
                                         'question': '<p>Crea una biblioteca de 8 respuestas comerciales para tu '
                                                     'negocio:</p><ul><li>Bienvenida.</li><li>Pregunta de '
                                                     'diagnóstico.</li><li>Envío de precio.</li><li>Explicación de '
                                                     'beneficio.</li><li>Respuesta a duda '
                                                     'frecuente.</li><li>Seguimiento 24 horas '
                                                     'después.</li><li>Seguimiento final '
                                                     'respetuoso.</li><li>Agradecimiento después de la '
                                                     'compra.</li></ul><p>Cada respuesta debe tener menos de 80 '
                                                     'palabras.</p>'}}},
              {'title': 'Sección 10: Armar un embudo simple de contenido a venta',
               'lesson': {'title': '10. Del video al cliente: sistema completo',
                          'sections': [{'heading': 'Un embudo simple evita depender de la suerte',
                                        'paragraphs': ['Publicar contenido sin embudo es como abrir una tienda sin '
                                                       'saber qué hacer cuando alguien entra. El embudo no tiene que '
                                                       'ser complicado. Puede ser: video corto que atrae, perfil que '
                                                       'explica, CTA que invita, WhatsApp que conversa, oferta que '
                                                       'cierra y seguimiento que recupera interesados. Ese camino '
                                                       'convierte atención en oportunidad comercial.',
                                                       'Cada parte del embudo debe tener una función. El video no '
                                                       'siempre vende todo; muchas veces solo despierta interés. El '
                                                       'perfil confirma confianza. El WhatsApp resuelve dudas. La '
                                                       'oferta ordena el valor. El seguimiento evita perder personas '
                                                       'que sí estaban interesadas. Cuando entiendes esto, dejas de '
                                                       'pedirle a un solo Reel que haga todo el trabajo.',
                                                       'La IA puede ayudarte a diseñar el embudo completo. Puedes '
                                                       'pedirle que revise si hay huecos: “Este es mi nicho, oferta, '
                                                       'bio, CTA y flujo de WhatsApp. Evalúa el embudo y dime dónde se '
                                                       'puede perder un cliente”. Esa revisión te ayuda a encontrar '
                                                       'puntos débiles.']},
                                       {'heading': 'Qué medir para mejorar',
                                        'paragraphs': ['No necesitas métricas complicadas al inicio. Mide cuatro '
                                                       'cosas: videos publicados, mensajes recibidos, conversaciones '
                                                       'calificadas y ventas cerradas. Si tienes vistas pero nadie '
                                                       'escribe, puede fallar el CTA o la oferta. Si escriben pero no '
                                                       'compran, puede fallar el WhatsApp, el precio, la confianza o '
                                                       'la claridad de beneficios.',
                                                       'También mira qué temas generan mejores conversaciones. No todo '
                                                       'video con muchas vistas trae clientes. A veces un video '
                                                       'educativo muy específico atrae menos gente, pero mejores '
                                                       'leads. Por eso, además de vistas y likes, revisa comentarios, '
                                                       'guardados, mensajes y preguntas reales.',
                                                       'El proyecto final consiste en juntar todo: nicho, oferta, '
                                                       'perfil, ideas, guiones, calendario, WhatsApp, respuestas y '
                                                       'métricas. Al terminar, el estudiante no tiene solo teoría; '
                                                       'tiene un sistema mínimo listo para probar durante 14 días.']}],
                          'quiz': {'title': 'Quiz corto 10: Embudo y métricas',
                                   'questions': [{'question': '¿Qué es un embudo simple de venta?',
                                                  'options': ['Un camino que lleva de la atención al contacto y a la '
                                                              'compra',
                                                              'Un archivo de Excel obligatorio',
                                                              'Un video viral sin oferta',
                                                              'Una promoción sin seguimiento'],
                                                  'answer': 0,
                                                  'explanation': 'El embudo ordena los pasos desde contenido hasta '
                                                                 'venta.'},
                                                 {'question': '¿Qué puede indicar que hay vistas pero nadie escribe?',
                                                  'options': ['Puede fallar el CTA, la oferta o la claridad del perfil',
                                                              'Todo está perfecto',
                                                              'No se puede mejorar',
                                                              'El negocio debe cerrar'],
                                                  'answer': 0,
                                                  'explanation': 'Las vistas sin contacto muestran un posible problema '
                                                                 'de conversión.'},
                                                 {'question': '¿Qué métrica importa además de likes?',
                                                  'options': ['Mensajes recibidos y conversaciones calificadas',
                                                              'Color del botón',
                                                              'Número de emojis',
                                                              'Cantidad de filtros'],
                                                  'answer': 0,
                                                  'explanation': 'Los mensajes y leads muestran intención comercial '
                                                                 'más real.'}]},
                          'assignment': {'title': 'Actividad final 10: Proyecto final del sistema de ventas',
                                         'type': 'Document',
                                         'question': '<p>Sube un documento final con tu sistema mínimo de ventas por '
                                                     'contenido. Debe incluir:</p><ul><li>Nicho '
                                                     'definido.</li><li>Oferta de entrada.</li><li>Bio '
                                                     'optimizada.</li><li>10 ideas de contenido priorizadas.</li><li>3 '
                                                     'guiones listos para grabar.</li><li>Calendario de 14 '
                                                     'días.</li><li>Flujo de WhatsApp.</li><li>Biblioteca de '
                                                     'respuestas.</li><li>4 métricas que medirás durante la '
                                                     'prueba.</li></ul><p>El documento debe ser claro, ordenado y '
                                                     'aplicable a un negocio real.</p>'}}}]}


def field_exists(doctype, fieldname):
    try:
        meta = frappe.get_meta(doctype)
        return bool(meta.get_field(fieldname))
    except Exception:
        return True


def set_value_if_field_exists(doc, fieldname, value):
    if field_exists(doc.doctype, fieldname):
        setattr(doc, fieldname, value)


def get_existing_name(doctype, filters):
    found = frappe.get_all(doctype, filters=filters, fields=["name"], limit=1)
    if not found:
        return None
    first = found[0]
    return first.get("name") if isinstance(first, dict) else first.name


def create_or_update_category(category_title):
    existing = get_existing_name("LMS Category", {"category": category_title})
    if existing:
        return existing

    doc = frappe.get_doc({
        "doctype": "LMS Category",
        "category": category_title,
    })
    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    return doc.name


def create_or_update_course(category_name):
    existing = get_existing_name("LMS Course", {"title": COURSE_DATA["title"]})
    if existing:
        course = frappe.get_doc("LMS Course", existing)
    else:
        course = frappe.new_doc("LMS Course")
        course.title = COURSE_DATA["title"]

    set_value_if_field_exists(course, "short_introduction", COURSE_DATA["short_introduction"])
    set_value_if_field_exists(course, "description", COURSE_DATA["description"])
    set_value_if_field_exists(course, "published", 1)
    set_value_if_field_exists(course, "category", category_name)
    set_value_if_field_exists(course, "card_gradient", COURSE_DATA.get("card_gradient", "Blue"))
    set_value_if_field_exists(course, "enable_certification", 1)

    if not existing:
        course.insert(ignore_permissions=True, ignore_mandatory=True)
    else:
        course.save(ignore_permissions=True)

    add_instructor_if_missing(course)
    return course.name


def add_instructor_if_missing(course):
    if not field_exists("LMS Course", "instructors"):
        return

    instructors = course.get("instructors") or []
    for row in instructors:
        if getattr(row, "instructor", None) == INSTRUCTOR_NAME:
            return

    course.append("instructors", {"instructor": INSTRUCTOR_NAME})
    course.save(ignore_permissions=True)


def create_or_update_assignment(course_name, assignment_data):
    title = assignment_data["title"]
    existing = get_existing_name("LMS Assignment", {"title": title, "course": course_name})

    if existing:
        doc = frappe.get_doc("LMS Assignment", existing)
    else:
        doc = frappe.new_doc("LMS Assignment")
        doc.title = title

    set_value_if_field_exists(doc, "course", course_name)
    set_value_if_field_exists(doc, "type", assignment_data.get("type", "Text"))
    set_value_if_field_exists(doc, "question", assignment_data.get("question", ""))

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    return doc.name


def create_or_update_question(question_data):
    q_text = question_data["question"]
    existing = get_existing_name("LMS Question", {"question": q_text})

    if existing:
        doc = frappe.get_doc("LMS Question", existing)
    else:
        doc = frappe.new_doc("LMS Question")
        doc.question = q_text

    set_value_if_field_exists(doc, "type", "Choices")

    options = question_data.get("options", [])
    answer_idx = int(question_data.get("answer", 0))
    explanation = question_data.get("explanation", "Respuesta correcta.")

    for idx in range(4):
        option_field = f"option_{idx + 1}"
        correct_field = f"is_correct_{idx + 1}"
        explanation_field = f"explanation_{idx + 1}"

        set_value_if_field_exists(doc, option_field, options[idx] if idx < len(options) else "")
        set_value_if_field_exists(doc, correct_field, 1 if idx == answer_idx else 0)
        if idx == answer_idx:
            set_value_if_field_exists(doc, explanation_field, explanation)
        else:
            set_value_if_field_exists(doc, explanation_field, "")

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    return doc.name


def create_or_update_quiz(quiz_data):
    title = quiz_data["title"]
    existing = get_existing_name("LMS Quiz", {"title": title})

    if existing:
        doc = frappe.get_doc("LMS Quiz", existing)
    else:
        doc = frappe.new_doc("LMS Quiz")
        doc.title = title

    set_value_if_field_exists(doc, "passing_percentage", quiz_data.get("passing_percentage", 70))
    set_value_if_field_exists(doc, "max_attempts", quiz_data.get("max_attempts", 3))

    if not existing:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    if field_exists("LMS Quiz", "questions"):
        doc.set("questions", [])
        for q in quiz_data.get("questions", []):
            question_name = create_or_update_question(q)
            doc.append("questions", {"question": question_name, "marks": 1})

    doc.save(ignore_permissions=True)
    return doc.name


def paragraph_block(text):
    return {
        "type": "paragraph",
        "data": {
            "text": text.replace("\n", "<br>")
        }
    }


def header_block(text, level=3):
    return {
        "type": "header",
        "data": {
            "text": text,
            "level": level
        }
    }


def build_editorjs_content(lesson_data, quiz_name=None, assignment_name=None):
    blocks = []

    blocks.append(header_block("Objetivo de la lectura", 2))
    blocks.append(paragraph_block(
        "Lee esta sección con una idea práctica: al terminar, tendrás una pieza concreta para mejorar tu sistema de ventas. "
        "No necesitas hacerlo perfecto; necesitas hacerlo claro, aplicable y medible."
    ))

    for section in lesson_data.get("sections", []):
        blocks.append(header_block(section.get("heading", "Tema"), 3))
        for paragraph in section.get("paragraphs", []):
            blocks.append(paragraph_block(paragraph))

    if quiz_name:
        blocks.append(header_block("Quiz corto de la lectura", 3))
        blocks.append(paragraph_block("Responde este quiz breve para comprobar que entendiste las ideas principales antes de pasar a la actividad final."))
        blocks.append({
            "type": "quiz",
            "data": {
                "quiz": quiz_name
            }
        })

    if assignment_name:
        blocks.append(header_block("Actividad final de la sección", 3))
        blocks.append(paragraph_block("Completa la actividad con una respuesta aplicable a un negocio real o ficticio. La meta es que construyas algo que puedas probar, no solo una respuesta teórica."))
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


def create_or_update_lesson(course_name, chapter_name, lesson_data):
    quiz_name = None
    assignment_name = None

    if lesson_data.get("quiz"):
        quiz_name = create_or_update_quiz(lesson_data["quiz"])

    if lesson_data.get("assignment"):
        assignment_name = create_or_update_assignment(course_name, lesson_data["assignment"])

    title = lesson_data["title"]
    existing = get_existing_name("Course Lesson", {"title": title, "chapter": chapter_name})

    if existing:
        doc = frappe.get_doc("Course Lesson", existing)
    else:
        doc = frappe.new_doc("Course Lesson")
        doc.title = title

    set_value_if_field_exists(doc, "chapter", chapter_name)
    set_value_if_field_exists(doc, "course", course_name)
    set_value_if_field_exists(doc, "body", "")
    set_value_if_field_exists(doc, "content", build_editorjs_content(lesson_data, quiz_name, assignment_name))

    if existing:
        doc.save(ignore_permissions=True)
    else:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    return doc.name


def create_or_update_chapter(course_name, chapter_data):
    title = chapter_data["title"]
    existing = get_existing_name("Course Chapter", {"title": title, "course": course_name})

    if existing:
        doc = frappe.get_doc("Course Chapter", existing)
    else:
        doc = frappe.new_doc("Course Chapter")
        doc.title = title

    set_value_if_field_exists(doc, "course", course_name)

    if not existing:
        doc.insert(ignore_permissions=True, ignore_mandatory=True)

    lesson_name = create_or_update_lesson(course_name, doc.name, chapter_data["lesson"])

    if field_exists("Course Chapter", "lessons"):
        doc.set("lessons", [])
        doc.append("lessons", {"lesson": lesson_name})

    doc.save(ignore_permissions=True)
    return doc.name


def rebuild_course_chapters(course_name, chapter_names):
    course = frappe.get_doc("LMS Course", course_name)
    if field_exists("LMS Course", "chapters"):
        course.set("chapters", [])
        for chapter_name in chapter_names:
            course.append("chapters", {"chapter": chapter_name})
    course.save(ignore_permissions=True)


def run():
    frappe.set_user("Administrator")
    print("Iniciando creación/actualización del curso...")

    category_name = create_or_update_category(COURSE_DATA["category"])
    course_name = create_or_update_course(category_name)

    chapter_names = []
    for chapter_data in COURSE_DATA.get("chapters", []):
        chapter_name = create_or_update_chapter(course_name, chapter_data)
        chapter_names.append(chapter_name)

    rebuild_course_chapters(course_name, chapter_names)
    frappe.db.commit()

    # Actualizar estadísticas (lecciones, rating, enrollments) para que no salga en 0
    from lms.lms.doctype.lms_course.lms_course import update_course_statistics
    update_course_statistics()
    frappe.db.commit()
    print("Estadísticas del curso actualizadas correctamente.")

    print("Curso creado o actualizado correctamente:", COURSE_DATA["title"])
    print("Curso ID:", course_name)
    print("Secciones:", len(chapter_names))
    print("Lecturas:", len(chapter_names))
    print("Quizzes:", len(chapter_names))
    print("Actividades finales:", len(chapter_names))


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
