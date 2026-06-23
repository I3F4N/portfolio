import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the line that adds padding to certificate-card
old_rule = ".experience-card, .project-card, .certificate-card {\n                padding: 1.25rem !important;\n            }"
new_rule = ".experience-card, .project-card {\n                padding: 1.25rem !important;\n            }"

if old_rule in css:
    css = css.replace(old_rule, new_rule)
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Fixed style.css")
else:
    print("Warning: old_rule not found in style.css!")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
