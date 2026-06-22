import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the class on certificates container
html = html.replace('<div id="certificates-container" class="certificates-container">', '<div id="certificates-container" class="expandable-container">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed certificates container class.")
