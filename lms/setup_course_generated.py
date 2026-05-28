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
    "title": "Lanza y Vende con IA: TikTok, Reels & WhatsApp para Tu Primer Éxito Digital",
    "short_introduction": "Domina la ruta directa hacia tu primera venta online. Este microcurso potencia TikTok, Reels, WhatsApp y la IA para un lanzamiento y monetización sin precedentes.",
    "description": "<p>Transforma tu visión de producto en una realidad rentable. Si eres un emprendedor o principiante listo para debutar en el mercado digital, este microcurso es tu atajo estratégico para lanzar y monetizar tu primera oferta, ya sea física o digital, con una eficiencia inigualable.</p><p>Hemos diseñado la metodología precisa para asegurar tu primera venta online. Integrando el dinamismo de TikTok y Reels con la conversión directa de WhatsApp, te equipamos con un sistema de ventas ágil. Pero vamos un paso más allá: la Inteligencia Artificial se convierte en tu copiloto estratégico, simplificando radicalmente cada fase del proceso y acelerando tus resultados, incluso sin experiencia previa en marketing digital o ventas.</p><p><b>Este curso resuelve desafíos clave:</b></p><ul>    <li><b>Claridad en el Lanzamiento:</b> Convierte la incertidumbre del debut digital en un plan de acción claro y ejecutable.</li>    <li><b>Monetización en Redes:</b> Transforma la visibilidad en TikTok y Reels en oportunidades de venta tangibles y medibles.</li>    <li><b>Dominio de la IA:</b> Deja atrás el temor a la tecnología; la Inteligencia Artificial se convertirá en tu herramienta más potente para la productividad y el cierre de ventas.</li></ul><p>Al completar este microcurso, no solo habrás formulado una estrategia de contenido y ventas robusta y personalizada, sino que también dominarás la creación de publicaciones persuasivas con soporte de IA, establecerás un embudo de ventas impecable a través de WhatsApp, y ejecutarás con confianza los pasos precisos para materializar tu primera venta online de forma autónoma. Prepárate para no solo vender, sino para marcar el inicio de tu imperio digital.</p>",
    "card_gradient": "Blue",
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza comprensión, aplicación real, claridad y creatividad antes que perfección técnica. Valora respuestas naturales, ejemplos útiles y esfuerzo real. Penaliza respuestas vacías, copiadas, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, qué mejorar, nota final y estado: Aprobado si es 7 o más, Desaprobado si es menor a 7.",
    "chapters": [
        {
            "title": "Módulo 1: La Base de tu Éxito: Tu Producto y Audiencia Ideal",
            "lesson": {
                "title": "Define tu Producto, Encuentra a tu Cliente Ideal y Resuelve un Problema Real",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Bienvenido/a a la primera parada de tu viaje para vender online! Sé que estás emocionado/a por empezar a crear contenido y ver esas primeras ventas, pero confía en mí: esta lección es la más importante. Es como construir una casa; si los cimientos no son sólidos, no importa lo bonita que sea la fachada.",
                            "Aquí no te voy a hablar de algoritmos complejos ni de estrategias de marketing de gurú. Vamos a lo esencial, a lo que *realmente* te hará vender: entender qué ofreces, a quién se lo ofreces y por qué esa persona lo necesita. Esto es lo que te dará la claridad para el resto del curso y para que tu primera venta sea un hecho, no una ilusión."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Imagina que tienes el producto más innovador del mundo, pero nadie sabe que lo necesita. O, peor aún, lo ofreces a personas que no le ven ningún valor. ¿De qué sirve? Exacto, de nada. Por eso, estos tres puntos van de la mano y son la base de tu éxito:",
                            "**1. Define tu Producto (más allá de lo obvio):** No es solo 'vendo tazas personalizadas' o 'ofrezco consultorías'. Piensa: ¿qué hay de especial en *tus* tazas? ¿Qué tipo de personalización haces? ¿Qué problema resuelve tu consultoría? Tu producto es el vehículo que entregará un valor. Detalla sus características, sí, pero sobre todo, su 'superpoder'. ¿Es su diseño único, su durabilidad, la emoción que genera, el ahorro de tiempo que ofrece?",
                            "**2. Encuentra a tu Cliente Ideal (tu alma gemela comercial):** Este es uno de los errores más grandes de los principiantes: querer venderle a 'todo el mundo'. Cuando intentas venderle a todos, no le vendes a nadie. Tu cliente ideal no es una estadística, es una persona real con sueños, problemas, intereses y una forma de vivir. ¿Quién es esa persona que *realmente* apreciaría tu producto, que está buscando exactamente lo que tú ofreces? Piensa en su edad, dónde vive, qué le gusta hacer, qué le preocupa, qué tipo de lenguaje usa. ¡Sé específico/a!",
                            "**3. Resuelve un Problema Real (el verdadero motivo de compra):** La gente no compra productos; compra soluciones a sus problemas o la satisfacción de sus deseos. ¿Qué dolor le quitas a tu cliente ideal? ¿Qué necesidad le satisfaces? ¿Qué aspiración le ayudas a cumplir? Si tu producto le ahorra tiempo, le hace la vida más fácil, le mejora el ánimo, le ayuda a aprender algo nuevo o le resuelve una preocupación, ¡bingo! Has encontrado un problema real. Conectar tu producto con ese problema es la clave para que la venta sea casi natural."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Veámoslo con un par de casos concretos para que te quede clarísimo:",
                            "**Ejemplo 1: Una artista que vende láminas y cuadros digitales personalizados.**",
                            "- **Producto:** 'Retratos de mascotas estilo acuarela digital'.",
                            "- **Cliente Ideal:** Personas (entre 25-55 años, con ingresos medios-altos, amantes de los animales, a menudo con perros o gatos como miembros de la familia), que buscan una forma única y emotiva de honrar a sus mascotas, ya sea como decoración personal, un regalo especial o un recuerdo para siempre. Suelen estar en grupos de amantes de mascotas en redes sociales, valoran el arte original y personalizado.",
                            "- **Problema que Resuelve:** La dificultad de encontrar regalos originales y con sentimiento para amantes de animales, el deseo de tener un recuerdo artístico y personalizado de su mascota que capture su esencia, o la necesidad de decorar su hogar con algo que refleje su amor por los animales de una manera única y artística.",
                            "**Ejemplo 2: Un experto que vende una guía digital para organizar viajes.**",
                            "- **Producto:** 'Guía definitiva en PDF: Organiza tu Viaje a Europa sin Estrés y Ahorrando'.",
                            "- **Cliente Ideal:** Viajeros frecuentes o primerizos (entre 20-40 años, estudiantes, parejas jóvenes, familias), que quieren viajar por Europa, pero se sienten abrumados por la planificación (rutas, presupuesto, visados, alojamiento), tienen miedo a los imprevistos o a gastar de más. Buscan eficiencia, consejos prácticos y quieren disfrutar sin la carga de la organización. A menudo buscan información en blogs de viajes o grupos de Facebook sobre viajar.",
                            "- **Problema que Resuelve:** La frustración y el estrés de planificar un viaje complejo, el miedo a cometer errores o perder tiempo y dinero, la falta de información centralizada y confiable, y el deseo de tener una experiencia de viaje fluida y económica sin ser un experto en logística."
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "Aquí te cuento lo que NO debes hacer, porque son los tropiezos más frecuentes en esta etapa:",
                            "- **No definir un nicho:** Decir 'vendo ropa' o 'doy clases de inglés'. Es como gritar en un estadio, nadie te escucha. Sé específico: 'vendo ropa sostenible para mujeres profesionales de 30-45 años' o 'doy clases de inglés conversacional para viajeros de nivel intermedio'.",
                            "- **Enamorarse solo del producto:** Creer que tu producto es lo máximo sin pensar si alguien realmente lo necesita o lo quiere. Tu producto es genial, pero debe serlo *para alguien*.",
                            "- **No identificar el problema:** Vender 'características' en lugar de 'soluciones'. No vendas 'un cuaderno de 200 páginas', vende 'la herramienta para organizar tus ideas y reducir el estrés de tu día a día'.",
                            "- **Investigar poco o nada:** Asumir lo que tus clientes quieren sin preguntarles, sin observar sus comentarios en redes sociales o sin ver qué está haciendo tu competencia. ¡No adivines, investiga!",
                            "- **Cambiar de idea constantemente:** Saltar de un producto a otro, o de un cliente ideal a otro, sin darle tiempo a asentar tu base. La claridad viene con la concentración."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "Recuerda la fórmula mágica: **Tu Producto + Tu Cliente Ideal + El Problema que Resuelves = El cimiento de tu éxito online.** Si tienes estos tres elementos claros, el resto del camino se vuelve mucho más sencillo y directo. Sabrás qué decir, cómo decirlo y a quién dirigirte.",
                            "**Tu primera tarea práctica y no negociable:** Toma papel y lápiz (o abre un documento en tu ordenador) y responde a estas preguntas de la forma más detallada y sincera posible. ¡No te saltes este paso! Es el ancla de todo lo que haremos a continuación:",
                            "1. **Mi Producto/Servicio es...** (sé específico, describe su 'superpoder')",
                            "2. **Mi Cliente Ideal es...** (imagina a una persona real: edad, intereses, qué le gusta, qué le duele)",
                            "3. **El Problema Real que mi Producto/Servicio Resuelve es...** (o el deseo que satisface).",
                            "Cuando tengas esto claro, habrás dado un paso gigante. ¡Nos vemos en la siguiente lección, donde transformaremos esta claridad en contenido real!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: El Cimiento de tu Negocio Online",
                    "questions": [
                        {
                            "question": "Según la lección, ¿cuál es el cimiento más importante para el éxito al vender online?",
                            "options": [
                                "Tener un conocimiento profundo de los algoritmos de las redes sociales.",
                                "Crear contenido viral y atractivo de forma constante.",
                                "Comprender qué ofreces, a quién se lo ofreces y qué problema resuelve.",
                                "Enamorarse de tu producto y creer ciegamente en él."
                            ],
                            "answer": 2,
                            "explanation": "La lección enfatiza que el cimiento más sólido es entender tu producto (qué ofreces), tu cliente ideal (a quién) y el problema real que solucionas (por qué lo necesita esa persona)."
                        },
                        {
                            "question": "¿Cuál de las siguientes afirmaciones describe mejor el error de 'enamorarse solo del producto'?",
                            "options": [
                                "Invertir demasiado tiempo en mejorar el producto en lugar de venderlo.",
                                "Asumir que tu producto es genial sin verificar si hay una necesidad real en el mercado.",
                                "No estar dispuesto a cambiar las características de tu producto.",
                                "Poner un precio demasiado alto a tu producto debido a su calidad."
                            ],
                            "answer": 1,
                            "explanation": "'Enamorarse solo del producto' se refiere a creer que tu producto es lo máximo sin pensar si alguien realmente lo necesita o lo quiere, asumiendo su valor sin validación de mercado."
                        },
                        {
                            "question": "Cuando la lección sugiere definir el 'superpoder' de tu producto, ¿a qué aspecto se refiere principalmente?",
                            "options": [
                                "A la tecnología avanzada o los materiales de alta calidad con los que está hecho.",
                                "Al valor único, la emoción que genera o la solución de problema que ofrece.",
                                "A su capacidad para ser personalizado en múltiples variantes.",
                                "Al volumen de ventas que esperas alcanzar con él."
                            ],
                            "answer": 1,
                            "explanation": "El 'superpoder' del producto va más allá de las características obvias; se refiere a la emoción que genera, el ahorro de tiempo, la durabilidad o la solución única que aporta al cliente, es decir, el valor o el problema que resuelve."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Los Cimientos de tu Éxito",
                    "type": "Text",
                    "question": "¡Excelente! Acabas de aprender que la base de todo tu éxito online reside en la claridad de tres pilares fundamentales. Como se mencionó en la lección, este no es un paso que debas saltarte, sino el cimiento que sostendrá tu negocio digital.\n\n**Tu Misión:**\nPara esta actividad práctica, vas a aplicar directamente los conceptos aprendidos para definir los pilares de TU propio negocio. Toma papel y lápiz, o abre un documento digital, y desarrolla cada uno de los siguientes puntos con la mayor profundidad y detalle posible. Piensa en los ejemplos prácticos y los errores comunes que vimos para evitar caer en las trampas más frecuentes.\n\n**Entregables:**\n\n1.  **Mi Producto/Servicio es...**\n    *   Describe tu producto o servicio más allá de lo obvio. ¿Cuáles son sus características principales? Pero, sobre todo, ¿cuál es su 'superpoder'? ¿Qué lo hace único y valioso? ¿Qué tipo de emoción genera o qué beneficio tangible ofrece (ahorro de tiempo, mejora de calidad de vida, etc.)?\n\n2.  **Mi Cliente Ideal es...**\n    *   ¡No vendas a 'todo el mundo'! Imagina a tu cliente ideal como una persona real. Dale vida:\n        *   ¿Qué edad tiene aproximadamente?\n        *   ¿Dónde vive (tipo de lugar, no necesariamente una dirección específica)?\n        *   ¿Cuáles son sus intereses, hobbies, aspiraciones?\n        *   ¿Qué le preocupa, qué le quita el sueño, qué problemas enfrenta en su día a día?\n        *   ¿Qué tipo de lenguaje utiliza?\n        *   ¿Dónde busca soluciones o información (redes sociales, blogs, foros)?\n    *   Sé tan específico/a como los ejemplos de la artista o el experto en viajes de la lección.\n\n3.  **El Problema Real que mi Producto/Servicio Resuelve es... (o el deseo que satisface).**\n    *   Conecta tu producto/servicio directamente con una necesidad profunda de tu cliente ideal. ¿Qué dolor le alivias? ¿Qué frustración eliminas? ¿Qué anhelo o aspiración le ayudas a cumplir? Recuerda: la gente compra soluciones, no solo productos. Describe cómo tu \"superpoder\" del punto 1 se convierte en la respuesta a la \"preocupación\" o el \"deseo\" del punto 2.\n\nTómate tu tiempo para esta reflexión. La claridad que obtengas aquí te guiará en cada decisión futura de marketing y ventas. ¡Adelante!"
                }
            }
        },
        {
            "title": "Módulo 2: Desbloqueando el Poder de TikTok, Reels y la IA",
            "lesson": {
                "title": "Fundamentos del Contenido Atractivo y Cómo la IA Multiplica tu Alcance",
                "sections": [
                    {
                        "heading": "¡Bienvenidos al Corazón de la Creación de Contenido!",
                        "paragraphs": [
                            "¡Hola, futuro vendedor digital! ¿Listos para sumergirnos en el fascinante mundo del contenido corto que realmente vende? En el Módulo 1, hablamos de la visión general y el poder de estas plataformas. Ahora, en el Módulo 2, vamos a desentrañar qué hace que un video sea irresistible en TikTok y Reels, y cómo nuestra aliada, la Inteligencia Artificial (IA), puede multiplicar tu alcance y hacerte la vida mucho más fácil. Prepárate para pasar de la teoría a la acción con ideas claras y herramientas prácticas.",
                            "Este es el momento de entender que no necesitas ser un experto en marketing ni tener un estudio de grabación. Con los fundamentos correctos y la ayuda de la IA, tu teléfono se convertirá en tu centro de creación de contenido, y tu mente en una fábrica de ideas que conectan y venden. ¿Suena bien? ¡Pues vamos a ello!"
                        ]
                    },
                    {
                        "heading": "La Receta del Contenido Atractivo y Cómo la IA es Tu Mejor Aliada",
                        "paragraphs": [
                            "Crear contenido que capture miradas en un mar de videos no es magia, es estrategia y un poco de chispa. Aquí te desgloso los ingredientes clave para que tu contenido sea magnético:",
                            "1.  **El Gancho (Hook) Implacable:** Tienes 3 segundos, ¡máximo! para captar la atención. Piensa en una pregunta provocadora, un truco sorprendente, una afirmación fuerte o una demostración rápida. El gancho es el \"¿Qué demonios es eso?\" que hace que alguien deje de deslizar.",
                            "2.  **Valor o Entretenimiento:** Una vez que los tienes, ¿qué les das? Información útil, una solución a un problema, una risa, inspiración, una nueva perspectiva. Tu contenido debe educar, entretener o inspirar. La gente se queda por lo que obtienen de ti.",
                            "3.  **Autenticidad:** Sé tú mismo. La gente conecta con personas reales, no con marcas perfectas y acartonadas. Muestra un poco de tu personalidad, tus errores, tu proceso. La autenticidad genera confianza y comunidad.",
                            "4.  **Brevedad y Ritmo Dinámico:** Los videos cortos son un sprint, no un maratón. Ve al grano, usa transiciones rápidas, música pegadiza y subtítulos (¡muchos ven sin sonido!). Mantén el ritmo alto para no aburrir.",
                            "5.  **Llamada a la Acción (CTA) Clara:** ¿Qué quieres que hagan después de ver tu video? \"Sígueme para más tips\", \"Comenta tu opinión\", \"Link en mi biografía para comprar\", \"Envía un DM si te interesa\". Hazlo sencillo y directo.",
                            "Ahora, ¿dónde entra la IA en todo esto? ¡Para multiplicarlo! Piensa en la IA como tu asistente personal de marketing digital que trabaja 24/7:",
                            "-   **Generación de Ideas Brillantes:** ¿Bloqueo creativo? Pregúntale a la IA: \"Dame 5 ideas de videos cortos para vender [tu producto/servicio] a [tu público objetivo] que incluyan un gancho fuerte\". ¡Boom, inspiración instantánea!",
                            "-   **Guiones y Descripciones que Enganchan:** La IA puede ayudarte a redactar el guion perfecto para tu video, incluyendo ganchos, puntos clave y llamadas a la acción. También te puede generar descripciones atractivas y hashtags relevantes para maximizar la visibilidad.",
                            "-   **Subtítulos y Edición Básica:** Muchas herramientas de IA (como CapCut o plataformas de IA en línea) pueden generar subtítulos automáticamente, traducir tu contenido o incluso sugerir la música o efectos de sonido adecuados para tu video, ahorrándote horas de trabajo.",
                            "-   **Análisis y Optimización (Un Vistazo):** Aunque es un tema más avanzado, algunas IA pueden analizar qué tipo de contenido funciona mejor para tu audiencia, sugiriendo horarios de publicación o temas que resuenen más. Por ahora, nos enfocamos en la creación, pero la IA puede ser tu brújula a futuro."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico: Velas Aromáticas y la Magia de la IA",
                        "paragraphs": [
                            "Imagina que vendes 'Velas Artesanales para la Relajación' y quieres crear tu primer Reel o TikTok. Te sientes un poco perdido sobre qué grabar.",
                            "**1.  Pidiendo Ideas a la IA:** Abres ChatGPT o Bard y escribes: _\"Soy un pequeño emprendedor que vende velas aromáticas artesanales para la relajación. Dame 3 ideas de videos cortos para TikTok/Reels que atraigan a personas estresadas que buscan desconectar, incluyendo un gancho fuerte y un CTA al final.\"_",
                            "**La IA podría responder:**",
                            "    *   **Idea 1: 'El antes y después de tu espacio'.** Gancho: _'¿Tu casa se siente caótica? ¡Mira cómo cambio esto en 30 segundos!'_ CTA: _'Visita el link en mi bio para encontrar tu vela de la calma.'_",
                            "    *   **Idea 2: 'Detrás de cámaras: La magia de crear calma'.** Gancho: _'No creerás lo que lleva crear una vela que realmente relaja.'_ CTA: _'Sígueme para ver más procesos artesanales y encontrar tu momento zen.'_",
                            "    *   **Idea 3: 'Rutina de 5 minutos para desestresarte'.** Gancho: _'¡Olvídate del estrés en solo 5 minutos!'_ CTA: _'Comenta 'vela' y te envío el link de nuestra colección relax.'_",
                            "**2.  Eligiendo y Desarrollando el Guion con IA:** Te gusta la Idea 3. Ahora pides a la IA: _\"Desarrolla un guion para un Reel de 30 segundos sobre una 'rutina de 5 minutos para desestresarte' usando mi vela. Incluye el gancho, el desarrollo visual y el CTA.\"_",
                            "**La IA te da un guion así:**",
                            "    *   **(0-3 seg) GANCHO:** Video rápido de alguien con cara de estrés, con texto superpuesto: \"¡Tu estrés tiene los minutos contados!\" O un sonido relajante que empieza fuerte y se suaviza. _(Música relajante empieza a sonar)_",
                            "    *   **(3-15 seg) DESARROLLO (Visual y Texto):** Muestra manos encendiendo la vela. Texto: \"1. Enciende tu Vela Esencia de Paz (mostrar la vela).\" Luego, alguien toma una respiración profunda, cierra los ojos. Texto: \"2. Respira profundo 3 veces.\" Finalmente, el video muestra la vela encendida en un rincón acogedor, con alguien leyendo o meditando. Texto: \"3. Disfruta 5 minutos de calma.\" _(Imágenes suaves y transiciones rápidas)_",
                            "    *   **(15-25 seg) BENEFICIO/PRODUCTO:** Un close-up a la vela, mostrando los ingredientes naturales o la llama. Voz en off (o texto): \"Nuestras velas están diseñadas para transformar tu ambiente y tu mente.\" _(Música sube un poco de volumen)_",
                            "    *   **(25-30 seg) CTA:** El texto final grande: \"¡Encuentra tu paz! Link en Bio para nuestra colección Esencia de Paz.\" _(Música suave fade out)_",
                            "¿Lo ves? La IA te ha dado una estructura y un texto que, con tu toque personal y tu creatividad al grabar, se convierte en un video atractivo y listo para vender. ¡Es tu copiloto, no tu reemplazo!"
                        ]
                    },
                    {
                        "heading": "Errores Comunes que Debes Evitar (y Cómo Superarlos)",
                        "paragraphs": [
                            "Aunque la IA es una maravilla, hay trampas comunes en las que caen los principiantes. ¡Evítalas!",
                            "1.  **Ignorar el Gancho:** Si tu video no captura en los primeros segundos, el resto no importa. Dedica tiempo a pensar un buen gancho. La IA es excelente para esto.",
                            "2.  **Ser Demasiado Vendedor Desde el Inicio:** La gente no está en TikTok o Reels para que les vendan directamente. Primero aporta valor, entretén o educa. La venta viene después, como una solución a lo que acabas de ofrecer.",
                            "3.  **Contenido sin Subtítulos:** ¡Error garrafal! Más del 80% de las personas ven videos sin sonido en redes sociales. Si no pones subtítulos, tu mensaje se pierde. La buena noticia es que hay apps (como CapCut) y herramientas de IA que los generan automáticamente.",
                            "4.  **No tener un CTA Claro:** Si no le dices a la gente qué hacer, no lo harán. Sé específico: \"Sígueme\", \"Link en bio\", \"Envía DM\".",
                            "5.  **Perfeccionismo Paralizante:** No esperes la grabación perfecta ni el guion de Hollywood. Empieza, experimenta, aprende. \"Hecho es mejor que perfecto\". Tu primer video será el peor, ¡y eso está bien!",
                            "6.  **Dejar que la IA haga TODO:** La IA es una herramienta, no tu cerebro creativo. Úsala para potenciar tus ideas, no para que cree contenido sin tu esencia. Tu voz, tu personalidad, son insustituibles."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Tu Próxima Acción",
                        "paragraphs": [
                            "Para resumir esta lección crucial: el contenido atractivo en TikTok y Reels se basa en un **gancho potente**, aportar **valor o entretenimiento**, ser **auténtico**, mantener un **ritmo dinámico** y tener una **llamada a la acción clara**. Y la **Inteligencia Artificial** es tu compañera ideal para generar ideas, crear guiones, y hacer tu proceso creativo más eficiente y efectivo.",
                            "**Tu Acción Inmediata:** Piensa en tu producto o servicio. Abre una herramienta de IA (como ChatGPT, Bard, o Copilot) y pídele ideas de videos cortos para tu nicho. Luego, elige la que más te guste y pídele un guion sencillo para tu primer Reel o TikTok. ¡Guarda ese guion! En la próxima lección, lo vamos a llevar a la vida.",
                            "Recuerda: El camino hacia tu primera venta online es paso a paso. ¡No subestimes el poder de un buen video corto! Tu creatividad, potenciada por la IA, es imparable. ¡Vamos a crear!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz del Módulo 2: Contenido Atractivo y la IA",
                    "questions": [
                        {
                            "question": "¿Cuál es el tiempo máximo recomendado para captar la atención de tu audiencia con un 'Gancho Implacable' en TikTok o Reels?",
                            "options": [
                                "10 segundos",
                                "3 segundos",
                                "30 segundos",
                                "1 minuto"
                            ],
                            "answer": 1,
                            "explanation": "La lección enfatiza que tienes un máximo de 3 segundos para captar la atención con un gancho fuerte antes de que el usuario siga deslizando, haciendo que el 'gancho' sea el '¿Qué demonios es eso?'."
                        },
                        {
                            "question": "Según la lección, ¿cuál de los siguientes aspectos NO debe ser delegado completamente a la Inteligencia Artificial, sino que requiere la esencia del creador?",
                            "options": [
                                "La generación de ideas para videos",
                                "La redacción de guiones y descripciones",
                                "La autenticidad y personalidad del creador",
                                "La generación automática de subtítulos"
                            ],
                            "answer": 2,
                            "explanation": "La lección advierte contra 'Dejar que la IA haga TODO', destacando que 'Tu voz, tu personalidad, son insustituibles' y la IA debe ser una herramienta para potenciar, no para reemplazar tu esencia creativa."
                        },
                        {
                            "question": "¿Por qué la lección considera un 'error garrafal' no incluir subtítulos en tus videos cortos para redes sociales?",
                            "options": [
                                "Porque reduce la calidad de la música y los efectos de sonido.",
                                "Porque más del 80% de los usuarios ven videos sin sonido.",
                                "Porque las plataformas penalizan el contenido sin texto visible.",
                                "Porque son indispensables para el SEO en todas las plataformas."
                            ],
                            "answer": 1,
                            "explanation": "Se menciona que 'Más del 80% de las personas ven videos sin sonido en redes sociales. Si no pones subtítulos, tu mensaje se pierde', haciendo que sean cruciales para la accesibilidad y el impacto."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Crea Tu Primer Guion para TikTok/Reel con IA",
                    "type": "Text",
                    "question": "¡Felicidades! Has llegado al momento de aplicar lo aprendido sobre el poder de TikTok, Reels y la IA para crear contenido que engancha. Esta actividad te guiará paso a paso para desarrollar tu primer guion de video corto, utilizando la inteligencia artificial como tu asistente personal. El objetivo es pasar de la teoría a la acción con ideas claras y herramientas prácticas.\n\n**Objetivo de la Actividad:**\n*   Aplicar la \"Receta del Contenido Atractivo\" a un producto o servicio real.\n*   Utilizar una herramienta de IA para generar ideas y desarrollar un guion de video.\n*   Identificar y evitar errores comunes en la creación de contenido corto.\n\n**Instrucciones Detalladas:**\n\n1.  **Define Tu Producto/Servicio:** Piensa en un producto o servicio real que te gustaría vender o promocionar. Si no tienes uno, puedes usar el ejemplo de \"Velas Aromáticas para la Relajación\" de la lección, o elegir uno como:\n    *   Clases de Yoga Online\n    *   Pasteles Artesanales Personalizados\n    *   Servicio de Diseño Gráfico para Emprendedores\n    *   Accesorios para Mascotas Sostenibles\n\n2.  **Genera Ideas con IA:** Abre tu herramienta de IA preferida (ChatGPT, Google Bard, Copilot, etc.). Formula un prompt claro y conciso para pedirle **3 a 5 ideas** de videos cortos (TikTok/Reel) para tu producto/servicio. Es crucial que tu prompt incluya:\n    *   Tu producto/servicio y el público objetivo al que te diriges.\n    *   La solicitud explícita de que cada idea debe incluir un **gancho fuerte** y una **llamada a la acción (CTA)** clara.\n    *   **Ejemplo de prompt:** _\"Soy un pequeño emprendedor que vende [Tu Producto/Servicio] a [Tu Público Objetivo, ej. 'personas estresadas que buscan desconectar']. Dame 3 ideas de videos cortos para TikTok/Reels que atraigan a mi público, incluyendo un gancho fuerte y un CTA al final de cada idea.\"_\n\n3.  **Selecciona la Mejor Idea:** De las 3 a 5 ideas que la IA te proporcione, elige la que consideres más prometedora, original y que mejor se adapte a tu estilo o posibilidades de grabación. Recuerda buscar aquellas que ofrezcan valor o entretenimiento, no solo una venta directa.\n\n4.  **Desarrolla el Guion Completo con IA:** Una vez que tengas tu idea seleccionada, vuelve a tu herramienta de IA. Pídele que desarrolle un guion detallado para un video de **30-60 segundos** basado en esa idea. Asegúrate de que el guion incluya:\n    *   **Gancho (Hook):** Qué se verá/dirá en los primeros 3 segundos.\n    *   **Desarrollo del Contenido:** Cómo se aporta valor o entretenimiento (puntos clave, demostración, explicación, solución a un problema).\n    *   **Sugerencias Visuales:** Ideas de qué grabar o mostrar en cada segmento (ej. \"Close-up a [producto]\", \"Persona [acción]\", \"Transición rápida\").\n    *   **Texto en Pantalla/Subtítulos:** Ideas de qué texto superponer (recuerda que muchos ven sin sonido).\n    *   **Llamada a la Acción (CTA) Clara:** Qué quieres que el espectador haga al final (ej. \"Link en bio\", \"Síguenos\", \"Comenta\").\n    *   **Ejemplo de prompt:** _\"Desarrolla un guion detallado para un Reel de 30-60 segundos basado en la siguiente idea: [Pega aquí tu idea seleccionada]. Asegúrate de incluir el gancho, el desarrollo visual, sugerencias de texto en pantalla y una llamada a la acción clara.\"_\n\n5.  **Revisa y Ajusta (Tu Toque Personal):** Lee el guion generado por la IA cuidadosamente.\n    *   ¿Cumple con los 5 puntos de la \"Receta del Contenido Atractivo\"? (Gancho, Valor/Entretenimiento, Autenticidad – ¿puedes inyectar la tuya?, Brevedad/Ritmo, CTA).\n    *   ¿Evita los \"Errores Comunes\" mencionados en la lección (ignorar el gancho, ser demasiado vendedor, sin subtítulos, no tener CTA claro, perfeccionismo paralizante, dejar que la IA haga TODO)?\n    *   Añade cualquier detalle, frase o ajuste para que el guion refleje tu personalidad y el mensaje único de tu marca. Recuerda, la IA es tu copiloto, no tu reemplazo. Dale tu esencia.\n\n**Entregables:**\n\nPor favor, envía el siguiente contenido como respuesta a esta actividad. Tu entrega debe ser un documento de texto claro y organizado:\n\n1.  **Tu Producto/Servicio Seleccionado:** (Ejemplo: Velas Artesanales para la Relajación)\n2.  **Prompt Usado para Generar Ideas:** (Copia y pega el prompt exacto que utilizaste en el paso 2)\n3.  **Las Ideas de Video Generadas por la IA:** (Copia y pega las 3 a 5 ideas que te dio la IA en el paso 2)\n4.  **Tu Idea de Video Elegida:** (La que seleccionaste en el paso 3)\n5.  **Prompt Usado para Generar el Guion:** (Copia y pega el prompt exacto que utilizaste en el paso 4)\n6.  **Tu Guion de Video Final (Con tus ajustes):** (Copia y pega el guion detallado que la IA te dio y que tú revisaste/ajustaste en el paso 5. Incluye el tiempo estimado para cada sección si es posible, tal como se mostró en el ejemplo de la lección.)\n\n¡Este guion será la base para tu primera creación en video! Será el primer paso tangible para desbloquear el poder de TikTok, Reels y la IA en tu estrategia de ventas. ¡Mucho éxito!"
                }
            }
        },
        {
            "title": "Módulo 3: Creación de Contenido Irresistible con Inteligencia Artificial",
            "lesson": {
                "title": "Diseña tus Primeras Publicaciones para TikTok y Reels en Minutos con IA",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Bienvenido/a a la lección donde tus ideas de producto se convierten en contenido que engancha! Sé que pensar en qué grabar para TikTok o Reels puede parecer una montaña. ¿Qué digo? ¿Cómo lo hago para que a la gente le interese? ¿Y si no soy un experto en video?",
                            "¡Respira hondo! La buena noticia es que, en esta lección, vamos a desmitificar todo eso. Te voy a mostrar cómo, con la ayuda de la Inteligencia Artificial, puedes diseñar tus primeras publicaciones para estas plataformas virales en cuestión de minutos. Sí, has leído bien: en minutos. Olvídate de la parálisis por análisis y prepárate para ver cómo la IA se convierte en tu mejor aliada para crear contenido irresistible y empezar a mostrar tu producto al mundo."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "TikTok y Reels son el escaparate perfecto para tu producto, especialmente si es visual o si tienes una historia que contar. Pero para destacar, necesitas contenido que capte la atención en los primeros segundos, ofrezca un valor (entretener, educar, inspirar) y, por supuesto, impulse a la gente a saber más sobre lo que ofreces. Aquí es donde entra en juego la Inteligencia Artificial.",
                            "Imagina la IA como tu asistente personal de marketing. Puedes pedirle ideas, ganchos, textos, descripciones e incluso estructuras de video completas. La clave está en darle la información correcta sobre tu producto y tu público. Con esta base, la IA puede generar guiones, títulos y llamadas a la acción que resuenen con tu audiencia, todo adaptado al formato rápido y dinámico de estas plataformas.",
                            "El proceso es simple: Primero, piensa qué quieres lograr con tu video (¿vender un producto específico, generar curiosidad, mostrar un beneficio?). Luego, cuéntale a tu herramienta de IA (como ChatGPT, Gemini o Claude) sobre tu producto, tu público objetivo y tu objetivo. Finalmente, pídele que te genere ideas, guiones o ganchos. La IA te dará una base sólida que tú solo tendrás que adaptar con tu toque personal y grabar con tu móvil. ¡Es como tener un estratega de contenido 24/7!"
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Vamos a crear un guion para un producto muy popular: **Velas aromáticas artesanales y ecológicas**.",
                            "**Tu Producto:** Velas de soja artesanales, eco-friendly, con aromas relajantes (lavanda, sándalo) y envases reutilizables.",
                            "**Tu Público:** Mujeres de 25-45 años que buscan bienestar, reducir el estrés, crear un ambiente acogedor en casa y valoran los productos sostenibles.",
                            "**Tu Objetivo del Video:** Generar interés en las velas para que visiten tu perfil y, eventualmente, compren.",
                            "",
                            "**El 'Prompt' para tu IA (¡Copia y adapta!):**",
                            "\"Actúa como un experto en marketing para TikTok y Reels. Mi producto son velas de soja artesanales, eco-friendly, con aromas relajantes (lavanda, sándalo) y envases reutilizables. Mi público son mujeres de 25-45 años que buscan bienestar, reducir el estrés y productos sostenibles para su hogar. Necesito 3 ideas de videos cortos (15-30 segundos) que: 1. Capten la atención rápidamente (gancho), 2. Muestren el beneficio (relajación, ambiente, sostenibilidad), 3. Incluyan un llamado a la acción suave para ver más en mi perfil o link en bio. Para cada idea, dame un título, el gancho inicial y una descripción corta del video con los elementos visuales sugeridos y un texto para la pantalla.\"",
                            "",
                            "**Posible 'Output' de la IA (ejemplo):**",
                            "---",
                            "**Idea de Video 1: 'Tu dosis de calma diaria'**",
                            "*   **Gancho:** (Sonido de suspiro de alivio) \"¿Estrés? ¿Qué es eso?\"",
                            "*   **Descripción del Video:** Muestra rápidamente el caos del día (escritorio desordenado, tráfico), luego un cambio abrupto a una habitación tranquila, encendiendo la vela. Primer plano de la llama y el humo sutil. La persona se sienta y sonríe, respirando profundamente. Finaliza con un hermoso envase de la vela. ",
                            "*   **Texto en Pantalla:** \"Transforma tu espacio en un oasis de paz. ¡Velas de soja #EcoFriendly!\"",
                            "*   **Llamado a la Acción:** \"Encuentra tu aroma perfecto en el link de mi bio.\"",
                            "",
                            "**Idea de Video 2: 'Decora con propósito'**",
                            "*   **Gancho:** (Música moderna, rápida) \"¡Dale un 'upgrade' a tu hogar que huela bien y sienta mejor!\"",
                            "*   **Descripción del Video:** Montaje rápido mostrando cómo la vela complementa diferentes estilos de decoración: en un baño minimalista, en una mesa de centro acogedora, en una mesita de noche. Destaca el envase reutilizable. Muestra a alguien reutilizando el envase vacío (ej. como maceta pequeña o lapicero).",
                            "*   **Texto en Pantalla:** \"Estilo, aroma y sostenibilidad en una sola vela. ¡El detalle que tu hogar necesita!\"",
                            "*   **Llamado a la Acción:** \"Descubre cómo en nuestro perfil.\"",
                            "",
                            "**Idea de Video 3: 'El secreto de mis noches tranquilas'**",
                            "*   **Gancho:** (Voz en off suave) \"Antes de dormir, tengo un ritual...\"",
                            "*   **Descripción del Video:** Empieza mostrando la rutina nocturna: pijama, libro, una taza de té. Luego, la persona enciende la vela de lavanda, se relaja y cierra los ojos brevemente. La cámara se centra en la llama y el suave brillo en la oscuridad. Transición a la persona durmiendo plácidamente (sugerido, no explícito).",
                            "*   **Texto en Pantalla:** \"Rituales nocturnos para un descanso profundo. #VelasDeLavanda\"",
                            "*   **Llamado a la Acción:** \"Elige tu aroma relajante hoy. Link en bio.\"",
                            "---",
                            "¿Ves qué potente? Con estas ideas, ya tienes una base para grabar tus videos. Solo necesitas tu móvil, el producto y tu creatividad para darle vida. ¡No necesitas ser Spielberg!"
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "Para que tus primeras publicaciones sean un éxito, evita estos fallos comunes:",
                            "1.  **Ser Demasiado 'Vendedor':** Nadie quiere un anuncio directo. Ofrece valor primero: entretén, inspira, educa. Vende el beneficio, no solo el producto. En lugar de \"Compra mi vela\", di \"Relájate con el aroma de lavanda de mi vela\".",
                            "2.  **Ignorar el Gancho Inicial:** Los primeros 3 segundos son cruciales. Si no captas la atención, la gente pasará de largo. La IA es excelente para generar ganchos potentes, ¡úsalos!",
                            "3.  **No Tener un Llamado a la Acción (CTA) Claro:** ¿Qué quieres que la gente haga después de ver tu video? Visitar tu perfil, ir al link de la bio, comentar... Dilo claramente. Un CTA confuso es un CTA inútil.",
                            "4.  **Olvidar los Hashtags y la Música en Tendencia:** Son vitales para la visibilidad. Investiga cuáles son populares en tu nicho y úsalos inteligentemente. La IA también puede sugerir hashtags.",
                            "5.  **No Adaptar el Contenido de la IA:** La IA te da una base, no el resultado final. Adapta los textos a tu voz, tu personalidad y tu estilo. Hazlo tuyo.",
                            "6.  **Miedo a la Imperfección:** \"Hecho es mejor que perfecto\". No esperes tener la producción de Hollywood. Un video grabado con tu móvil, auténtico y con tu energía, conecta mucho más que algo ultraproducido pero sin alma."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "Hemos visto que diseñar tus publicaciones para TikTok y Reels no tiene por qué ser complicado. La Inteligencia Artificial es una herramienta poderosa que te ahorra tiempo y te da ideas frescas para que tu producto brille.",
                            "Recuerda los pilares: un gancho que atrape, un valor que enganche y un llamado a la acción claro que invite a interactuar. Y siempre, siempre, ¡ponle tu toque personal!",
                            "**¡Tu turno!**",
                            "Abre tu herramienta de IA preferida (ChatGPT, Gemini, Claude...). Piensa en tu producto estrella y en tu cliente ideal. Utiliza el 'prompt' de ejemplo que te di y pide 3 ideas para tus primeros Reels o TikToks. Una vez que tengas las ideas, ¡saca tu móvil y atrévete a grabar! No tiene que ser perfecto, solo tiene que ser tuyo. Cada video es un paso más cerca de tu primera venta. ¡A por ello!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: IA para TikTok y Reels",
                    "questions": [
                        {
                            "question": "Según la lección, ¿cuál es uno de los beneficios clave de usar la Inteligencia Artificial para crear publicaciones en TikTok y Reels?",
                            "options": [
                                "Garantizar que todos tus videos se conviertan en virales instantáneamente.",
                                "Eliminar completamente la necesidad de grabar videos, generando clips automáticamente.",
                                "Superar la parálisis por análisis y diseñar contenido atractivo en minutos.",
                                "Reemplazar por completo el papel del experto en marketing humano."
                            ],
                            "answer": 2,
                            "explanation": "La lección enfatiza que la IA ayuda a superar la parálisis por análisis y a diseñar publicaciones virales en cuestión de minutos, sirviendo como un asistente."
                        },
                        {
                            "question": "¿Cuál de las siguientes acciones se menciona explícitamente como un 'error común' que se debe evitar al crear contenido para TikTok y Reels?",
                            "options": [
                                "Incluir un llamado a la acción claro al final del video.",
                                "Adaptar y personalizar el contenido generado por la IA.",
                                "Ofrecer valor al público antes de intentar vender directamente.",
                                "Ser demasiado 'vendedor' y no ofrecer valor primero."
                            ],
                            "answer": 3,
                            "explanation": "La lección advierte contra ser 'demasiado vendedor' y subraya la importancia de ofrecer valor (entretener, inspirar, educar) antes de una venta directa."
                        },
                        {
                            "question": "Para obtener las ideas de contenido más efectivas de una herramienta de IA (como ChatGPT o Gemini), ¿qué información clave DEBES proporcionarle sobre tu producto y tu estrategia?",
                            "options": [
                                "El historial completo de ventas y métricas de rendimiento pasadas de tu producto.",
                                "Tu producto, tu público objetivo y el objetivo específico del video.",
                                "Los perfiles detallados de tus tres principales competidores en el mercado.",
                                "Una lista exhaustiva de todas las herramientas de edición de video que planeas usar."
                            ],
                            "answer": 1,
                            "explanation": "La lección indica que 'la clave está en darle la información correcta sobre tu producto y tu público', además de definir qué quieres lograr con el video (el objetivo)."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Genera tus Primeros Reels/TikToks con IA",
                    "type": "Text",
                    "question": "¡Es tu momento de brillar! En esta actividad, aplicarás directamente lo aprendido para convertir las ideas de tu producto en contenido atractivo para TikTok o Reels, utilizando la Inteligencia Artificial como tu asistente personal de marketing. Olvídate de la parálisis por análisis y prepárate para crear guiones que enganchen a tu audiencia.\n\n**Objetivo de la Actividad:** Utilizar una herramienta de IA para generar ideas de videos cortos (15-30 segundos) para tu propio producto, adaptarlas con tu toque personal y presentarlas como si fueran tus próximos contenidos.\n\n**Instrucciones Detalladas:**\n\n1.  **Define Tu Punto de Partida:** Antes de interactuar con la IA, clarifica los siguientes puntos sobre TU producto estrella. Esto es crucial para obtener resultados relevantes:\n    *   **Tu Producto:** Describe tu producto principal de forma concisa (ej. \"cursos de guitarra online para principiantes\", \"joyería artesanal de plata\", \"servicio de consultoría de marketing digital para pymes\").\n    *   **Tu Público Objetivo:** Describe a quién le vendes tu producto (ej. \"jóvenes adultos de 18-30 años interesados en hobbies creativos\", \"mujeres de 30-50 años que valoran la sostenibilidad y el diseño único\", \"emprendedores que buscan escalar su negocio\").\n    *   **Tu Objetivo del Video:** ¿Qué quieres lograr con este video? (ej. \"generar curiosidad para que visiten mi perfil\", \"mostrar un beneficio específico del producto\", \"impulsar la suscripción a mi newsletter\").\n\n2.  **Crea Tu 'Prompt' para la IA:** Utiliza la estructura del 'prompt' de ejemplo de la lección como base, pero adáptala con la información de TU producto, TU público y TU objetivo. Recuerda pedirle a la IA que genere:\n    *   3 ideas de videos cortos (15-30 segundos).\n    *   Para cada idea: un título, un gancho inicial, una descripción corta del video con elementos visuales sugeridos y un texto para la pantalla, y un llamado a la acción suave.\n\n    *Ejemplo de estructura de prompt a adaptar: \"Actúa como un experto en marketing para TikTok y Reels. Mi producto es [TU PRODUCTO]. Mi público son [TU PÚBLICO]. Mi objetivo es [TU OBJETIVO]. Necesito 3 ideas de videos cortos (15-30 segundos) que: 1. Capten la atención rápidamente (gancho), 2. Muestren un beneficio claro, 3. Incluyan un llamado a la acción suave para ver más en mi perfil o link en bio. Para cada idea, dame un título, el gancho inicial y una descripción corta del video con los elementos visuales sugeridos y un texto para la pantalla.\"*\n\n3.  **Genera y Adapta el Contenido con la IA:**\n    *   Abre tu herramienta de IA preferida (ChatGPT, Gemini, Claude, etc.).\n    *   Pega tu 'prompt' adaptado y genera las 3 ideas.\n    *   **¡Este es el paso clave!** Revisa las ideas que te ha dado la IA. No las copies tal cual. Adáptalas, mejora los ganchos, haz los CTAs más claros y ponles tu toque personal. Asegúrate de que evitan los errores comunes mencionados en la lección (no ser demasiado \"vendedor\", tener un gancho claro, un CTA claro, etc.). Piensa en la voz de tu marca y cómo resonaría con tu audiencia.\n\n**Entregables Concretos:**\n\nPor favor, entrega los siguientes puntos:\n\n1.  **Información de Base de Tu Producto:**\n    *   **Producto:** [Tu descripción del producto]\n    *   **Público Objetivo:** [Tu descripción del público objetivo]\n    *   **Objetivo del Video:** [Tu descripción del objetivo]\n\n2.  **El Prompt Exacto que Utilizaste para la IA:**\n    *   [Copia y pega aquí tu prompt exacto]\n\n3.  **Las 3 Ideas de Video Generadas por la IA (¡y adaptadas por ti!):**\n    *   Para cada idea, presenta el siguiente formato y, en la sección de Adaptación/Notas, menciona brevemente cómo ajustaste la idea original de la IA o qué elemento clave añadiste para hacerla más tuya y efectiva.\n\n    --- \n    **Idea de Video 1: [Título que Adaptaste]**\n    *   **Gancho:** [Tu gancho adaptado]\n    *   **Descripción del Video:** [Tu descripción adaptada con elementos visuales sugeridos]\n    *   **Texto en Pantalla:** [Tu texto adaptado para la pantalla]\n    *   **Llamado a la Acción:** [Tu CTA adaptado]\n    *   **Adaptación/Notas:** [Breve explicación de cómo mejoraste la idea o qué enfoque personal le diste].\n    \n    --- \n    **Idea de Video 2: [Título que Adaptaste]**\n    *   **Gancho:** [Tu gancho adaptado]\n    *   **Descripción del Video:** [Tu descripción adaptada con elementos visuales sugeridos]\n    *   **Texto en Pantalla:** [Tu texto adaptado para la pantalla]\n    *   **Llamado a la Acción:** [Tu CTA adaptado]\n    *   **Adaptación/Notas:** [Breve explicación de cómo mejoraste la idea o qué enfoque personal le diste].\n\n    --- \n    **Idea de Video 3: [Título que Adaptaste]**\n    *   **Gancho:** [Tu gancho adaptado]\n    *   **Descripción del Video:** [Tu descripción adaptada con elementos visuales sugeridos]\n    *   **Texto en Pantalla:** [Tu texto adaptado para la pantalla]\n    *   **Llamado a la Acción:** [Tu CTA adaptado]\n    *   **Adaptación/Notas:** [Breve explicación de cómo mejoraste la idea o qué enfoque personal le diste].\n    ---\n\n¡No te detengas ahí! Una vez que tengas estas ideas, saca tu móvil y atrévete a grabar al menos una de ellas. Recuerda: ¡Hecho es mejor que perfecto!"
                }
            }
        },
        {
            "title": "Módulo 4: WhatsApp Business: Tu Canal Directo para el Cierre de Ventas",
            "lesson": {
                "title": "Estrategias Prácticas para Convertir Interesados en Compradores por WhatsApp",
                "sections": [
                    {
                        "heading": "Introducción",
                        "paragraphs": [
                            "¡Felicidades! Has llegado a un punto clave. Ya sabes cómo captar la atención en TikTok y Reels, cómo crear contenido que resuene. Pero, ¿qué pasa cuando alguien se interesa y te escribe por WhatsApp? Ahí es donde la magia ocurre, donde un simple 'Hola, me interesa' se convierte en tu primera venta.",
                            "WhatsApp Business no es solo una app de mensajes; es tu tienda personal, tu asesor de ventas 24/7 y, sobre todo, tu canal directo para cerrar ventas. En esta lección, vamos a ver cómo pasar de tener un interesado a tener un comprador feliz, usando estrategias que cualquiera puede aplicar, sin complicaciones."
                        ]
                    },
                    {
                        "heading": "Explicación Principal",
                        "paragraphs": [
                            "Transformar un \"me interesa\" en una venta por WhatsApp es cuestión de estrategia, empatía y organización. Aquí te dejo las claves:",
                            "1. **Respuesta Rápida y Personalizada:** El tiempo es oro. Cuando alguien te escribe, responde lo antes posible. Y no uses mensajes genéricos siempre; adapta tu saludo y tu primera pregunta. Si sabes de dónde viene (ej. \"Vi tu Reel de los jabones artesanales\"), úsalo. Pregunta algo específico para entender mejor su necesidad.",
                            "2. **Escucha Activa y Solución de Dudas:** Tu cliente potencial tiene preguntas o quizás objeciones. Escucha (o lee) atentamente lo que te dice. En lugar de soltar todo tu discurso de ventas, enfócate en resolver sus dudas. Si pregunta por el precio, dáselo claramente y añade el valor que justifica ese precio. \"Cuesta X y te incluye Y, Z...\" ",
                            "3. **Usa el Catálogo de WhatsApp Business:** Si tienes varios productos, no hagas que el cliente te pregunte uno por uno. Ten tu catálogo bien configurado y envíale el enlace o los productos directamente. Esto ahorra tiempo y presenta tu oferta de forma profesional y atractiva.",
                            "4. **Ofrece Valor Extra y Opciones:** A veces, un pequeño detalle marca la diferencia. ¿Puedes ofrecer un tip de uso del producto? ¿Una pequeña guía? También, da opciones. Si vende un curso, quizás hay una versión 'básica' y otra 'premium'. Si son productos físicos, ¿diferentes tamaños, colores o packs?",
                            "5. **Cierra la Venta con un Llamado a la Acción Claro:** Una vez resueltas las dudas, es momento de guiarlo al siguiente paso. \"¿Te gustaría adquirirlo ahora?\", \"Puedes hacer el pago aquí: [enlace de pago]\" o \"Para coordinar el envío, necesito estos datos...\". Facilita el proceso al máximo.",
                            "6. **Seguimiento Amigable (¡No Intrusivo!):** Si la persona no compró de inmediato, no la presiones. Puedes hacer un seguimiento sutil al día siguiente o a los dos días. \"Hola [Nombre], ¿pudiste revisar la información que te envié? Cualquier otra duda, aquí estoy para ayudarte\". O si hubo alguna promoción, recordársela."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico",
                        "paragraphs": [
                            "Imagina que vendes \"Cursos de edición de video con IA para principiantes\" y alguien te escribe por WhatsApp después de ver tu Reel donde muestras cómo la IA puede ayudarte a editar rápidamente:",
                            "**Cliente:** \"Hola, vi tu video de edición con IA y me interesa el curso. ¿Cuánto cuesta?\"",
                            "**Tú (Respuesta Rápida y Personalizada):** \"¡Hola! Qué genial que te interese nuestro curso de edición con IA. ¿Hay algo específico que te gustaría aprender a editar o algún tipo de video en particular que hagas? Así te puedo dar la información más precisa.\"",
                            "**Cliente:** \"Pues soy nuevo en esto y me gustaría hacer videos para TikTok, pero me abruma un poco.\" ",
                            "**Tú (Escucha Activa y Catálogo):** \"¡Entiendo perfecto! Muchos empiezan así. Nuestro curso está diseñado justo para eso, para que con la ayuda de la IA, crear videos para TikTok sea fácil y rápido. Tenemos el 'Pack Básico para TikTokers' por $29.99, que incluye [Menciona 2-3 beneficios clave]. Puedes ver todos los detalles y el temario completo aquí en nuestro catálogo: [Enlace al producto en WhatsApp Business].\"",
                            "**Cliente:** \"¿Y qué herramientas de IA se usan? ¿Son difíciles?\"",
                            "**Tú (Resuelve Dudas y Ofrece Valor):** \"Usamos herramientas muy intuitivas como CapCut y algunas funciones de IA integradas. Te enseñamos desde cero cómo usarlas, ¡no necesitas experiencia previa! Además, con tu compra, te incluimos una guía rápida de '30 ideas de Reels virales' para que nunca te falte inspiración.\"",
                            "**Cliente:** \"Suena bien... ¿cómo hago para pagarlo?\"",
                            "**Tú (Llamado a la Acción Claro):** \"¡Excelente! Para inscribirte, solo tienes que hacer clic en este enlace de pago seguro: [Enlace de pago]. Una vez completado, te envío el acceso inmediato al curso y tu guía de Reels. ¿Te parece bien?\"",
                            "**Si no responde en 24h:**",
                            "**Tú (Seguimiento Amigable):** \"¡Hola [Nombre del cliente]! Solo para saber si pudiste revisar la información del curso de edición. Cualquier otra duda o si necesitas ayuda con el pago, estoy aquí para ayudarte. ¡Anímate a crear esos videos increíbles con IA! 😉\""
                        ]
                    },
                    {
                        "heading": "Errores Comunes",
                        "paragraphs": [
                            "Para que tu camino al éxito sea más directo, evita estos tropiezos:",
                            "1. **Tardar en responder:** Cada minuto cuenta. Si tardas horas, es probable que la persona haya perdido el interés o ya haya buscado otra opción.",
                            "2. **Ser un robot:** Mensajes genéricos, sin nombre, sin intentar entender la necesidad. La gente busca conectar con personas, no con bots (a menos que seas uno programado para eso, pero no es el caso aquí).",
                            "3. **Bombardear con información:** No envíes un testamento de una vez. Ve dosificando la información, respondiendo a lo que te preguntan y añadiendo valor poco a poco.",
                            "4. **No tener un llamado a la acción claro:** Una vez que el cliente está listo, no lo dejes en el aire. Dile exactamente qué hacer (clic aquí, envía tus datos, etc.).",
                            "5. **Desaparecer después del primer contacto:** Si la conversación se enfría, un seguimiento amable puede reavivar el interés. Pero, recuerda: amigable, no insistente.",
                            "6. **No usar las funciones de WhatsApp Business:** Las respuestas rápidas, el catálogo, las etiquetas para organizar contactos... ¡están ahí para ayudarte! Úsalas para ser más eficiente y profesional."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Acción",
                        "paragraphs": [
                            "WhatsApp Business es tu mejor aliado para convertir interesados en compradores. Recuerda: sé rápido, personaliza, escucha, resuelve dudas, ofrece valor y guía con claridad. Trata a cada persona como si fuera la única, y verás cómo tus ventas empiezan a despegar.",
                            "Tu misión ahora es aplicar estas estrategias. Revisa tu WhatsApp Business, configura tus respuestas rápidas, actualiza tu catálogo y, la próxima vez que te llegue un mensaje de interés, ¡pon en práctica todo lo aprendido para cerrar esa venta! ¡A por tu primera venta (o muchas más)!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz: Convierte Interesados en Compradores por WhatsApp",
                    "questions": [
                        {
                            "question": "¿Cuál es la primera y más crucial estrategia al recibir un mensaje de interés en WhatsApp?",
                            "options": [
                                "Enviar inmediatamente el enlace de pago.",
                                "Responder lo más rápido posible y de forma personalizada, preguntando algo específico.",
                                "Ignorar el mensaje hasta tener una promoción especial para ofrecer.",
                                "Enviar un mensaje genérico de bienvenida y pedir que espere."
                            ],
                            "answer": 1,
                            "explanation": "La lección enfatiza la 'Respuesta Rápida y Personalizada' como el primer paso clave para captar al cliente antes de que pierda interés o busque otras opciones."
                        },
                        {
                            "question": "¿Cuál de las siguientes acciones es un 'error común' que debes evitar al vender por WhatsApp?",
                            "options": [
                                "Utilizar el catálogo de WhatsApp Business.",
                                "Bombardear al cliente con un exceso de información de una sola vez.",
                                "Hacer un seguimiento amigable si el cliente no compra de inmediato.",
                                "Resolver las dudas del cliente antes de presentar el precio."
                            ],
                            "answer": 1,
                            "explanation": "Bombardear con información es un error común que abruma al cliente. Es mejor dosificar la información y responder a sus preguntas específicas."
                        },
                        {
                            "question": "Una vez que el cliente potencial ha resuelto sus dudas y parece interesado, ¿cuál es el siguiente paso esencial para cerrar la venta?",
                            "options": [
                                "Esperar a que el cliente solicite el método de pago.",
                                "Ofrecerle más opciones de productos o servicios.",
                                "Guiarlo con un llamado a la acción claro y facilitar el proceso de pago.",
                                "Pedirle que evalúe la conversación hasta el momento."
                            ],
                            "answer": 2,
                            "explanation": "La lección subraya la importancia de 'Cerrar la Venta con un Llamado a la Acción Claro' para guiar al cliente al siguiente paso, como un enlace de pago o solicitar datos de envío."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad Práctica: ¡Cierra esa Venta por WhatsApp!",
                    "type": "Text",
                    "question": "¡Es hora de poner en práctica tus habilidades para convertir interesados en compradores felices a través de WhatsApp Business!\n\n**Escenario:**\nImagina que has promocionado un producto o servicio tuyo (o uno ficticio) en TikTok o Reels, y un cliente potencial te escribe por WhatsApp mostrando interés. Tu objetivo es guiarlo estratégicamente hasta el cierre de la venta, aplicando todas las estrategias aprendidas en esta lección.\n\n**Parte 1: Prepara tu WhatsApp Business para el Éxito**\nSelecciona un producto o servicio específico que te gustaría vender a través de WhatsApp Business (puede ser real o ficticio, como el 'Curso de edición de video con IA para principiantes' del ejemplo). Luego, simula cómo prepararías tu cuenta de WhatsApp Business para este producto/servicio. Deberás entregar:\n\n1.  **Configuración de Perfil:** Describe brevemente cómo optimizarías la información de tu perfil de WhatsApp Business para este producto/servicio (ej. descripción de la empresa, horarios, dirección, enlace web).\n2.  **Mensaje de Bienvenida:** Redacta el mensaje de bienvenida que un nuevo contacto recibiría al escribirte. Recuerda que debe ser amigable y personalizado.\n3.  **Respuestas Rápidas Clave:** Crea 3 respuestas rápidas (`/precio`, `/beneficios`, `/comprar`) para las preguntas o situaciones más comunes que podrías enfrentar con este producto/servicio. Escribe el texto completo de cada una.\n4.  **Producto en Catálogo:** Describe el producto/servicio principal que ofrecerías en tu catálogo de WhatsApp Business. Menciona su nombre, precio, una breve descripción y 2-3 beneficios clave. Si puedes, adjunta una captura de pantalla de cómo se vería en tu catálogo (si tienes uno real configurado, ¡mucho mejor!).\n\n**Parte 2: Simula tu Conversación de Venta Estelar**\nAhora, escribe una simulación de conversación completa entre tú (el vendedor) y el cliente potencial, aplicando todas las estrategias de cierre de ventas de la lección. La conversación debe:\n\n*   **Iniciar con un mensaje del cliente:** \"Hola, vi tu [menciona dónde lo vio: Reel/TikTok/historia] y me interesa tu [nombre del producto/servicio de la Parte 1]. ¿Cuánto cuesta?\"\n*   **Aplicar las 6 claves de la lección:**\n    1.  **Respuesta Rápida y Personalizada:** Tu primera respuesta debe reflejar esto.\n    2.  **Escucha Activa y Solución de Dudas:** Responde a las preguntas del cliente y anticipa posibles objeciones.\n    3.  **Uso del Catálogo de WhatsApp Business:** Haz referencia al producto/servicio de la Parte 1 y, si aplica, envía el enlace directo a tu catálogo o al producto.\n    4.  **Ofrece Valor Extra y Opciones:** Propón un pequeño detalle adicional o diferentes versiones del producto/servicio.\n    5.  **Cierre de Venta con Llamado a la Acción Claro:** Guía al cliente de forma inequívoca al siguiente paso (ej. enlace de pago, solicitud de datos).\n    6.  **Seguimiento Amigable (¡No Intrusivo!):** Incluye un posible mensaje de seguimiento si el cliente no compra de inmediato, pero muestra interés inicial.\n\n**Entregable:**\nUn documento de texto o PDF que incluya:\n*   Las descripciones y textos de la Parte 1 (configuración del perfil, mensaje de bienvenida, 3 respuestas rápidas, descripción del producto del catálogo y captura de pantalla opcional).\n*   La simulación completa de la conversación de venta de la Parte 2, donde se puedan identificar claramente la aplicación de las 6 claves."
                }
            }
        },
        {
            "title": "Módulo 5: Tu Primera Venta Online: Estrategia de Lanzamiento y Éxito",
            "lesson": {
                "title": "Lanza, Vende y Celebra: Ejecuta tu Estrategia y Consigue tu Primera Venta",
                "sections": [
                    {
                        "heading": "Introducción: ¡El Momento de la Verdad ha Llegado!",
                        "paragraphs": [
                            "¡Felicidades! Has llegado al módulo final, y eso significa que estás a punto de transformar toda la estrategia, el conocimiento y las herramientas que hemos construido juntos en una realidad tangible: tu primera venta online. Este no es solo un paso más, es EL paso. Es el momento de dejar de planificar y empezar a ejecutar, de sembrar y de recoger.",
                            "Hemos preparado el terreno, diseñado tu producto (o servicio), identificado a tu público ideal, creado contenido atractivo con la ayuda de la Inteligencia Artificial y configurado tu canal de ventas por WhatsApp. Ahora, es tiempo de unirte a la acción, lanzar tu mensaje al mundo y hacer que suceda. Prepárate para no solo vender, sino también para celebrar cada pequeño logro en el camino."
                        ]
                    },
                    {
                        "heading": "Lanza, Vende y Celebra: El Paso a Paso para Tu Primera Venta",
                        "paragraphs": [
                            "Aquí es donde todo se une. Tu estrategia está lista, ahora vamos a ponerla en marcha. Recuerda, la clave es la acción, la interacción y la claridad en cada paso. No busques la perfección, busca el progreso.",
                            "**1. ¡A Publicar con Confianza!**: Sube a TikTok y Reels esos videos y contenidos que ya preparaste. No te quedes pegado en '¿será perfecto?'. La IA ya te ayudó a crear textos y guiones geniales, solo necesitas publicarlos. Usa los hashtags relevantes y la música en tendencia para aumentar tu visibilidad.",
                            "**2. Activa la Interacción: Responde y Conecta**: Una vez que tus publicaciones estén online, tu trabajo no termina. Estate atento a los comentarios y mensajes directos. Cada 'me gusta', cada comentario es una oportunidad para conectar. Responde de forma genuina, agradece y, si hay interés en tu producto, guía a esa persona hacia el siguiente paso.",
                            "**3. Tu Call to Action (CTA) es el Puente a WhatsApp**: Este es CRUCIAL. Tus publicaciones deben tener una llamada a la acción súper clara. Por ejemplo: \"Link en mi biografía para más información\", \"Manda un DM si quieres el tuyo\", \"Escríbeme por WhatsApp para ver todos los detalles (link en mi perfil)\". Haz que sea lo más fácil posible para tu potencial cliente saber qué hacer después.",
                            "**4. El Cierre de Venta en WhatsApp: La Conversación que Convierte**: Una vez que la gente llega a tu WhatsApp, es tu momento de brillar. Sé amable, atento y resuelve todas sus dudas. Reitera los beneficios de tu producto, cómo les ayudará a resolver su problema o a mejorar su vida. Pregunta qué les gustaría saber, qué les preocupa. Ofrece opciones de pago claras y sencillas. Tu objetivo es hacer que se sientan cómodos y seguros al comprar.",
                            "**5. ¡Celebra Tu Primera Venta!**: Cuando veas esa notificación de pago, o recibas la confirmación de tu primera transacción, tómate un momento. ¡Celébralo! Es un hito enorme. Has demostrado que puedes hacerlo. Cada experto, cada gran empresa, empezó con una primera venta. Este es el inicio de tu camino como emprendedor online."
                        ]
                    },
                    {
                        "heading": "Ejemplo Práctico: Vendiendo tu 'Kit de Estudio Minimalista'",
                        "paragraphs": [
                            "Imagina que vendes un 'Kit de Estudio Minimalista' (un producto digital con plantillas, guías y audios para mejorar la concentración) y tu público son estudiantes universitarios. Así se vería tu lanzamiento:",
                            "**Contenido (TikTok/Reels)**: Publicas un video corto que creaste con ayuda de IA, mostrando \"Un día en mi vida con mi Kit de Estudio Minimalista\" – ves a un estudiante estresado transformarse en uno concentrado y tranquilo usando tus herramientas. El texto en pantalla dice: \"¿Estrés en épocas de exámenes? Descomplica tu estudio\". La voz en off (generada por IA) dice: \"Haz clic en el link de mi perfil para descubrir cómo\".",
                            "**Interacción**: Alguien comenta: \"¡Lo necesito! ¿Cómo funciona?\".",
                            "**Tu Respuesta**: \"¡Claro que sí! Es perfecto para simplificar tu vida académica. Te envié un DM con el link directo a mi WhatsApp para darte todos los detalles y resolver cualquier duda que tengas. ¡Te espero!\".",
                            "**En WhatsApp**: El estudiante te escribe. Le saludas: \"¡Hola [Nombre del Estudiante]! Gracias por tu interés en el Kit de Estudio Minimalista. Te cuento que incluye... (describes los beneficios principales). Cuesta X dólares y puedes pagar con [métodos de pago]. ¿Tienes alguna pregunta o te gustaría empezar hoy mismo?\".",
                            "El estudiante pregunta si incluye técnicas para procrastinación. Le respondes cómo el kit ayuda directamente con eso. Ofreces un pequeño bonus (un checklist imprimible extra) si compra hoy. Finalmente, te dice: \"¡Me lo quedo!\". Le envías el link de pago y las instrucciones. ¡Y listo! ¡Tu primera venta está hecha!"
                        ]
                    },
                    {
                        "heading": "Errores Comunes a Evitar: No Te Tropieces en la Recta Final",
                        "paragraphs": [
                            "Para que tu camino sea lo más fluido posible, ten en cuenta estos errores comunes que muchos principiantes cometen:",
                            "**1. El Síndrome del Perfeccionista**: Querer que el contenido sea 100% perfecto antes de publicarlo. Recuerda, lo bueno es mejor que lo perfecto (y no hecho). Tus primeros contenidos serán tus maestros.",
                            "**2. Publicar y Desaparecer**: No interactuar con los comentarios o mensajes directos. El engagement es tu combustible para las ventas. Sin interacción, no hay conexión, y sin conexión, no hay confianza.",
                            "**3. CTA Confuso o Inexistente**: Si la gente no sabe qué hacer después de ver tu contenido, no hará nada. Sé explícito sobre el siguiente paso: \"Link en bio\", \"DM para info\", \"Escríbeme al WhatsApp\".",
                            "**4. Proceso de Compra Complicado**: En WhatsApp, haz que la información sea clara y los pasos para pagar sean sencillos. Demasiados clics o preguntas innecesarias pueden frustrar al comprador y hacer que abandone.",
                            "**5. Desanimarse por la Inmediatez**: Tu primera venta puede no llegar al minuto de publicar. Es normal. Sé constante, sigue publicando, interactuando y ajustando tu mensaje. La persistencia es clave. Cada \"no\" te acerca a un \"sí\"."
                        ]
                    },
                    {
                        "heading": "Mini Resumen y Tu Próxima Gran Acción",
                        "paragraphs": [
                            "Hemos llegado al final de este camino, pero es solo el comienzo del tuyo. Recuerda: la clave para tu primera venta online es la **acción constante**, la **interacción genuina** y una **claridad impecable** en tu proceso de venta. Ya tienes todas las herramientas, desde la estrategia de contenido hasta el uso inteligente de la IA, y sabes cómo cerrar una venta.",
                            "Tu tarea final (y la más emocionante) es: **¡Lanza tus contenidos, interactúa con cada persona interesada, guía a tus clientes potenciales a WhatsApp y cierra tu primera venta!** No subestimes el poder de ese primer logro. Es la prueba de que tu idea tiene valor, de que tu esfuerzo da frutos, y el impulso que necesitas para seguir construyendo tu pequeño negocio. Estamos ansiosos por celebrar contigo este gran paso. ¡Ve a por ello!"
                        ]
                    }
                ],
                "quiz": {
                    "title": "Quiz del Módulo: Tu Primera Venta Online",
                    "questions": [
                        {
                            "question": "¿Cuál es el primer paso esencial que la lección indica para tu primera venta online, después de haber preparado el contenido con ayuda de IA?",
                            "options": [
                                "Publicar con confianza en plataformas como TikTok y Reels, sin buscar la perfección.",
                                "Realizar una investigación de mercado final para asegurar la viabilidad del producto.",
                                "Crear una landing page profesional antes de mostrar cualquier contenido.",
                                "Esperar a tener al menos 1000 seguidores para garantizar visibilidad."
                            ],
                            "answer": 0,
                            "explanation": "La lección enfatiza que el primer paso es '¡A Publicar con Confianza!' en plataformas como TikTok y Reels, priorizando la acción sobre la perfección."
                        },
                        {
                            "question": "¿Cuál es la función CRUCIAL de un Call to Action (CTA) efectivo en el proceso de venta, según la lección?",
                            "options": [
                                "Servir como el puente claro que guía al potencial cliente desde tu publicación hasta el siguiente paso (ej. WhatsApp).",
                                "Describir de forma exhaustiva todos los beneficios del producto en un solo mensaje.",
                                "Generar debates y controversia en los comentarios para aumentar la visibilidad.",
                                "Solicitar directamente el pago antes de cualquier interacción personalizada."
                            ],
                            "answer": 0,
                            "explanation": "El CTA es 'CRUCIAL' porque funciona como el puente que indica al potencial cliente qué hacer a continuación, facilitando la transición a la conversación de venta, por ejemplo, en WhatsApp."
                        },
                        {
                            "question": "¿Cuál de los siguientes es un error común que la lección advierte específicamente que debes evitar al buscar tu primera venta?",
                            "options": [
                                "No interactuar con los comentarios o mensajes directos de tus publicaciones.",
                                "Celebrar cada pequeña venta y logro en el camino.",
                                "Ofrecer opciones de pago claras y sencillas a tus clientes.",
                                "Usar hashtags relevantes y música en tendencia para aumentar la visibilidad."
                            ],
                            "answer": 0,
                            "explanation": "La lección destaca que 'Publicar y Desaparecer' (no interactuar con comentarios o DMs) es un error común que obstaculiza las ventas, ya que 'el engagement es tu combustible'."
                        }
                    ]
                },
                "assignment": {
                    "title": "Actividad: Tu Primera Venta Online - ¡Acción!",
                    "type": "Text",
                    "question": "¡Felicidades! Has llegado al momento más emocionante: poner en práctica todo lo aprendido para conseguir tu primera venta online. Esta actividad está diseñada para que des el paso final y ejecutes tu estrategia de lanzamiento. Recuerda, la acción es la clave, no la perfección.\n\n**Tu Misión:** Lanza tus contenidos, interactúa con tus potenciales clientes y guía el proceso hasta el cierre de tu primera venta (¡o al menos hasta generar conversaciones de alto valor!).\n\n**Instrucciones y Entregables:**\n\n1.  **Lanzamiento de Contenido (TikTok/Reels):**\n    *   **Acción:** Publica al menos **dos (2)** videos o Reels en tu plataforma elegida (TikTok, Instagram Reels) utilizando el contenido y las ideas que has preparado con ayuda de la IA. Asegúrate de incluir hashtags relevantes y música en tendencia.\n    *   **Entregable:** Proporciona los **enlaces directos (URLs)** a tus dos publicaciones o **dos capturas de pantalla** que demuestren que el contenido ha sido publicado exitosamente. Asegúrate de que se vean las publicaciones y la fecha de publicación (si es visible).\n\n2.  **Definición de Tu Call to Action (CTA):**\n    *   **Acción:** Revisa que tus publicaciones y tu perfil tengan una llamada a la acción clara que guíe a los interesados hacia tu WhatsApp.\n    *   **Entregable:** Describe de forma explícita cuál es tu **CTA principal** y dónde está ubicada (ej. \"Link en bio para más detalles\", \"Envía un DM con la palabra 'QUIERO'\", \"Haz clic en el enlace de mi perfil que te lleva directo a WhatsApp\").\n\n3.  **Estrategia de Interacción y Cierre en WhatsApp:**\n    *   **Acción:** Prepara cómo manejarás las interacciones. Una vez que la gente empiece a comentar o llegue a tu WhatsApp, tu respuesta es crucial.\n    *   **Entregable:**\n        *   **Plan de Interacción:** Describe brevemente cómo planeas responder a los comentarios/mensajes directos iniciales en tus redes sociales para guiar a los interesados a WhatsApp.\n        *   **Guion de Conversación en WhatsApp:** Diseña un breve **guion o flujo de conversación** que utilizarías una vez que un potencial cliente te contacta por WhatsApp. Incluye:\n            *   Un saludo inicial.\n            *   Cómo presentarías los beneficios clave de tu producto/servicio.\n            *   Cómo responderías a una pregunta común sobre tu oferta.\n            *   Cómo harías el llamado al pago (métodos, precio, etc.).\n            *   Menciona cómo manejarías una objeción común (ej. \"es muy caro\", \"no estoy seguro\").\n\n4.  **Evidencia de Interacción (Opcional, pero muy recomendado):**\n    *   **Acción:** Si ya has recibido comentarios, DMs o mensajes en WhatsApp, interactúa activamente con ellos.\n    *   **Entregable (Opcional):** Una **captura de pantalla** de una interacción real (comentario respondido, DM enviado, parte de una conversación en WhatsApp). Si no has tenido interacciones aún, no te preocupes, el objetivo es el lanzamiento y la preparación. Puedes simplemente indicarlo.\n\n5.  **Reflexión y Próximos Pasos:**\n    *   **Acción:** Reflexiona sobre el proceso de lanzamiento inicial.\n    *   **Entregable:** Escribe un breve párrafo (50-100 palabras) sobre:\n        *   ¿Qué fue lo más desafiante de esta fase de lanzamiento?\n        *   ¿Qué aprendiste o qué te sorprendió?\n        *   ¿Qué ajustes planeas hacer en tus contenidos o en tu estrategia de interacción para las próximas semanas?\n\n**El objetivo principal de esta actividad es que te atrevas a lanzar y aprendas de la experiencia. ¡Cada intento te acerca más a tu primera venta!**"
                }
            }
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Primera Venta Online con TikTok, Reels y WhatsApp usando IA",
        "type": "Document",
        "question": "¡Felicidades! Has llegado al proyecto final de 'Vende tu primer producto por TikTok, Reels y WhatsApp usando IA'. Este proyecto es tu oportunidad de aplicar todo lo aprendido para conseguir tu primera venta online.\n\nEl objetivo es que demuestres tu capacidad para diseñar, crear y ejecutar una estrategia de venta práctica para un producto real (físico o digital), apoyándote en la Inteligencia Artificial para optimizar tu tiempo y creatividad. Prepárate para transformar tu idea en una venta tangible y celebrar tu primera transacción.\n\n**Paso a paso detallado para entregar el proyecto final:**\n\n**FASE 1: Planificación y Estrategia (Documento de Concepto)**\n\n1.  **Definición del Producto y Público Objetivo:**\n    *   **Producto:** Elige un producto (físico o digital) que tengas o que te interese mucho vender. Descríbelo brevemente (nombre, qué es, beneficios clave, precio de venta).\n    *   **Público Objetivo:** Define a tu cliente ideal. ¿Quién es? (Edad, intereses, dónde pasa su tiempo online, especialmente en TikTok/Instagram). ¿Qué problema o necesidad resuelve tu producto para ellos?\n\n2.  **Estrategia de Contenido para TikTok/Reels (Asistida por IA):**\n    *   **Brainstorming con IA:** Utiliza una herramienta de IA (ej. ChatGPT, Google Gemini, Copilot) para generar al menos **5 ideas de contenido** (hooks, llamados a la acción, formatos de video, temas de conversación) que sean atractivas para tu público objetivo y promocionen tu producto. Incluye el prompt que usaste.\n    *   **Selección y Guion/Outline Detallado:** Elige las **2 mejores ideas** de tu brainstorming. Para cada una, crea un guion corto o un outline detallado (incluyendo texto en pantalla, acciones visuales, audio o música recomendado, duración estimada de 15-30 segundos). **Indica claramente qué partes del guion/outline fueron generadas o asistidas por la IA.**\n    *   **Llamada a la Acción (CTA) para Redes:** Define cómo dirigirás a los interesados desde TikTok/Reels hacia WhatsApp (ej. “Link en la bio”, “Envía DM con la palabra [PRODUCTO]”, “Manda un WhatsApp al número [TU NÚMERO]”).\n\n3.  **Diseño del Flujo de Venta por WhatsApp (Asistido por IA):**\n    *   **Mensaje de Bienvenida Automatizado:** Crea el primer mensaje que recibirá un cliente potencial al contactarte por WhatsApp. Debe ser amable, confirmar su interés en el producto y pedir información clave si es necesario (ej. nombre, ubicación).\n    *   **Preguntas Frecuentes (FAQ) con IA:** Utiliza una herramienta de IA para generar al menos **3 preguntas frecuentes** que tu cliente ideal podría tener sobre tu producto, junto con sus **respuestas concisas y persuasivas**. Incluye el prompt que usaste.\n    *   **Cierre de Venta y CTA en WhatsApp:** Diseña una frase de cierre y una llamada a la acción clara para finalizar la venta (ej. “¿Listo para ordenar? Haz clic aquí para pagar”, “Confirma tu pedido y te enviamos los datos de pago”).\n\n**FASE 2: Creación y Simulación (Evidencia Audiovisual y Conversacional)**\n\n1.  **Creación de Contenido para TikTok/Reels:**\n    *   **Video 1:** Graba y edita un video corto (15-30 segundos) siguiendo uno de los guiones/outlines que diseñaste en la Fase 1, punto 2.b. (Puedes usar tu teléfono; no se requieren equipos profesionales). Súbelo a tu perfil de TikTok o Instagram Reels (puedes configurarlo como privado o para “solo yo”, pero debe ser accesible vía enlace para la evaluación). Asegúrate de que el video contenga el CTA definido.\n    *   **Video 2:** Graba y edita otro video corto (15-30 segundos) siguiendo el segundo guion/outline. Súbelo de la misma forma que el Video 1, incluyendo su respectivo CTA.\n\n2.  **Simulación de Interacción por WhatsApp:**\n    *   **Conversación Simulada:** Simula una conversación completa con un cliente potencial en WhatsApp (puedes pedirle a un amigo que te ayude o usar dos números tuyos). La conversación debe mostrar:\n        *   Tu mensaje de bienvenida.\n        *   Al menos 2 intercambios donde respondas a las preguntas frecuentes que generaste con IA.\n        *   Tu frase de cierre de venta y el llamado a la acción final.\n    *   **Evidencia:** Toma capturas de pantalla de esta conversación simulada completa. Asegúrate de que se vea el flujo de la interacción.\n\n**Entregables:**\n\nDeberás consolidar toda la información y las evidencias en un único documento digital (ej. Google Docs, Microsoft Word, PDF, o una página de Notion/Miro/Trello) que incluya claramente los siguientes apartados:\n\n1.  **Documento de Planificación (Contenido de la Fase 1):**\n    *   Descripción del Producto y Público Objetivo.\n    *   Los 5 prompts y las ideas de contenido generadas por IA.\n    *   Los 2 guiones/outlines para videos (señalando el aporte de la IA).\n    *   La estrategia de CTA para redes sociales.\n    *   El mensaje de bienvenida de WhatsApp.\n    *   Los 3 prompts y las FAQ con respuestas generadas por IA.\n    *   La frase de cierre de venta y CTA de WhatsApp.\n\n2.  **Enlaces a Videos (Evidencia de Fase 2.1):**\n    *   Enlace accesible al Video 1 (TikTok/Reels).\n    *   Enlace accesible al Video 2 (TikTok/Reels).\n\n3.  **Evidencia de WhatsApp (Evidencia de Fase 2.2):**\n    *   Las capturas de pantalla de la conversación simulada por WhatsApp, que muestren el flujo completo de venta.\n\n**Criterios de Evaluación (por IA):**\n\nTu proyecto será evaluado en base a los siguientes puntos:\n\n*   **Claridad y Coherencia:** El plan de producto, público y estrategia de contenido debe ser lógico y alineado.\n*   **Uso Evidente de IA:** Se demuestra el uso de IA para generar ideas, guiones, prompts y FAQs, y se especifica su contribución.\n*   **Practicidad y Orientación a la Venta:** Los guiones, mensajes de WhatsApp y CTAs son directos, persuasivos y orientados a generar una venta.\n*   **Calidad del Contenido Audiovisual:** Los videos son creados y accesibles, y siguen la estrategia y guiones definidos (no se evalúa producción profesional, sino la ejecución de la idea).\n*   **Flujo de Venta en WhatsApp:** La simulación de conversación muestra un proceso de venta claro, completo y persuasivo desde el primer contacto hasta el cierre.\n*   **Completitud de Entregables:** Todos los puntos y evidencias solicitados han sido incluidos en el documento final."
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
    return frappe.db.get_value(doctype, filters, "name")

def create_or_update_category(category_name):
    name = get_existing_name("LMS Category", {"category": category_name})
    if name:
        return name
    doc = frappe.get_doc({
        "doctype": "LMS Category",
        "category": category_name
    })
    doc.insert(ignore_permissions=True)
    return doc.name

def add_instructor_if_missing(course_name, instructor_name):
    doc = frappe.get_doc("LMS Course", course_name)
    has_instructor = any(i.instructor == instructor_name for i in doc.get("instructors", []))
    if not has_instructor:
        try:
            doc.append("instructors", {"instructor": instructor_name})
            doc.save(ignore_permissions=True)
        except Exception:
            pass

def create_or_update_course(course_data, category_name):
    name = get_existing_name("LMS Course", {"title": course_data["title"]})
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
    
    doc.save(ignore_permissions=True)
    add_instructor_if_missing(doc.name, INSTRUCTOR_NAME)
    return doc.name

def create_or_update_assignment(assignment_data, course_name):
    name = get_existing_name("LMS Assignment", {"title": assignment_data["title"], "course": course_name})
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
    name = get_existing_name("LMS Question", {"question": question_data["question"]})
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
    name = get_existing_name("LMS Quiz", {"title": quiz_data["title"], "course": course_name})
    if name:
        doc = frappe.get_doc("LMS Quiz", name)
        doc.set("questions", [])
    else:
        doc = frappe.new_doc("LMS Quiz")
        doc.title = quiz_data["title"]
        doc.course = course_name
        
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
    name = get_existing_name("Course Lesson", {"title": lesson_data["title"], "chapter": chapter_name})
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
    name = get_existing_name("Course Chapter", {"title": chapter_data["title"], "course": course_name})
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
