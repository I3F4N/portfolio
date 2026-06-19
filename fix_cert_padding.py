import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">'
replacement = '<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">'

html = html.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added bottom padding to certificate grid.")
