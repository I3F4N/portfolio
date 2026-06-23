import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace justify-center in interests-grid
old_interests = 'class="flex flex-wrap justify-center gap-4 bg-[#050505] border border-green-500/20 shadow-lg p-6 rounded-xl hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500" id="interests-grid"'
new_interests = 'class="flex flex-wrap gap-3 bg-[#050505] border border-green-500/20 shadow-lg p-6 rounded-xl hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500" id="interests-grid"'

if old_interests in html:
    html = html.replace(old_interests, new_interests)
    print("Fixed interests alignment.")
else:
    print("Warning: Could not find interests grid class.")

# Cache bust
import time
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
