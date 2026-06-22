import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix Custom Cursor
cursor_css = """#custom-cursor {
            position: fixed;
            top: 0;
            left: 0;
            width: 40px;
            height: 40px;
            border: 2px solid rgba(34, 197, 94, 0.8);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s, background-color 0.3s, border 0.3s;
        }
        #custom-cursor.hover {
            width: 80px;
            height: 80px;
            background-color: rgba(34, 197, 94, 0.1);
            border-color: rgba(34, 197, 94, 1);
        }
        
        #cursor-dot {
            position: fixed;
            top: 0;
            left: 0;
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 1);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s;
        }"""

css = re.sub(r'#custom-cursor\s*\{.*?(?=#cursor-dot\.hover \{.*?})', cursor_css + '\n        ', css, flags=re.DOTALL)
# The regex above might be tricky. It's safer to just replace mix-blend-mode directly.

# Safer replacement:
css = css.replace('mix-blend-mode: difference;', '')
css = css.replace('border: 1px solid rgba(34, 197, 94, 0.5);', 'border: 2px solid rgba(34, 197, 94, 0.8);')
css = css.replace('width: 6px;\n            height: 6px;\n            background-color: #22c55e;', 'width: 8px;\n            height: 8px;\n            background-color: #22c55e;\n            box-shadow: 0 0 10px rgba(34, 197, 94, 1);')

# The hover state background:
css = css.replace('background-color: #22c55e;\n            border-color: transparent;', 'background-color: rgba(34, 197, 94, 0.1);\n            border-color: rgba(34, 197, 94, 1);')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed cursor in style.css")
