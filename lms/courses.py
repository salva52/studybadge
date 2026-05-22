import os
import sys
import json
import frappe

# Ajuste de rutas para ejecución directa
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)
apps_dir = os.path.abspath(os.path.join(script_dir, ".."))
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

def get_courses_data():
    """
    Retorna la estructura de los 10 cursos.
    Cada curso contiene módulos, lecciones y un mínimo de 10 asignaciones en total.
    """
    return [
        {
            "title": "Trading Institucional y Pruebas de Fondeo",
            "category": "Finanzas y Trading",
            "short_intro": "Domina la acción del precio y prepara tu psicología para pasar un prop firm challenge de $15,000.",
            "description": "<p>Aprende trading desde cero. Nos enfocaremos en EUR/USD, gestión de riesgo y estructura de mercado para que logres tu cuenta fondeada.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Fundamentos y Acción del Precio",
                    "lessons": [
                        {
                            "title": "1. Estructura de Mercado Básica",
                            "body": "### Entendiendo la Tendencia\nEl mercado se mueve en impulsos y retrocesos. Para operar EUR/USD, debes identificar los altos más altos (HH) y bajos más altos (HL) en temporalidades mayores. No operes en contra de la estructura diaria.\n\nAplicar esto te evitará el 80% de las pérdidas en cuentas de fondeo.",
                            "assignments": [
                                {"title": "Identificar Tendencia Diaria", "type": "Document", "question": "Sube una captura de TradingView del EUR/USD en gráfico diario marcando 3 impulsos y retrocesos."},
                                {"title": "Zonas de Oferta y Demanda", "type": "Document", "question": "Marca 2 zonas de oferta y 2 de demanda en temporalidad de 1H y sube la imagen."}
                            ]
                        },
                        {
                            "title": "2. Gestión de Riesgo para FundedNext",
                            "body": "### Matemáticas del Trading\nSi arriesgas el 1% por trade en una cuenta de $15,000, tu riesgo es de $150. Las firmas de fondeo penalizan el drawdown diario. Tu objetivo inicial no es hacer dinero, es proteger el capital para no perder la prueba.",
                            "assignments": [
                                {"title": "Plan de Riesgo", "type": "Text", "question": "Escribe tu regla de pérdida máxima diaria y semanal. ¿Cuántos trades perdedores seguidos te obligan a parar?"},
                                {"title": "Calculadora de Lotes", "type": "URL", "question": "Pega el enlace a una calculadora de tamaño de posición que vayas a usar."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Operativa y Psicología",
                    "lessons": [
                        {
                            "title": "3. Ejecución y Entradas",
                            "body": "### El Gatillo\nUna vez el precio llega a tu zona, no entras a ciegas. Esperas un cambio de carácter (ChoCh) en temporalidades menores (5m o 1m). Esto reduce tu stop loss y aumenta tu ratio riesgo/beneficio.",
                            "assignments": [
                                {"title": "Backtesting de Entradas", "type": "Document", "question": "Sube un PDF con 3 ejemplos de backtesting mostrando la confirmación en 5 minutos."},
                                {"title": "Diario Emocional", "type": "Text", "question": "Describe qué emociones sentiste en tu última operación (demo o real) y cómo las gestionaste."},
                                {"title": "Checklist de Entrada", "type": "Text", "question": "Crea una lista de 5 pasos que el mercado debe cumplir antes de que presiones 'Comprar' o 'Vender'."}
                            ]
                        },
                        {
                            "title": "4. Preparación para el Challenge",
                            "body": "### Fases de la Prueba\nRecuerda que la Fase 1 suele requerir un 8% de profit, mientras la Fase 2 pide un 5%. La paciencia es clave. No intentes pasar la prueba en un día.",
                            "assignments": [
                                {"title": "Elección de Prop Firm", "type": "URL", "question": "Pega el enlace a las reglas oficiales del challenge que planeas tomar."},
                                {"title": "Proyección de Ratio", "type": "Text", "question": "Si tu Win Rate es del 40% y tu RR es 1:3, ¿cuántos trades necesitas para alcanzar un 8%? Haz el cálculo."},
                                {"title": "Reglas de Drawdown", "type": "Text", "question": "Explica con tus palabras la diferencia entre drawdown estático y trailing drawdown según la firma elegida."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Desarrollo Avanzado y Scripting en Roblox",
            "category": "Programación y Videojuegos",
            "short_intro": "Crea mecánicas complejas, diseña GUIs profesionales y organiza tu código como un desarrollador top en Roblox Studio.",
            "description": "<p>Desde el modelado de assets hasta la correcta arquitectura de scripts cliente-servidor.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Interfaz y Client-Side",
                    "lessons": [
                        {
                            "title": "1. Arquitectura de Interfaces",
                            "body": "### Organización de GUIs\nUn error común es colocar lógica pesada directamente en StarterGui. Para un código limpio y eficiente, los scripts locales que manejan la interfaz principal deben ubicarse en `starterplayerscripts`. Esto asegura que el código se cargue correctamente cuando el jugador entra al juego y facilita la comunicación con módulos.",
                            "assignments": [
                                {"title": "Estructura de Carpetas", "type": "Document", "question": "Sube una captura de tu Explorer en Roblox Studio mostrando tu GUI y tu LocalScript en starterplayerscripts."},
                                {"title": "Diseño de Menú Principal", "type": "URL", "question": "Sube tu diseño de UI (puede ser Figma o un screenshot de Studio) con botones de 'Jugar' y 'Tienda'."},
                                {"title": "Animación de Botones", "type": "Text", "question": "Pega el código usando TweenService para hacer que un botón crezca ligeramente al pasar el mouse (MouseEnter)."}
                            ]
                        },
                        {
                            "title": "2. Modelado y Assets",
                            "body": "### Optimización de Mallas\nAl importar mallas desde Blender, cuida el número de triángulos. Un juego lleno de assets pesados causará lag en dispositivos móviles.",
                            "assignments": [
                                {"title": "Modelado Low-Poly", "type": "Document", "question": "Sube una imagen de un prop (ej. una caja o un arma) modelado en estilo low-poly."},
                                {"title": "Importación a Studio", "type": "Text", "question": "Explica brevemente la diferencia entre SurfaceAppearance y un MaterialVariant."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Servidor y Seguridad",
                    "lessons": [
                        {
                            "title": "3. RemoteEvents y Seguridad",
                            "body": "### Confía Cero en el Cliente\nNunca confíes en el LocalScript para decisiones importantes como sumar dinero o hacer daño. El cliente debe enviar un RemoteEvent al servidor, y es el servidor (ServerScriptService) quien valida y ejecuta la acción.",
                            "assignments": [
                                {"title": "Creación de RemoteEvent", "type": "Text", "question": "Escribe el fragmento de código donde el cliente dispara un RemoteEvent llamado 'ComprarItem'."},
                                {"title": "Validación en el Servidor", "type": "Text", "question": "Escribe el código del lado del servidor que recibe el evento y verifica si el jugador tiene suficientes monedas."},
                                {"title": "Prevención de Exploits", "type": "Text", "question": "Explica 2 métodos comunes que usan los exploiters y cómo tus comprobaciones en el servidor los bloquean."}
                            ]
                        },
                        {
                            "title": "4. DataStore y Guardado",
                            "body": "### Persistencia de Datos\nUsaremos DataStoreService para guardar el progreso. Siempre usa pcalls (protected calls) al guardar o cargar datos, ya que las peticiones a la API de Roblox pueden fallar.",
                            "assignments": [
                                {"title": "Configuración de DataStore", "type": "Text", "question": "Pega el código de tu función de PlayerAdded que carga los datos del jugador."},
                                {"title": "Manejo de Errores", "type": "Text", "question": "Escribe cómo manejas un error si el DataStore falla (ej. reintentos o mensajes al usuario)."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Composición de Trap y Reggaetón",
            "category": "Música y Arte",
            "short_intro": "Aprende a estructurar tus barras, crear flujos pegadizos y escribir letras que conecten.",
            "description": "<p>Domina la métrica, las referencias culturales y la estructura estándar de la música urbana moderna.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Estructura y Métrica",
                    "lessons": [
                        {
                            "title": "1. La Arquitectura del Hit",
                            "body": "### Ordenando el Caos\nUna canción urbana necesita estructura. Para mantener el interés, usa etiquetas claras al escribir. Etiqueta tus bloques con `#VERSE` para los versos narrativos y `#CHORUS` para el estribillo principal. El estribillo debe ser la parte más memorable y repetitiva.",
                            "assignments": [
                                {"title": "Estructura Base", "type": "Text", "question": "Escribe la estructura de tu próxima canción usando las etiquetas #INTRO, #VERSE, #PRECHORUS, #CHORUS y #OUTRO."},
                                {"title": "Creación del Estribillo", "type": "Text", "question": "Escribe un #CHORUS de 4 líneas enfocado en un concepto de superación o lujo."},
                                {"title": "Análisis de Referencia", "type": "URL", "question": "Pega el link de YouTube de tu canción urbana favorita y anota los minutos exactos donde entra el #CHORUS."}
                            ]
                        },
                        {
                            "title": "2. Métrica y Delivery",
                            "body": "### El Flow es el Rey\nNo importa qué tan buena sea la letra si no encaja en el beat. Cuenta las sílabas. Mantén una longitud consistente en tus barras de Trap para que el delivery suene contundente y natural.",
                            "assignments": [
                                {"title": "Conteo de Sílabas", "type": "Text", "question": "Escribe 2 líneas de barra (punchlines) y asegúrate de que ambas tengan la misma cantidad de sílabas. Anota el número."},
                                {"title": "Cambio de Flow", "type": "Text", "question": "Escribe un #VERSE de 8 líneas donde las primeras 4 tengan un ritmo lento y las últimas 4 usen doble tempo."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Temática y Branding",
                    "lessons": [
                        {
                            "title": "3. Barras y Referencias",
                            "body": "### Códigos Culturales\nEl Trap y Reggaetón se alimentan de referencias a marcas, lugares (ej. Daikoku), deportes o autos. Estas referencias conectan con el estilo de vida que el oyente aspira a tener.",
                            "assignments": [
                                {"title": "Lluvia de Referencias", "type": "Text", "question": "Haz una lista de 5 marcas, 2 lugares icónicos y 2 deportistas que encajen con tu identidad artística."},
                                {"title": "Punchlines con Marcas", "type": "Text", "question": "Escribe 2 barras que utilicen de forma inteligente una de las marcas que listaste antes."},
                                {"title": "El Outro", "type": "Text", "question": "Escribe un #OUTRO que despida la canción bajando la energía progresivamente."}
                            ]
                        },
                        {
                            "title": "4. Grabación y Producción Vocal",
                            "body": "### Actitud en el Micrófono\nTu estado de ánimo se transmite en la toma. Antes de grabar, asegúrate de tener la pista de acompañamiento lista y tus ad-libs (voces de fondo) planificados.",
                            "assignments": [
                                {"title": "Guía de Ad-libs", "type": "Text", "question": "Toma un #VERSE que hayas escrito y anota entre paréntesis qué sonidos o palabras usarás de fondo (ej. '¡Skrrt!', '¡Yeah!')."},
                                {"title": "Demo Vocal", "type": "Document", "question": "Graba un audio simple desde tu celular recitando tu #CHORUS y súbelo en formato de archivo comprimido (.zip) o documento de enlace."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Creación de Bots en Discord con Python",
            "category": "Programación y Videojuegos",
            "short_intro": "Automatiza comunidades y ofrece servicios mediante la creación de bots profesionales.",
            "description": "<p>Aprende a usar discord.py para crear sistemas de tickets, comandos y respuestas automáticas.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Setup y Comandos Básicos",
                    "lessons": [
                        {
                            "title": "1. Configuración del Portal de Desarrolladores",
                            "body": "### El Token es tu Llave\nPara que tu código se comunique con Discord, necesitas crear una aplicación en el Developer Portal. Activa los 'Privileged Gateway Intents' (como Message Content Intent) para que tu bot pueda leer lo que escriben los usuarios.",
                            "assignments": [
                                {"title": "Creación de App", "type": "Document", "question": "Sube un screenshot del panel de tu bot en el Discord Developer Portal (¡Oculta el token!)."},
                                {"title": "Invitación al Servidor", "type": "URL", "question": "Genera el enlace de invitación (OAuth2) con permisos de administrador y pégalo aquí."},
                                {"title": "El Primer Script", "type": "Text", "question": "Pega el código básico de Python que enciende el bot y muestra 'Bot conectado' en la terminal."}
                            ]
                        },
                        {
                            "title": "2. Slash Commands (Comandos /)",
                            "body": "### Interacción Moderna\nLos comandos con prefijo (como !ayuda) están quedando atrás. Usaremos Slash Commands (`app_commands`) porque ofrecen autocompletado y mejor interfaz para el usuario.",
                            "assignments": [
                                {"title": "Comando Ping", "type": "Text", "question": "Escribe el código para un slash command `/ping` que responda con la latencia del bot."},
                                {"title": "Embeds Básicos", "type": "Text", "question": "Crea una función que envíe un mensaje tipo 'Embed' con título azul y descripción."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Sistemas Avanzados (Ticketly)",
                    "lessons": [
                        {
                            "title": "3. Sistema de Tickets",
                            "body": "### Soporte al Usuario\nUn bot de tickets necesita componentes UI (Botones y Menús desplegables). Cuando un usuario presiona 'Abrir Ticket', el bot debe crear un canal privado y asignar permisos exclusivos al usuario y al staff.",
                            "assignments": [
                                {"title": "UI de Botones", "type": "Text", "question": "Escribe el código de una clase en discord.py que defina un botón verde llamado 'Crear Ticket'."},
                                {"title": "Lógica de Canales", "type": "Text", "question": "Pega el fragmento de código que crea un canal de texto nuevo dentro de una categoría específica."},
                                {"title": "Gestión de Permisos", "type": "Text", "question": "Explica qué método usas para denegar el permiso `read_messages` al rol `@everyone` en el nuevo canal."}
                            ]
                        },
                        {
                            "title": "4. Hosting y Mantenimiento",
                            "body": "### Bot 24/7\nTu bot no puede depender de tu computadora encendida. Necesitas un VPS o un servicio de hosting en la nube para mantener el script corriendo permanentemente usando gestores como PM2 o systemd.",
                            "assignments": [
                                {"title": "Elección de Hosting", "type": "URL", "question": "Pega el enlace del proveedor de VPS o hosting (ej. Cuaku Hosting, Heroku, etc.) que utilizarás."},
                                {"title": "Archivo Requirements", "type": "Text", "question": "Escribe el contenido de tu archivo `requirements.txt` necesario para desplegar el bot."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Matemáticas Aplicadas para Negocios",
            "category": "Educación y Emprendimiento",
            "short_intro": "Usa funciones lineales y matrices para calcular costos, utilidades y optimizar tu negocio.",
            "description": "<p>Deja atrás las matemáticas teóricas. Aprende a aplicar fórmulas para tomar decisiones empresariales reales.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Funciones Lineales",
                    "lessons": [
                        {
                            "title": "1. Ecuaciones de Costo e Ingreso",
                            "body": "### Modelando tu Empresa\nEl costo total de producción se modela mediante una función lineal: Costo Total = (Costo Variable Unitario * Cantidad) + Costos Fijos. Comprender esto te permite proyectar gastos a cualquier escala de producción.",
                            "assignments": [
                                {"title": "Identificación de Costos", "type": "Text", "question": "Para un negocio de camisetas, lista 3 costos fijos y 2 costos variables."},
                                {"title": "Modelado de Función", "type": "Text", "question": "Si tus costos fijos son $500 y fabricar una unidad cuesta $5, escribe la función lineal de Costo Total (C(x))."},
                                {"title": "Gráfica de Costos", "type": "Document", "question": "Sube una foto de una gráfica trazada a mano o en software mostrando la línea de costos del ejercicio anterior."}
                            ]
                        },
                        {
                            "title": "2. El Punto de Equilibrio",
                            "body": "### Donde no pierdes ni ganas\nEl punto de equilibrio ocurre cuando el Ingreso Total es exactamente igual al Costo Total. A partir de esa unidad vendida, empiezas a generar utilidad pura.",
                            "assignments": [
                                {"title": "Cálculo de Equilibrio", "type": "Text", "question": "Si C(x) = 5x + 500 y vendes cada unidad a $15, ¿cuántas unidades debes vender para llegar al equilibrio? Muestra el cálculo."},
                                {"title": "Análisis de Utilidad", "type": "Text", "question": "Escribe la función de Utilidad U(x) = Ingreso - Costo, simplificada, para el ejercicio anterior."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Matrices y Optimización",
                    "lessons": [
                        {
                            "title": "3. Matrices para Inventarios",
                            "body": "### Multiplicación de Matrices\nLas matrices son excelentes para gestionar múltiples productos e ingredientes. Si tienes una matriz de materiales por producto, y la multiplicas por una matriz de costos de materiales, obtienes el costo exacto por producto de forma masiva.",
                            "assignments": [
                                {"title": "Creación de Matriz", "type": "Text", "question": "Crea una matriz 2x2 que represente el inventario de 2 productos en 2 tiendas diferentes."},
                                {"title": "Operación Matricial", "type": "Document", "question": "Sube un archivo mostrando el cálculo manual de la multiplicación de una matriz de inventario por un vector de precios."},
                                {"title": "Aplicación Real", "type": "Text", "question": "Explica en un párrafo cómo usarías una matriz para organizar el inventario de una aplicación como CuakuFit o similar."}
                            ]
                        },
                        {
                            "title": "4. Resolución de Sistemas",
                            "body": "### Oferta y Demanda\nLos sistemas de ecuaciones te permiten encontrar el precio exacto donde la cantidad que los clientes quieren comprar coincide con la cantidad que tú quieres vender (Punto de equilibrio del mercado).",
                            "assignments": [
                                {"title": "Ecuación de Demanda", "type": "Text", "question": "Resuelve el sistema: 2x + y = 100 ; x - y = 20. ¿Cuál es el valor de x e y?"},
                                {"title": "Interpretación", "type": "Text", "question": "Si 'x' es precio e 'y' es cantidad, ¿qué significa el resultado del punto anterior para un negocio?"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Lanzamiento de Marcas Digitales",
            "category": "Diseño y Marketing",
            "short_intro": "Desde el concepto visual hasta los assets técnicos como splash screens y logos de aplicaciones.",
            "description": "<p>Diseña la identidad visual de startups técnicas o de fitness y prepáralas para su lanzamiento oficial.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Identidad Visual",
                    "lessons": [
                        {
                            "title": "1. Psicología del Color y Naming",
                            "body": "### La Primera Impresión\nEl nombre y los colores definen cómo te perciben. Un servicio de hosting transmite seguridad con azules oscuros, mientras que una app de fitness requiere colores vibrantes (naranjas, verdes) que evoquen energía y movimiento.",
                            "assignments": [
                                {"title": "Paleta de Colores", "type": "URL", "question": "Crea una paleta en Coolors.co para una app de fitness y pega el enlace."},
                                {"title": "Justificación de Naming", "type": "Text", "question": "Explica por qué un nombre corto e impactante es crucial para plataformas digitales."},
                                {"title": "Boceto de Logo", "type": "Document", "question": "Sube un boceto (hecho a mano o digital) del isologotipo de tu marca."}
                            ]
                        },
                        {
                            "title": "2. Tipografía y Jerarquía",
                            "body": "### Legibilidad ante todo\nEn pantallas móviles, las fuentes sans-serif geométricas suelen ser la mejor opción. Mantén máximo dos familias tipográficas: una para títulos (con mucha personalidad) y otra para párrafos (limpia).",
                            "assignments": [
                                {"title": "Selección de Fuentes", "type": "Text", "question": "Nombra 2 fuentes de Google Fonts que combinarías para tu proyecto y especifica cuál es para títulos."},
                                {"title": "Análisis de Competencia", "type": "URL", "question": "Pega el enlace a la página de una marca competidora y analiza su uso tipográfico en 3 líneas."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Assets de Aplicación",
                    "lessons": [
                        {
                            "title": "3. Creación de Splash Screens",
                            "body": "### La Pantalla de Carga\nEl splash screen es la pantalla que aparece mientras la app carga. Debe ser minimalista: tu logo centrado, el color de fondo primario y, opcionalmente, un pequeño indicador de carga. No satures este espacio.",
                            "assignments": [
                                {"title": "Diseño de Splash", "type": "Document", "question": "Diseña la imagen del splash screen con el logo de tu proyecto (ej. CuakuFit) respetando las proporciones 16:9 vertical. Súbela aquí."},
                                {"title": "Exportación de Assets", "type": "Text", "question": "Lista los formatos y tamaños de imagen requeridos generalmente para íconos de iOS y Android."},
                                {"title": "Variación Modo Oscuro", "type": "Document", "question": "Sube la versión en 'Dark Mode' de tu splash screen."}
                            ]
                        },
                        {
                            "title": "4. Guía de Estilo (Brandbook)",
                            "body": "### Consistencia Técnica\nUna guía de estilo documenta los códigos HEX de los colores, los tamaños de las fuentes y cómo (y cómo NO) usar el logo. Es fundamental cuando trabajas en equipo.",
                            "assignments": [
                                {"title": "Documento Brandbook", "type": "Document", "question": "Sube un PDF de 1 o 2 páginas resumiendo los elementos visuales de tu marca."},
                                {"title": "Reglas del Logo", "type": "Text", "question": "Escribe 2 restricciones de uso de tu logo (ej. 'No estirar horizontalmente')."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Redacción y Argumentación Universitaria",
            "category": "Educación",
            "short_intro": "Estructura ensayos sólidos, plantea tesis debatibles y defiende tus ideas con claridad académica.",
            "description": "<p>Preparación intensiva para exámenes de admisión y trabajos universitarios de alto nivel.</p>",
            "modules": [
                {
                    "title": "Módulo 1: La Tesis y la Estructura",
                    "lessons": [
                        {
                            "title": "1. Planteamiento de la Tesis",
                            "body": "### El Corazón del Ensayo\nUna tesis no es un hecho demostrable ('El cielo es azul'), es una postura debatible ('La implementación de programas de educación digital reduce la brecha de desigualdad'). Todo tu texto orbitará en torno a defender esta oración.",
                            "assignments": [
                                {"title": "Redacción de Tesis", "type": "Text", "question": "Escribe una tesis debatible sobre la educación digital en colegios públicos."},
                                {"title": "Corrección de Errores", "type": "Text", "question": "Transforma la frase 'El internet es bueno para los niños' en una tesis académica fuerte."},
                                {"title": "Bosquejo General", "type": "Text", "question": "Escribe los 3 puntos principales que usarás para defender tu tesis."}
                            ]
                        },
                        {
                            "title": "2. Párrafos de Desarrollo",
                            "body": "### La Fórmula T-E-A\nCada párrafo debe tener: Tema (oración principal), Evidencia (datos, citas) y Análisis (cómo esa evidencia conecta con tu tesis). Nunca dejes una cita 'flotando' sin explicarla.",
                            "assignments": [
                                {"title": "Párrafo Argumentativo", "type": "Text", "question": "Redacta un párrafo siguiendo la fórmula T-E-A argumentando a favor de tu tesis anterior."},
                                {"title": "Citas APA", "type": "Text", "question": "Escribe el formato correcto en estilo APA 7 para citar un libro."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Refinamiento",
                    "lessons": [
                        {
                            "title": "3. Contraargumentos",
                            "body": "### Anticipar la Crítica\nUn buen ensayo reconoce posturas opuestas. Presentar un contraargumento (ej. 'Algunos afirman que lo digital distrae') y luego refutarlo fortalece tu credibilidad como autor.",
                            "assignments": [
                                {"title": "Redacción de Contraargumento", "type": "Text", "question": "Escribe un párrafo presentando una objeción válida a tu tesis principal."},
                                {"title": "Refutación", "type": "Text", "question": "Redacta la respuesta que destruye o minimiza el contraargumento que acabas de escribir."},
                                {"title": "Conectores Lógicos", "type": "Text", "question": "Lista 5 conectores de contraste que puedes usar en tu ensayo (ej. 'Sin embargo')."}
                            ]
                        },
                        {
                            "title": "4. Conclusión y Revisión",
                            "body": "### El Cierre Magistral\nLa conclusión no solo repite la introducción. Sintetiza los hallazgos y deja al lector con una reflexión final o una llamada a la acción. Revisa siempre la cohesión antes de entregar.",
                            "assignments": [
                                {"title": "Párrafo de Conclusión", "type": "Text", "question": "Escribe la conclusión de tu ensayo sobre educación digital."},
                                {"title": "Entrega Final del Ensayo", "type": "Document", "question": "Sube el ensayo argumentativo completo en formato Word o PDF."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Trigonometría Básica y Geometría Espacial",
            "category": "Educación",
            "short_intro": "Comprende triángulos, ángulos y modelado geométrico espacial.",
            "description": "<p>Desde el Teorema de Pitágoras hasta la resolución de problemas espaciales para ingresos universitarios.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Triángulos y Razones",
                    "lessons": [
                        {
                            "title": "1. Seno, Coseno y Tangente",
                            "body": "### SOH CAH TOA\nEl concepto fundamental de la trigonometría se basa en los triángulos rectángulos. Estas razones relacionan los ángulos con las longitudes de los lados. Es la base para medir distancias inaccesibles.",
                            "assignments": [
                                {"title": "Cálculo de Hipotenusa", "type": "Text", "question": "Si los catetos miden 3 y 4 metros, ¿cuánto mide la hipotenusa? Muestra el paso a paso."},
                                {"title": "Aplicación de Tangente", "type": "Text", "question": "Un árbol proyecta una sombra de 10m y el ángulo de elevación del sol es de 45 grados. Calcula la altura del árbol."},
                                {"title": "Razones Inversas", "type": "Text", "question": "Define con tus palabras qué son la secante, cosecante y cotangente."}
                            ]
                        },
                        {
                            "title": "2. Ley de Senos y Cosenos",
                            "body": "### Triángulos Oblicuángulos\nCuando no tienes un ángulo de 90 grados, debes usar estas leyes universales. Son clave para el modelado de terrenos y la navegación.",
                            "assignments": [
                                {"title": "Identificación de la Ley", "type": "Text", "question": "¿Cuándo debes usar la Ley de Cosenos en lugar de la Ley de Senos?"},
                                {"title": "Resolución Práctica", "type": "Document", "question": "Resuelve a mano el siguiente triángulo: a=5, b=7, c=10. Encuentra el ángulo más grande y sube la foto."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Geometría Espacial",
                    "lessons": [
                        {
                            "title": "3. Volúmenes y Áreas de Superficie",
                            "body": "### Pasando al 3D\nEl espacio tridimensional requiere visualizar las figuras desde distintos planos. Entender cómo se relacionan el área base y la altura de prismas y cilindros es vital para el diseño.",
                            "assignments": [
                                {"title": "Volumen de un Cilindro", "type": "Text", "question": "Calcula el volumen de un cilindro con radio de 2m y altura de 5m."},
                                {"title": "Área de un Cubo", "type": "Text", "question": "Si la diagonal de la cara de un cubo mide raíz de 8, ¿cuál es su área total?"},
                                {"title": "Desarrollo Plano", "type": "Document", "question": "Dibuja el desarrollo plano de una pirámide de base cuadrada y súbelo."}
                            ]
                        },
                        {
                            "title": "4. Modelado Espacial Aplicado",
                            "body": "### Traslación al Software\nLos principios geométricos se aplican en herramientas de modelado 3D (como Blender o Roblox). Las coordenadas X, Y, Z determinan vértices exactos.",
                            "assignments": [
                                {"title": "Coordenadas 3D", "type": "Text", "question": "En un sistema de coordenadas (x,y,z), calcula la distancia entre los puntos (0,0,0) y (3,4,12)."},
                                {"title": "Análisis Geométrico Final", "type": "Document", "question": "Elabora un mapa mental sobre las fórmulas de cuerpos redondos (esfera, cilindro, cono) y súbelo."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Productividad y Gestión de Proyectos Tech",
            "category": "Tecnología y Negocios",
            "short_intro": "Organiza tu tiempo, maneja tus repositorios y lidera proyectos de desarrollo eficientemente.",
            "description": "<p>Aprende metodologías ágiles, uso de Notion y control de versiones para no volverte loco programando.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Organización Personal",
                    "lessons": [
                        {
                            "title": "1. Time Blocking",
                            "body": "### Protege tu Enfoque\nEl multitasking destruye la productividad. Asigna bloques de tiempo cerrados para tareas específicas: 2 horas para código, 1 hora para correos. Respeta el bloque.",
                            "assignments": [
                                {"title": "Diseño de Calendario", "type": "Document", "question": "Sube una captura de tu Google Calendar con bloques de tiempo definidos para tu semana."},
                                {"title": "Técnica Pomodoro", "type": "Text", "question": "Describe cómo adaptarías la técnica Pomodoro (25m de trabajo) para sesiones largas de programación."},
                                {"title": "Matriz de Eisenhower", "type": "Document", "question": "Dibuja la matriz y clasifica 5 tareas pendientes que tengas ahora mismo."}
                            ]
                        },
                        {
                            "title": "2. Creación del 'Segundo Cerebro' en Notion",
                            "body": "### Libera tu Mente\nNo uses tu cerebro para recordar tareas, úsalo para crear. Documenta tus ideas, snippets de código y metas en una base de datos centralizada.",
                            "assignments": [
                                {"title": "Plantilla de Notion", "type": "URL", "question": "Crea un workspace básico en Notion para tus proyectos y pega el enlace de invitación (modo lectura)."},
                                {"title": "Base de datos Relacional", "type": "Text", "question": "Explica brevemente cómo conectarías una tabla de 'Proyectos' con una de 'Tareas' en Notion."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Gestión de Código",
                    "lessons": [
                        {
                            "title": "3. Fundamentos de Git",
                            "body": "### Historial Inmutable\nGit es el estándar de la industria. Aprender a hacer commits atómicos (pequeños y con un solo propósito) te salvará la vida cuando algo se rompa en producción.",
                            "assignments": [
                                {"title": "Creación de Repositorio", "type": "URL", "question": "Pega el enlace a un repositorio público vacío creado por ti en GitHub."},
                                {"title": "Secuencia de Comandos", "type": "Text", "question": "Escribe los 3 comandos básicos de terminal para subir un cambio local a la rama main (add, commit, push)."},
                                {"title": "Convención de Commits", "type": "Text", "question": "Da 3 ejemplos de mensajes de commit siguiendo el formato 'Conventional Commits' (ej. feat:, fix:)."}
                            ]
                        },
                        {
                            "title": "4. Tableros Kanban",
                            "body": "### Visualiza el Flujo\nHerramientas como Trello o GitHub Projects te permiten mover tarjetas de 'To Do' a 'In Progress' a 'Done'. Limita el trabajo en progreso para evitar cuellos de botella.",
                            "assignments": [
                                {"title": "Configuración Kanban", "type": "URL", "question": "Crea un tablero de Trello o GitHub Projects público para un proyecto hipotético y comparte el link."},
                                {"title": "Análisis de Flujo", "type": "Text", "question": "Explica qué sucede con tu eficiencia si tienes 10 tareas simultáneas en la columna 'In Progress'."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Desarrollo Web Ágil y Landing Pages",
            "category": "Programación y Videojuegos",
            "short_intro": "Crea y despliega páginas de aterrizaje altamente convertidoras en tiempo récord.",
            "description": "<p>Aprende estructura HTML/CSS, integración de formularios y despliegue gratuito para lanzar tus ideas rápido.</p>",
            "modules": [
                {
                    "title": "Módulo 1: Frontend Básico",
                    "lessons": [
                        {
                            "title": "1. Estructura Semántica",
                            "body": "### Más allá de los Divs\nHTML5 permite usar etiquetas como `<header>`, `<nav>`, `<section>` y `<footer>`. Esto mejora el SEO y la accesibilidad de tu landing page enormemente.",
                            "assignments": [
                                {"title": "Esqueleto HTML", "type": "Text", "question": "Pega el código HTML básico de la estructura de una landing (sin CSS)."},
                                {"title": "SEO On-Page", "type": "Text", "question": "Escribe las meta-etiquetas de 'title' y 'description' optimizadas para un negocio local de comida."},
                                {"title": "Llamado a la Acción (CTA)", "type": "Text", "question": "Escribe 3 ejemplos de textos persuasivos para botones (evita el aburrido 'Enviar')."}
                            ]
                        },
                        {
                            "title": "2. CSS con Flexbox",
                            "body": "### Centrar un Div ya no es magia\nFlexbox te permite crear layouts en una sola dimensión (filas o columnas) de manera increíblemente sencilla. Es indispensable para crear barras de navegación.",
                            "assignments": [
                                {"title": "Código Flexbox", "type": "Text", "question": "Escribe las 3 propiedades CSS necesarias en un contenedor para que sus elementos se centren vertical y horizontalmente."},
                                {"title": "Diseño Responsive", "type": "Text", "question": "Escribe una media query en CSS que cambie el color de fondo a azul si la pantalla es menor a 768px."}
                            ]
                        }
                    ]
                },
                {
                    "title": "Módulo 2: Integración y Deploy",
                    "lessons": [
                        {
                            "title": "3. Captación de Leads",
                            "body": "### Formularios y Base de Datos\nUna landing page sin formulario de captura no sirve para ventas. Puedes integrar servicios como Formspree o Mailchimp mediante un simple tag de `<form>`.",
                            "assignments": [
                                {"title": "Formulario HTML", "type": "Text", "question": "Escribe el código de un formulario pidiendo Nombre y Email, con su botón de envío."},
                                {"title": "Validación Frontend", "type": "Text", "question": "Explica qué atributo HTML usarías para hacer que el campo de Email sea obligatorio."},
                                {"title": "Página de Gracias", "type": "Text", "question": "Explica por qué es importante redirigir al usuario a una 'Thank You Page' tras llenar el formulario."}
                            ]
                        },
                        {
                            "title": "4. Despliegue en la Nube",
                            "body": "### Sube tu web gratis\nPlataformas como Vercel, Netlify o GitHub Pages te permiten conectar tu repositorio y publicar tu página al mundo en cuestión de minutos con certificados SSL integrados.",
                            "assignments": [
                                {"title": "Conexión a Vercel/Netlify", "type": "URL", "question": "Sube el código que hiciste a Vercel o Netlify y pega la URL pública generada."},
                                {"title": "Dominios Personalizados", "type": "Text", "question": "Explica qué son los registros DNS (específicamente A y CNAME) a la hora de vincular un dominio propio."}
                            ]
                        }
                    ]
                }
            ]
        }
    ]

def run():
    frappe.set_user("Administrator")
    print("Iniciando creación masiva de cursos...")

    instructor_name = "Administrator"
    courses_data = get_courses_data()

    for course_info in courses_data:
        cat_name = course_info["category"]
        course_title = course_info["title"]
        print(f"\n--- Procesando Curso: {course_title} ---")

        # 1. Crear o buscar Categoría
        if not frappe.db.exists("LMS Category", {"category": cat_name}):
            frappe.get_doc({"doctype": "LMS Category", "category": cat_name}).insert(ignore_permissions=True, ignore_mandatory=True)
        cat_id = frappe.get_all("LMS Category", filters={"category": cat_name})[0].name

        # 2. Crear o actualizar Curso Master
        if frappe.db.exists("LMS Course", {"title": course_title}):
            course = frappe.get_doc("LMS Course", {"title": course_title})
            print(f"El curso '{course_title}' ya existe. Usando existente.")
        else:
            course = frappe.get_doc({
                "doctype": "LMS Course",
                "title": course_title,
                "short_introduction": course_info["short_intro"],
                "description": course_info["description"],
                "published": 1,
                "category": cat_id,
                "card_gradient": "Blue",
                "enable_certification": 1
            })
            course.insert(ignore_permissions=True, ignore_mandatory=True)
            print(f"Curso creado: {course.name}")
        
        course_name = course.name

        # Validar instructor
        instructor_exists = any(i.instructor == instructor_name for i in course.get("instructors", []))
        if not instructor_exists:
            course.append("instructors", {"instructor": instructor_name})
            course.save(ignore_permissions=True)

        # Helpers locales vinculados al curso actual
        def create_chapter(title):
            existing = frappe.get_all("Course Chapter", filters={"title": title, "course": course_name})
            if existing:
                return frappe.get_doc("Course Chapter", existing[0].name)
            doc = frappe.get_doc({
                "doctype": "Course Chapter",
                "title": title,
                "course": course_name
            })
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            return doc

        def create_assignments_for_lesson(assignments_data):
            assign_names = []
            for a in assignments_data:
                assignment_title = f"{course_title} - {a['title']}"
                existing_assign = frappe.get_all("LMS Assignment", {"title": assignment_title, "course": course_name})
                if existing_assign:
                    assign_names.append(existing_assign[0].name)
                else:
                    doc = frappe.get_doc({
                        "doctype": "LMS Assignment",
                        "title": assignment_title,
                        "type": a["type"],
                        "course": course_name,
                        "question": a["question"]
                    })
                    doc.insert(ignore_permissions=True, ignore_mandatory=True)
                    assign_names.append(doc.name)
            return assign_names

        def create_lesson(chap_name, title, body, assignments_data):
            # Crear las asignaciones primero
            assign_names = create_assignments_for_lesson(assignments_data)

            # Construir el JSON de EditorJS
            blocks = []
            for p in body.split('\n\n'):
                if p.strip():
                    if p.startswith('### '):
                        blocks.append({
                            "type": "header",
                            "data": {"text": p.replace('### ', ''), "level": 3}
                        })
                    else:
                        blocks.append({
                            "type": "paragraph",
                            "data": {"text": p.replace('\n', '<br>')}
                        })
            
            # Inyectar bloques de asignación
            for as_name in assign_names:
                blocks.append({
                    "type": "assignment",
                    "data": {"assignment": as_name}
                })

            content_json = json.dumps({
                "time": 1716348270119,
                "blocks": blocks,
                "version": "2.29.1"
            })

            existing = frappe.get_all("Course Lesson", filters={"title": title, "chapter": chap_name})
            if existing:
                doc = frappe.get_doc("Course Lesson", existing[0].name)
                doc.content = content_json
                doc.body = ""
                doc.save(ignore_permissions=True)
                return existing[0].name
            
            doc = frappe.get_doc({
                "doctype": "Course Lesson",
                "title": title,
                "chapter": chap_name,
                "course": course_name,
                "body": "",
                "content": content_json
            })
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            return doc.name

        # 3. Procesar Módulos y Lecciones
        course_chapter_names = []
        for mod in course_info["modules"]:
            chapter_doc = create_chapter(mod["title"])
            chapter_doc.set("lessons", [])
            
            for les in mod["lessons"]:
                # Generar lección y sus múltiples asignaciones
                l_name = create_lesson(
                    chapter_doc.name, 
                    les["title"], 
                    les["body"], 
                    les.get("assignments", [])
                )
                chapter_doc.append("lessons", {"lesson": l_name})
            
            chapter_doc.save(ignore_permissions=True)
            course_chapter_names.append(chapter_doc.name)

        # 4. Vincular Capítulos al Curso Master
        course.reload()
        course.set("chapters", [])
        for c_name in course_chapter_names:
            course.append("chapters", {"chapter": c_name})
        course.save(ignore_permissions=True)

    frappe.db.commit()
    print("\n¡Proceso Finalizado! Los 10 cursos con sus asignaciones se han creado en la base de datos.")

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else "studybadge.localhost"
    frappe.init(site=site)
    frappe.connect()
    run()