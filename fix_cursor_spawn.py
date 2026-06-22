import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add list-none to nav-list to remove default HTML list dots
html = html.replace('ul id="nav-list" class="space-y-1 relative z-10 w-full pb-12"', 'ul id="nav-list" class="space-y-1 relative z-10 w-full pb-12 list-none"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 2. Add default opacity 0 to custom cursor to hide it on spawn
css = css.replace('#custom-cursor {\n            position: fixed;', '#custom-cursor {\n            position: fixed;\n            opacity: 0;')
css = css.replace('#cursor-dot {\n            position: fixed;', '#cursor-dot {\n            position: fixed;\n            opacity: 0;')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 3. Add JS to reveal cursor on first mouse movement
reveal_logic = """
        // Reveal custom cursor only when mouse moves
        let cursorRevealed = false;
        document.addEventListener('mousemove', (e) => {
            if (!cursorRevealed) {
                cursor.style.opacity = '1';
                cursorDot.style.opacity = '1';
                cursorRevealed = true;
            }
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            cursorDot.style.left = e.clientX + 'px';
            cursorDot.style.top = e.clientY + 'px';
        });"""

# Replace old mousemove logic
old_mousemove = """        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            cursorDot.style.left = e.clientX + 'px';
            cursorDot.style.top = e.clientY + 'px';
        });"""

js = js.replace(old_mousemove, reveal_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed default dots and cursor spawn visibility.")
