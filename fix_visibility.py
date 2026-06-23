import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the incorrect className string
old_line = "li.className = `transform translate-y-4 opacity-0 transition-all duration-300 ease-out ${colSpan}`;"
new_line = "li.className = `mobile-nav-item ${colSpan}`;"

if old_line in js:
    js = js.replace(old_line, new_line)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed script.js")
else:
    print("Warning: old_line not found in script.js!")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
