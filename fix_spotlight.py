import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove spotlight
html = html.replace('<div id="spotlight"></div>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove spotlight css
css = re.sub(r'#spotlight \{.*?\n        \}\n', '', css, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove spotlight JS logic
js = js.replace('spotlight.style.background = `radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(34, 197, 94, 0.05) 0%, transparent 50%)`;', '')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Removed spotlight to fix black screen bug.")
