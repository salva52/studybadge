import glob
import os

files = glob.glob(r"C:\Users\troll\Documents\studybadge\lms\*.py")

old_func = """def list_block(items, style="unordered"):
    clean_items = [str(item).strip() for item in (items or []) if str(item or "").strip()]
    if not clean_items:
        return None
    return {
        "type": "list",
        "data": {
            "style": style if style in {"ordered", "unordered"} else "unordered",
            "items": [{"content": item, "items": []} for item in clean_items],
        }
    }"""

new_func = """def list_block(items, style="unordered"):
    clean_items = [str(item).strip() for item in (items or []) if str(item or "").strip()]
    if not clean_items:
        return None
    return {
        "type": "list",
        "data": {
            "style": style if style in {"ordered", "unordered"} else "unordered",
            "items": [{"content": item, "items": []} for item in clean_items],
        }
    }"""

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Fixed: {os.path.basename(f)}")
