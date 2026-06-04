with open("app.py", "r") as f:
    text = f.read()

# Fix canvas background error
new_bg = """def _draw_bg(event=None):
            if not bg_canvas.winfo_exists(): return
            bg_canvas.delete("all")"""

text = text.replace('def _draw_bg(event=None):\n            bg_canvas.delete("all")', new_bg)

with open("app.py", "w") as f:
    f.write(text)

