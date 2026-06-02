import glob
import os

files = glob.glob(r"C:\Users\troll\Documents\studybadge\lms\*.py")

old_func = """def delimiter_block():
    return paragraph_block("---")"""

new_func = """def delimiter_block():
    return paragraph_block("---")"""

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Fixed delimiter: {os.path.basename(f)}")
