import re

# 1. Add cursor-pointer to script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_tag1 = "tag.className = `skill-tag bg-[#161b22]/50 border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2`;"
new_tag1 = "tag.className = `skill-tag bg-[#161b22]/50 border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2 cursor-pointer`;"

old_tag2 = "tag.className = `skill-tag border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2`;"
new_tag2 = "tag.className = `skill-tag border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2 cursor-pointer`;"

js = js.replace(old_tag1, new_tag1)
js = js.replace(old_tag2, new_tag2)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js")


# 2. Add cursor-pointer to index.html projects
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Projects are div elements with onclick='openModal(...)'
# We will use regex to find class="..." inside those div tags and inject cursor-pointer if it's not there.
def inject_cursor(match):
    tag = match.group(0)
    if 'cursor-pointer' not in tag:
        tag = tag.replace('class="', 'class="cursor-pointer ')
    return tag

# Find all divs with onclick="openModal
html = re.sub(r'<div[^>]*onclick="openModal[^>]*>', inject_cursor, html)

# Cache bust
import time
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")
