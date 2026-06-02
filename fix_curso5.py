import re

with open(r"C:\Users\troll\Documents\studybadge\lms\curso5.py", "r", encoding="utf-8") as f:
    text = f.read()

count = 1
def repl(m):
    global count
    res = f"Pregunta de repaso {count}?"
    count += 1
    return res

text = re.sub(r"¿Cuál es una idea importante de la lección 1\?", repl, text)

with open(r"C:\Users\troll\Documents\studybadge\lms\curso5.py", "w", encoding="utf-8") as f:
    f.write(text)
