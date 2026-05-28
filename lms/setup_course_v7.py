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
    "title": "Programación sin Fricción: Publica tu Web con Inteligencia Artificial",
    "short_introduction": "Aprende las bases lógicas del código sin teoría aburrida y publica tu primera web interactiva usando la IA como tu copiloto de aprendizaje.",
    "description": "<p>Olvídate de la teoría interminable y la parálisis por análisis. En este curso práctico e interactivo, aprenderás a programar escribiendo código real desde el primer minuto. Descubrirás cómo transformar a la Inteligencia Artificial en tu tutor personalizado 24/7 para resolver dudas, depurar errores y acelerar tu aprendizaje.</p><ul><li><strong>Enfoque 100% práctico:</strong> Crea proyectos reales y funcionales que puedas mostrar al mundo.</li><li><strong>Copiloto de Inteligencia Artificial:</strong> Domina el arte de formular prompts para destrabar tu código y avanzar sin frustraciones.</li><li><strong>Despliegue real:</strong> Al finalizar, sabrás cómo publicar tu proyecto en internet de forma totalmente gratuita.</li></ul>",
    "card_gradient": "Blue",
    "enable_certification": 1,
    "studybadge_ai_enabled": 1,
    "ai_rubric": "Evalúa las tareas de forma clara, justa y práctica. Prioriza comprensión, aplicación real, claridad y creatividad antes que perfección técnica. Valora respuestas naturales, ejemplos útiles y esfuerzo real. Penaliza respuestas vacías, copiadas, incoherentes o demasiado genéricas. Al final, asigna una nota del 1 al 10. 1-3 = Muy deficiente, 4-6 = Insuficiente, 7-8 = Aprobado, 9-10 = Excelente. Siempre indica puntos fuertes, qué mejorar, nota final y estado: Aprobado si es 7 o más, Desaprobado si es menor a 7.",
    "chapters": [
        {
            "title": "Módulo 1: Adiós al miedo al código y tus nuevos aliados",
            "lessons": [
                {
                    "title": "Piensa como programador: Tu primer código guiado por IA",
                    "objective": "Comprender la lógica de funcionamiento de una computadora y utilizar la Inteligencia Artificial como tutor personal de desarrollo.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Olvídate de que programar es solo para genios matemáticos. Programar es, en realidad, dar instrucciones claras paso a paso a una computadora para resolver un problema. Es muy similar a escribir una receta de cocina, pero en un idioma que la máquina pueda procesar.",
                                "Hoy cuentas con un superpoder que no existía hace unos años: la Inteligencia Artificial. Herramientas como ChatGPT o Claude serán tus tutores privados las 24 horas del día. No resolverán las cosas por ti; te explicarán cada línea para que aprendas a tu propio ritmo y sin frustraciones."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Las computadoras son veloces, pero extremadamente literales. No asumen intenciones ni leen entre líneas. Si le pides a una computadora que 'prepare café', fallará porque no sabe qué es una taza ni cómo calentar el agua. Debes guiarla paso a paso.",
                                "Para comunicarte con ella, utilizas un lenguaje de programación (como JavaScript) y un editor de código (como Visual Studio Code). Al sumar la IA a esta ecuación, puedes pedirle cosas como: 'Explícame este código como si tuviera 10 años' o '¿Por qué falla este bloque?'. El aprendizaje se vuelve fluido y conversacional."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Para indicarle a la computadora que muestre un mensaje en pantalla usando JavaScript, empleamos la instrucción 'console.log()'.",
                                "Si escribes: console.log('¡Hola, mundo!'); la pantalla mostrará exactamente ese texto. Si escribes: console.log(10 + 5); procesará la operación y mostrará 15. Prueba copiar estas líneas en tu chat de IA y pregúntale: '¿Qué hace este código de JavaScript paso a paso?'. Verás lo fácil que es entender el desglose."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El error más habitual al comenzar es cometer fallos de ortografía o puntuación, conocidos como 'errores de sintaxis'. Olvidar cerrar unas comillas, un paréntesis, o escribir 'consolo.log' en vez de 'console.log' detendrá el programa.",
                                "No dejes que esto te frustre. Si tu código no funciona, cópialo, pégalo en la IA y pregúntale: '¿Por qué no funciona este código y cómo lo soluciono?'. Obtendrás la respuesta corregida y la explicación en segundos."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: programar es dar instrucciones ordenadas. La IA es tu mejor aliada para traducir conceptos complejos, corregir errores en tiempo real y guiarte de la mano.",
                                "Tu acción de hoy es simple: instala Visual Studio Code en tu computadora. Luego, abre tu IA favorita y escribe este prompt: 'Explícame qué es una variable en programación con una analogía sencilla y dame 3 ejemplos cortos en JavaScript'. ¡Lee la respuesta y prepárate para el siguiente paso!"
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Pierde el miedo a programar con IA",
                        "questions": [
                            {
                                "question": "Según la lección, ¿qué es programar y con qué actividad cotidiana se relaciona?",
                                "options": [
                                    "Es un proceso matemático complejo similar a descifrar algoritmos de encriptación.",
                                    "Es como escribir una receta de cocina: dar instrucciones detalladas paso a paso a la máquina.",
                                    "Es una tarea puramente visual, parecida a diseñar una maqueta en un lienzo digital.",
                                    "Es una actividad técnica rígida que solo ingenieros especializados pueden realizar."
                                ],
                                "answer": 1,
                                "explanation": "La programación consiste en estructurar instrucciones lógicas paso a paso para que una máquina las ejecute, igual que los pasos de una receta de cocina."
                            },
                            {
                                "question": "¿Cuál es la instrucción estándar en JavaScript para mostrar un mensaje u operación en la consola?",
                                "options": [
                                    "console.log()",
                                    "consolo.log()",
                                    "mostrar.mensaje()",
                                    "print.screen()"
                                ],
                                "answer": 0,
                                "explanation": "La instrucción correcta y nativa de JavaScript para imprimir información en la consola de depuración es 'console.log()'."
                            },
                            {
                                "question": "¿Cuál es la acción recomendada al final de esta lección para comenzar tu práctica?",
                                "options": [
                                    "Comprar un servidor web para alojar tus bases de datos.",
                                    "Memorizar todos los errores de sintaxis comunes de JavaScript.",
                                    "Instalar Visual Studio Code y pedirle a la IA que te explique qué es una variable con ejemplos sencillos.",
                                    "Escribirle a un programador profesional para que resuelva tus ejercicios."
                                ],
                                "answer": 2,
                                "explanation": "La acción recomendada es configurar tu entorno de trabajo básico con VS Code y familiarizarte con el uso de prompts sencillos en la IA."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu primer rescate de código con soporte de IA",
                        "type": "Text",
                        "question": "<p>¡Es momento de pasar a la acción! Imagina que un amigo que está lanzando una pizzería intentó programar un pequeño mensaje en JavaScript para recibir a sus clientes y calcular una orden básica. Sin embargo, su código tiene errores, se detiene y está muy frustrado.</p><p><strong>Este es el código defectuoso de tu amigo:</strong></p><pre>consolo.log(\"¡Bienvenido a Pizza Express!)<br>console.log(15 + 4</pre><p>Tu misión es usar una Inteligencia Artificial (ChatGPT, Claude, Gemini, etc.) para identificar los problemas, solucionarlos y entender la corrección.</p><p><strong>Sigue estos pasos:</strong></p><ol><li>Copia el código con errores de arriba.</li><li>Abre la IA que prefieras y envíale un prompt similar a este: <em>\"Soy principiante. Este código de JavaScript tiene errores de sintaxis y no corre. ¿Podrías indicarme exactamente qué está mal, cómo solucionarlo y darme el código corregido?\"</em>.</li><li>Analiza detalladamente la respuesta de la IA (presta atención a las comillas, nombres de funciones y paréntesis).</li></ol><p><strong>¿Qué debes entregar?</strong></p><p>Escribe tu respuesta en el cuadro de texto utilizando el siguiente formato:</p><ul><li><strong>1. El código de JavaScript completamente corregido.</strong></li><li><strong>2. Una explicación breve (2 a 3 líneas)</strong> con tus propias palabras sobre qué fallaba en el código original y por qué la computadora no podía ejecutarlo.</li></ul>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 2: Variables y Datos: Las cajas lógicas",
            "lessons": [
                {
                    "title": "Variables y Operaciones: Tu primera calculadora lógica",
                    "objective": "Aprender a almacenar datos en variables, realizar operaciones aritméticas básicas y concatenar texto y números.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Imagina que estás organizando tu casa y usas cajas de cartón. Si guardas tus libros en una caja y escribes por fuera 'Libros', sabrás exactamente qué contiene y dónde buscarlo. En programación, las variables funcionan igual: son cajas virtuales con un nombre único que almacenan información para que la uses cuando quieras.",
                                "Hoy aprenderás a crear tus primeras variables en JavaScript, a guardar números y textos en ellas, y a combinarlas para dar vida a una mini-calculadora automática."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para declarar una variable en JavaScript, usamos la palabra clave 'let', seguida del nombre de nuestra variable, el signo de asignación '=' y el valor. Por ejemplo: let edad = 25;. El signo '=' no significa igualdad matemática aquí, sino 'guardar dentro'.",
                                "Trabajamos con diferentes tipos de datos. Los dos fundamentales son los Números (se escriben directamente, como 10 o 5.5) y los Textos (siempre van entre comillas, como 'Hola'). Si pones un número entre comillas ('10'), la computadora lo tratará como texto y no podrás realizar operaciones matemáticas con él.",
                                "Con las variables numéricas puedes usar los operadores estándar: + (suma), - (resta), * (multiplicación) y / (división). Si aplicas el signo '+' entre un texto y un número, la computadora los unirá en una sola frase. A este proceso lo llamamos 'concatenación'."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Escribe y analiza este bloque de código para entender el flujo de datos:",
                                "// 1. Declaramos las variables con los datos de entrada\nlet precioProducto = 120;\nlet descuento = 20;\n\n// 2. Realizamos la operación matemática\nlet precioFinal = precioProducto - descuento;\n\n// 3. Mostramos el resultado concatenando texto y variables\nconsole.log('El precio final con descuento es: $' + precioFinal);",
                                "Si decides cambiar el valor de 'precioProducto' o de 'descuento', no necesitas reescribir todo el programa. Al ejecutarlo, las operaciones se actualizarán de forma automática con los nuevos valores."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "Omitir las comillas en los textos: Escribir 'let nombre = Juan;' causará un error porque el sistema buscará una variable llamada Juan. Lo correcto es 'let nombre = \"Juan\";'.",
                                "Espacios en los nombres de variables: Escribir 'let precio total = 100;' romperá el código. Usa el formato 'camelCase' (mayúscula intermedia) para mantenerlo como una sola palabra legible: 'precioTotal'.",
                                "Confundir tipos de datos: Si declaras 'let a = \"5\";' y 'let b = \"10\";', al sumarlas con '+' obtendrás '510' en lugar de 15, porque las comillas indican al sistema que junte las piezas de texto en lugar de sumarlas matemáticamente."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Las variables son contenedores identificados por un nombre único. Usamos 'let' para definirlas, guardamos datos en ellas y podemos operar matemáticamente con números o encadenar textos usando el operador '+'.",
                                "Tu reto de hoy: Crea un archivo llamado 'calculadora.js' en tu editor, escribe el código del ejemplo práctico, experimenta modificando los valores y añade una nueva variable para calcular el IVA (16% o 21%).",
                                "Para acelerar el proceso, copia este prompt en tu IA: 'Dame 3 ejercicios muy sencillos de declaración de variables y concatenación en JavaScript para resolver ahora mismo'."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu primera mini-calculadora y variables",
                        "questions": [
                            {
                                "question": "Si ejecutas el siguiente código: let x = '4'; let y = '2'; console.log(x + y); ¿qué imprimirá la consola?",
                                "options": [
                                    "Imprimirá 6, realizando la suma aritmética.",
                                    "Imprimirá '42' porque las comillas definen textos y el operador '+' los une.",
                                    "Lanzará un error de sintaxis inmediatamente.",
                                    "Imprimirá undefined porque no se pueden sumar cadenas."
                                ],
                                "answer": 1,
                                "explanation": "Al usar comillas, los valores se consideran strings (texto). El operador '+' concatena (une) los textos, dando como resultado '42'."
                            },
                            {
                                "question": "¿Cuál de las siguientes declaraciones de variables sigue las mejores prácticas de sintaxis en JavaScript?",
                                "options": [
                                    "let primer costo = 150;",
                                    "let primer-costo = 150;",
                                    "let primerCosto = 150;",
                                    "let primerCosto = '150;"
                                ],
                                "answer": 2,
                                "explanation": "La variable 'let primerCosto = 150;' utiliza la convención camelCase, no tiene espacios ni caracteres inválidos, y el tipo de dato numérico no lleva comillas."
                            },
                            {
                                "question": "En JavaScript, ¿cuál es la función real del operador de asignación '=' al declarar una variable?",
                                "options": [
                                    "Establece que el valor de la derecha se almacena dentro del contenedor de la izquierda.",
                                    "Compara matemáticamente si el lado izquierdo es igual al lado derecho.",
                                    "Imprime de forma automática el valor asignado en la pantalla.",
                                    "Bloquea la variable para que su contenido nunca pueda modificarse."
                                ],
                                "answer": 0,
                                "explanation": "El signo '=' es un operador de asignación, no de igualdad. Toma el valor del lado derecho y lo guarda dentro de la variable especificada a la izquierda."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: El Presupuesto de la Fiesta",
                        "type": "Text",
                        "question": "<p>¡Es hora de programar algo sumamente práctico! Imagina que eres el organizador de un evento y necesitas calcular rápidamente los costos de la comida para ajustarte al presupuesto sin hacer cuentas manuales.</p><p><strong>Tu objetivo:</strong> Escribir un script en JavaScript que determine de forma automática el costo total de los alimentos y la aportación exacta que debe hacer cada participante.</p><p><strong>Instrucciones:</strong></p><ol><li>Declara tres variables usando <code>let</code> con valores numéricos de tu elección: <code>cantidadInvitados</code>, <code>costoPizzas</code> y <code>costoRefrescos</code>.</li><li>Crea una variable llamada <code>costoTotal</code> que sume los costos de pizzas y refrescos.</li><li>Crea una variable llamada <code>cuotaPorPersona</code> que divida el <code>costoTotal</code> entre la <code>cantidadInvitados</code>.</li><li>Usa <code>console.log()</code> para mostrar en la consola dos mensajes claros y descriptivos que unan tus textos y variables (concatenación). Por ejemplo:<br><em>\"El costo total de la fiesta es: $X\"</em><br><em>\"Cada invitado debe pagar: $Y\"</em></li></ol><p><strong>¿Qué debes entregar?</strong></p><p>Copia y pega el código completo de tu script. Al final, añade un comentario de una sola línea (usando <code>//</code>) indicando cuáles fueron tus datos de entrada y el resultado exacto impreso en pantalla.</p>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 3: Condicionales: Cómo toma decisiones un programa",
            "lessons": [
                {
                    "title": "Estructuras If/Else: Creando un validador inteligente",
                    "objective": "Aprender a estructurar condicionales (if/else) en JavaScript para que tus aplicaciones evalúen datos y tomen decisiones de forma autónoma.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "Piensa en cómo tomas decisiones a diario: si está lloviendo, usas paraguas; si el semáforo está en rojo, frenas. Tu cerebro evalúa de forma constante condiciones y define tu comportamiento.",
                                "En la programación ocurre lo mismo. Hasta ahora, tu código se ejecutaba de forma lineal, de arriba a abajo. Hoy aprenderás a darle un 'cerebro' a tus programas para que analicen datos y tomen diferentes caminos lógicos. Esto transforma una web estática en una aplicación interactiva e inteligente."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Para tomar decisiones en JavaScript, empleamos la estructura condicional 'if' (si ocurre esto) y 'else' (de lo contrario). Le indicamos a la computadora: 'Si esta condición se cumple, ejecuta este bloque de código; si no, ejecuta este otro'.",
                                "Para evaluar las condiciones, usamos operadores de comparación: '>' (mayor que), '<' (menor que), y '===' (estrictamente igual a). La computadora evalúa la condición y devuelve un valor booleano: verdadero (true) o falso (false), ejecutando solo el bloque que corresponda."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Imagina un sistema automatizado de control de acceso para mayores de edad. El código es directo y limpio:",
                                "let edadUsuario = 19;\n\nif (edadUsuario >= 18) {\n  console.log('Acceso autorizado.');\n} else {\n  console.log('Acceso denegado: Menor de edad.');\n}",
                                "Si ejecutas este código con el valor de 19, se imprimirá 'Acceso autorizado'. Si cambias el valor de 'edadUsuario' a 16 y ejecutas de nuevo, el sistema tomará la ruta alternativa, imprimiendo el mensaje de denegación."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "Confundir '=' con '===': Un solo '=' asigna un valor a una variable. Los tres signos '===' comparan si dos elementos son idénticos. Escribir 'if (edad = 18)' alterará el valor de la variable en lugar de compararla, rompiendo la lógica.",
                                "Olvidar las llaves '{}': Las llaves encierran el código que pertenece a cada decisión. Si no las colocas, JavaScript no sabrá dónde termina tu bloque 'if' y dónde comienza el 'else', generando fallas en la ejecución."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Los condicionales permiten controlar el rumbo de tu código utilizando 'if' y 'else'. Son la base lógica para construir flujos de registro, validaciones de seguridad y sistemas interactivos.",
                                "Tu reto de hoy: Crea una variable llamada 'temperatura'. Escribe un condicional: si es mayor a 30, imprime '¡Prende el aire acondicionado!'; de lo contrario, imprime 'El clima está agradable'. Si necesitas apoyo visual, dile a tu IA: 'Dame 3 ejemplos prácticos de condicionales if/else en JavaScript explicados línea por línea'."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Tu primer validador inteligente",
                        "questions": [
                            {
                                "question": "¿Cuál es la diferencia de uso entre '=' y '===' en JavaScript?",
                                "options": [
                                    "El signo '=' se usa para guardar información en una variable, mientras que '===' sirve para verificar si dos valores son iguales.",
                                    "El signo '=' realiza comparaciones de igualdad, mientras que '===' define variables globales.",
                                    "Se pueden usar indistintamente, son el mismo operador con distinta sintaxis.",
                                    "El operador '=' es numérico y '===' se usa únicamente con cadenas de texto."
                                ],
                                "answer": 0,
                                "explanation": "El símbolo '=' asigna valores a una variable. El operador '===' evalúa si dos valores (y sus tipos) son exactamente iguales."
                            },
                            {
                                "question": "¿Cuál es la función de las llaves '{}' en una estructura condicional?",
                                "options": [
                                    "Le indican a la computadora que la comparación debe repetirse de forma infinita.",
                                    "Delimitan el bloque de instrucciones de código que corresponden a cada decisión tomada.",
                                    "Reemplazan la necesidad de usar operadores como mayor que o menor que.",
                                    "Sirven exclusivamente para que el código se muestre con colores en el editor."
                                ],
                                "answer": 1,
                                "explanation": "Las llaves definen el alcance y el grupo de instrucciones que se ejecutarán cuando se cumpla o no la condición declarada."
                            },
                            {
                                "question": "Si declaras 'let temperatura = 28;' y ejecutas 'if (temperatura > 30)', ¿qué bloque se ejecutará?",
                                "options": [
                                    "El bloque 'if', porque 28 es cercano a 30.",
                                    "El sistema arrojará un error de sintaxis al no cumplirse la igualdad exacta.",
                                    "Se ignorará todo el condicional y el script terminará bruscamente.",
                                    "Se ejecutará el bloque dentro del 'else', ya que la condición evaluada es falsa (false)."
                                ],
                                "answer": 3,
                                "explanation": "Como 28 no es mayor que 30, la condición del 'if' resulta falsa, forzando al programa a ejecutar la sección alternativa dentro del bloque 'else'."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Tu primer validador de descuentos para E-commerce",
                        "type": "Text",
                        "question": "<p>¡Felicidades por dominar los condicionales! Ahora aplicarás este conocimiento en un escenario comercial común: automatizar el envío gratuito en una tienda digital según el monto de la compra.</p><p><strong>El reto:</strong> Programar un sistema de decisión que valide si un carrito califica para envío gratis o si debe agregarse un recargo.</p><p><strong>Instrucciones:</strong></p><ol><li>Crea una variable llamada <code>montoCompra</code> y asígnale un valor numérico inicial (por ejemplo, <code>120</code>).</li><li>Escribe una estructura condicional (<code>if</code> / <code>else</code>) con la siguiente lógica:</li><ul><li>Si el <code>montoCompra</code> es mayor o igual a 100, muestra en la consola el mensaje: <em>\"¡Envío gratis garantizado! Total: $[montoCompra]\"</em>.</li><li>Si es menor a 100, muestra el mensaje: <em>\"El envío tiene un costo extra de $10. Total a pagar: $[montoCompra + 10]\"</em>.</li></ul><li>Prueba tu código cambiando el valor de <code>montoCompra</code> a <code>85</code> para asegurarte de que tome el camino correcto en ambos escenarios.</li></ol><p><strong>¿Qué debes entregar?</strong></p><p>Copia y pega en la caja de texto tu código JavaScript completo junto con un párrafo breve explicativo de qué ocurrió en la consola cuando cambiaste el monto de la compra.</p>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 4: Automatizando con Bucles y Funciones",
            "lessons": [
                {
                    "title": "Funciones y Bucles: Escribe menos, automatiza más",
                    "objective": "Aprender a delegar tareas repetitivas a la computadora mediante bucles y a modularizar código reutilizable mediante funciones.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¿Te imaginas escribir cien veces 'No debo hablar en clase' en una libreta? Sería agotador. En el mundo físico puede que no tengas opción, pero en programación, forzar a un humano a realizar tareas repetitivas es ineficiente.",
                                "Las computadoras destacan por su velocidad y constancia. Hoy aprenderás a delegarles el trabajo repetitivo usando dos herramientas fundamentales que estructuran cualquier programa moderno: los bucles (loops) y las funciones."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Un bucle es una instrucción que le dice a la computadora: 'Repite este bloque de código mientras se cumpla una condición'. El bucle 'for' es el más utilizado cuando sabes de antemano cuántas veces necesitas repetir la tarea. El bucle 'while' se ejecuta de forma indefinida hasta que la condición especificada deje de cumplirse.",
                                "Por otro lado, una función es una máquina o una receta de cocina guardada bajo un nombre. En vez de reescribir diez líneas de código cada vez que quieras ejecutar una acción o saludo, las agrupas en una función para poder llamarla con una sola línea cuando sea necesario.",
                                "Las funciones aumentan su utilidad mediante 'parámetros': datos de entrada que les proporcionas para que trabajen. Por ejemplo, en una función 'saludar(nombre)', puedes pasarle 'Ana' o 'Pedro' para personalizar el resultado sin alterar el código interno."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Observemos cómo interactúan ambas herramientas para realizar una tarea automatizada en segundos:",
                                "// 1. Declaramos una función reutilizable con un parámetro\nfunction enviarAlerta(usuario) {\n  console.log('Alerta de seguridad enviada a: ' + usuario);\n}\n\n// 2. Usamos un bucle para ejecutar la función de forma repetitiva con un contador\nfor (let i = 1; i <= 3; i++) {\n  enviarAlerta('Usuario #' + i);\n}",
                                "Al ejecutar el código, el sistema imprimirá tres mensajes secuenciales sin necesidad de haber escrito la instrucción de impresión de forma manual tres veces."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "El bucle infinito: Ocurre cuando no defines una condición de detención válida o no incrementas el contador. Al cumplirse siempre la condición, el bucle correrá para siempre, consumiendo la memoria y congelando el programa. ¡Asegúrate de que tus bucles siempre tengan un fin!",
                                "Declarar una función pero no invocarla: Escribir el código de la función solo guarda la receta. Si no escribes su nombre seguido de paréntesis (ej. 'miFuncion();'), las instrucciones internas nunca se ejecutarán."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En resumen: Los bucles automatizan acciones repetitivas controlando sus ciclos, mientras que las funciones agrupan y estructuran lógica reutilizable para mantener el código limpio y ordenado.",
                                "Tu acción del día: Crea el archivo 'contador.js'. Escribe un bucle 'for' que imprima los números del 1 al 10 en la consola. Después, pídele a tu IA: 'Dame un ejemplo práctico de cómo usar una función en JavaScript para calcular el IVA de diferentes precios'."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: Automatizar tareas repetitivas",
                        "questions": [
                            {
                                "question": "¿En qué situación es más adecuado usar un bucle 'while' en lugar de un bucle 'for'?",
                                "options": [
                                    "Cuando desconoces el número exacto de iteraciones o repeticiones necesarias de antemano.",
                                    "Cuando sabes exactamente el número de repeticiones que debe dar el contador.",
                                    "Cuando necesitas que la computadora genere un error de sintaxis controlado.",
                                    "Únicamente cuando la función no recibe ningún tipo de parámetro de entrada."
                                ],
                                "answer": 0,
                                "explanation": "El bucle 'while' se basa en una condición lógica externa. Es idóneo cuando no sabemos cuántas vueltas dará el ciclo antes de que la condición cambie a falso."
                            },
                            {
                                "question": "¿Qué representa un 'parámetro' en la declaración de una función?",
                                "options": [
                                    "Una variable interna que impide que el bucle se vuelva infinito de forma automática.",
                                    "Un dato o ingrediente de entrada que la función recibe para operar y personalizar su resultado.",
                                    "El nombre de extensión que se le asigna a los archivos en Visual Studio Code.",
                                    "La consola de comandos del navegador donde se imprimen los errores."
                                ],
                                "answer": 1,
                                "explanation": "Los parámetros son los valores variables que le ingresamos a una función al invocarla para que su lógica se ejecute de forma dinámica."
                            },
                            {
                                "question": "¿Qué sucede en tu programa si escribes una función detallada pero olvidas llamarla o invocarla?",
                                "options": [
                                    "La computadora la ejecuta automáticamente al iniciar la lectura del código.",
                                    "El código de la función nunca se ejecutará, quedando guardado pero inactivo.",
                                    "Se generará un bucle infinito que colapsará el navegador de inmediato.",
                                    "El editor de código borrará el archivo por considerarlo innecesario."
                                ],
                                "answer": 1,
                                "explanation": "Declarar la función define la receta de pasos. Si no la invocas explícitamente usando su nombre y paréntesis, la computadora nunca ejecutará esas líneas."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad Práctica: El Entrenador Virtual Personalizado",
                        "type": "Text",
                        "question": "<p>¡Es hora de hacer que la computadora trabaje por ti! En esta actividad programarás la lógica central para una aplicación de rendimiento deportivo.</p><p><strong>Tu objetivo:</strong> Escribir un script en JavaScript que combine una función con parámetros y un bucle <code>for</code> para generar rutinas de entrenamiento automáticas.</p><p><strong>Instrucciones:</strong></p><ol><li>Define una función llamada <code>generarRutina</code> que acepte dos parámetros: <code>nombreEjercicio</code> (un texto) y <code>totalRepeticiones</code> (un número).</li><li>Dentro de la función, escribe un bucle <code>for</code> que cuente desde 1 hasta el número almacenado en <code>totalRepeticiones</code>.</li><li>En cada ciclo del bucle, imprime en la consola: <em>\"Ejecutando [nombreEjercicio]... Repetición X de Y\"</em> (reemplazando por tus variables).</li><li>Al terminar el bucle (fuera del ciclo, pero dentro de la función), imprime un mensaje de felicitación: <em>\"¡Excelente! Ejercicio [nombreEjercicio] completado.\"</em></li><li>Invoca la función al menos dos veces con datos diferentes. Ejemplo:<ul><li><code>generarRutina('Sentadillas', 3)</code></li><li><code>generarRutina('Flexiones', 5)</code></li></ul></li></ol><p><strong>¿Qué debes entregar?</strong></p><p>Copia y pega tu código completo en el cuadro de texto. Asegúrate de incluir las llamadas a la función para verificar su correcto funcionamiento.</p>"
                    }
                }
            ]
        },
        {
            "title": "Módulo 5: Despliegue: Tu web interactiva en vivo",
            "lessons": [
                {
                    "title": "HTML, JS y GitHub Pages: Publica tu web gratis",
                    "objective": "Unificar variables, funciones y lógica condicional con HTML para estructurar un sitio interactivo y desplegarlo en internet.",
                    "sections": [
                        {
                            "heading": "Introducción",
                            "paragraphs": [
                                "¡Felicidades por tu constancia! Has pasado de conocer los conceptos básicos a estar listo para desplegar tu primer sitio web real. En esta lección uniremos la estructura visual (HTML) con el motor lógico (JavaScript) y la facilidad de publicación gratuita en internet.",
                                "Crearemos un 'Decisor de Dilemas': una aplicación interactiva que ayuda a tomar determinaciones rápidas y lúdicas aplicando lógica de programación en tiempo real."
                            ]
                        },
                        {
                            "heading": "Explicación principal",
                            "paragraphs": [
                                "Un desarrollo web funcional requiere dos componentes coordinados: la estructura física y el comportamiento. Estructuramos con HTML, definiendo la ubicación de textos, entradas de datos y botones. El comportamiento se define mediante JavaScript, controlando lo que sucede en pantalla cuando el usuario interactúa.",
                                "Vinculamos ambos mundos mediante eventos de HTML como 'onclick'. Este evento avisa al navegador: 'Cuando el usuario presione este botón, ejecuta esta función de JavaScript'.",
                                "Cuando tu desarrollo funcione de forma local, utilizaremos GitHub Pages. Es una plataforma gratuita que actúa como almacenamiento público para que tu página web esté en línea mediante un enlace que puedes compartir con cualquiera."
                            ]
                        },
                        {
                            "heading": "Ejemplo práctico",
                            "paragraphs": [
                                "Crea un archivo llamado 'index.html' en tu editor, copia este código unificado y guárdalo:",
                                "<!DOCTYPE html>\n<html>\n<head>\n  <title>Mi Decisor Inteligente</title>\n  <style>body { font-family: sans-serif; text-align: center; margin-top: 50px; }</style>\n</head>\n<body>\n  <h1>El Decisor de Dilemas 🔮</h1>\n  <p>Escribe tu duda (ej. ¿Debo entrenar hoy?):</p>\n  <input type='text' id='pregunta' placeholder='Escribe aquí...'>\n  <button onclick='tomarDecision()'>Decidir mi destino</button>\n  <h3 id='resultado'></h3>\n\n  <script>\n    function tomarDecision() {\n      let duda = document.getElementById('pregunta').value;\n      if (duda === '') {\n        document.getElementById('resultado').innerText = 'Por favor, escribe algo primero.';\n        return;\n      }\n      let opciones = ['¡Sí, hazlo ahora!', 'Mejor no te arriesgues', 'Piénsalo dos veces', 'Definitivamente no.'];\n      let seleccion = opciones[Math.floor(Math.random() * opciones.length)];\n      document.getElementById('resultado').innerText = 'Para tu duda \"' + duda + '\", la respuesta es: ' + seleccion;\n    }\n  </script>\n</body>\n</html>",
                                "Para probarlo de inmediato, haz doble clic en tu archivo 'index.html'. Tu navegador abrirá la interfaz y podrás interactuar con ella de manera local."
                            ]
                        },
                        {
                            "heading": "Errores comunes",
                            "paragraphs": [
                                "No nombrar el archivo principal como 'index.html': Si usas mayúsculas o nombres diferentes, los servidores de internet no encontrarán la raíz del sitio y mostrarán un error '404 Not Found'.",
                                "Discrepancia de nombres entre HTML y JS: Si en tu botón HTML defines 'onclick=\"tomarDecision()\"' pero en JavaScript declaras 'function tomardecision()' (con d minúscula), la ejecución fallará. JavaScript distingue mayúsculas de minúsculas de manera estricta. Presiona F12 en tu navegador para inspeccionar errores en la consola si algo no funciona."
                            ]
                        },
                        {
                            "heading": "Mini resumen y acción recomendada",
                            "paragraphs": [
                                "En esta lección conectamos la interfaz con la lógica de control para dar vida a una aplicación web real, lista para la nube. No requieres memorizar estructuras, sino saber cómo vincular los elementos esenciales.",
                                "Tu reto: Personaliza la aplicación usando Inteligencia Artificial. Copia el código en tu IA y usa este prompt: 'Ayúdame a mejorar este index.html. Quiero agregarle un diseño visual atractivo con CSS de estilo modo oscuro y añadir una opción de respuesta adicional en la lista de JavaScript. Explícame en qué línea exacta debo reemplazar la versión anterior'."
                            ]
                        }
                    ],
                    "quiz": {
                        "title": "Quiz: ¡Tu primer proyecto web real!",
                        "questions": [
                            {
                                "question": "¿Por qué es fundamental nombrar 'index.html' (en minúsculas) al archivo principal de tu sitio?",
                                "options": [
                                    "Porque es el estándar que buscan los servidores de hosting por defecto para cargar tu sitio web en la raíz.",
                                    "Porque es obligatorio para que el navegador ejecute los estilos CSS de forma predeterminada.",
                                    "Para evitar que la IA confunda el archivo con un script de base de datos.",
                                    "Únicamente para que el archivo sea visible en Visual Studio Code."
                                ],
                                "answer": 0,
                                "explanation": "Los servidores web buscan por convención el archivo index.html para mostrarlo como pantalla de bienvenida de la dirección del sitio."
                            },
                            {
                                "question": "¿Qué atributo HTML empleamos para invocar una función de JavaScript cuando un usuario presiona un botón?",
                                "options": [
                                    "placeholder",
                                    "onclick",
                                    "href",
                                    "style"
                                ],
                                "answer": 1,
                                "explanation": "El evento 'onclick' detecta la interacción táctil o clic de un mouse y corre de inmediato la lógica vinculada de JavaScript."
                            },
                            {
                                "question": "Si tu aplicación web no responde a la interacción, ¿cuál es el primer paso de depuración recomendado?",
                                "options": [
                                    "Abrir las herramientas de desarrollo con F12 y revisar la pestaña de Consola.",
                                    "Cambiar de editor de código de forma inmediata.",
                                    "Comprimir el archivo en un formato ZIP.",
                                    "Eliminar la etiqueta script de HTML."
                                ],
                                "answer": 0,
                                "explanation": "La consola del navegador (F12) te muestra detalladamente las alertas, errores de sintaxis y llamadas inválidas en tiempo real."
                            }
                        ]
                    },
                    "assignment": {
                        "title": "Actividad: Personaliza y Dale Vida a tu Propio Decisor de Dilemas",
                        "type": "Text",
                        "question": "<p>¡Llegó la hora de la verdad! Tomarás el código base del <strong>Decisor de Dilemas</strong> y lo personalizarás para que resuelva un problema real o divertido (por ejemplo: ¿Qué cenar hoy?, ¿Qué serie ver?, o ¿Qué lenguaje aprender primero?).</p><p><strong>Sigue estos pasos:</strong></p><ol><li>Modifica el título, los textos de descripción y las preguntas en el HTML para que combinen con la temática que seleccionaste.</li><li>Modifica el listado de <code>opciones</code> en JavaScript con al menos <strong>5 respuestas creativas</strong> de tu propia autoría.</li><li>Personaliza los estilos CSS dentro de la etiqueta <code>&lt;style&gt;</code> (colores, fondos, botones). Puedes usar la IA con el prompt sugerido en la lección para obtener un diseño moderno.</li><li>Prueba tu archivo <code>index.html</code> de forma local en tu navegador para verificar que todo responda perfectamente.</li></ol><p><strong>¿Qué debes entregar?</strong></p><p>Copia y pega en la caja de texto el <strong>código completo</strong> de tu archivo <code>index.html</code> personalizado (que incluya HTML, CSS y la lógica modificada de JavaScript).</p>"
                    }
                }
            ]
        }
    ],
    "final_project": {
        "title": "Proyecto Final: Tu Portal Web Interactivo y Publicado en Internet",
        "type": "Document",
        "question": "<p>¡Felicidades por llegar al reto de consolidación final! Has aprendido a estructurar código, dotarlo de lógica condicional y conectarlo con una interfaz de usuario real.</p><h3>El Reto: Construir tu \"Asistente de Planificación Inteligente\"</h3><p>Desarrollarás una aplicación web interactiva (un solo archivo <code>index.html</code>) que integre diseño adaptativo moderno y dos utilidades lógicas en pantalla:</p><ol><li><strong>Herramienta 1: Calculadora de Gastos Grupales (Lógica Matemática):</strong> Permite ingresar un monto monetario total y la cantidad de personas. El sistema calculará la división equitativa de gastos. Debe validar mediante un condicional (<code>if</code>/<code>else</code>) que los valores ingresados sean mayores a cero; si no lo son, mostrará una advertencia clara en pantalla.</li><li><strong>Herramienta 2: Recomendador de Metas Diarias (Lógica de Arrays y Funciones):</strong> Un módulo interactivo que elija aleatoriamente una meta de productividad, estudio o bienestar de una lista (un array de mínimo 5 elementos) al presionar un botón.</li></ol><h3>Flujo de Trabajo Guiado por IA:</h3><ul><li><strong>Estructura lógica:</strong> Define el maquetado en HTML y las funciones de JavaScript que hagan operar a ambos módulos.</li><li><strong>Estilizado moderno:</strong> Puedes utilizar un prompt para apoyarte con la IA: <em>\"Tengo este código de mi sitio web [pega tu código]. Genera estilos CSS limpios, modernos y adaptables para dispositivos móviles con una combinación de colores atractiva y explicaciones de dónde colocarlos.\"</em></li><li><strong>Despliegue:</strong> Sube tu desarrollo a un repositorio de GitHub y activa GitHub Pages para dejar la aplicación web operativa en la nube de manera gratuita.</li></ul><h3>¿Qué debes entregar?</h3><p>Copia y pega en el cuadro de texto los siguientes entregables organizados de forma clara:</p><ul><li><strong>1. El código completo de tu archivo <code>index.html</code></strong> (HTML, estilos CSS personalizados y JavaScript integrado).</li><li><strong>2. El enlace público (URL) de tu aplicación</strong> (el enlace web de GitHub Pages funcionando para poder auditar el proyecto en tiempo real).</li><li><strong>3. Tu Bitácora de Co-creación con IA</strong> (un texto breve de 3 o 4 líneas que detalle un prompt de valor utilizado para corregir un bug, mejorar los estilos visuales o pulir alguna funcionalidad, indicando qué aprendiste en el proceso).</li></ul>"
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
