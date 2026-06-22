import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Cursor
cursor_html = """
    <!-- Custom Cursor -->
    <div id="custom-cursor"></div>
    <div id="cursor-dot"></div>

    <!-- Matrix Canvas sits absolutely in the background -->"""
if '<div id="custom-cursor"></div>' not in html:
    html = html.replace('<!-- Matrix Canvas sits absolutely in the background -->', cursor_html)

# 2. Setup Minimap Container
old_nav = r'<nav id="desktop-nav".*?</nav>'
new_nav = """<div class="flex flex-col items-end opacity-50 hover:opacity-100 transition-opacity duration-500">
                        <div class="text-[10px] font-mono text-gray-500 mb-2 tracking-widest text-right w-full uppercase border-b border-gray-800 pb-1">Map // Root</div>
                        <div id="minimap-container" class="relative w-16 h-[500px] border-r border-gray-800 cursor-pointer overflow-hidden rounded-sm"></div>
                    </div>"""
html = re.sub(old_nav, new_nav, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html for cursor and minimap container.")
