import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Fonts to Space Grotesk (Modern, Geometric, Techy but High-End)
html = html.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Space+Grotesk:wght@300;400;600;700&display=swap" rel="stylesheet">'
)

# 2. Add cursor dot element for the trailing effect
if '<div id="cursor-dot"></div>' not in html:
    html = html.replace('<div id="custom-cursor"></div>', '<div id="custom-cursor"></div>\n    <div id="cursor-dot"></div>')

# 3. Update Cards to be solid black with stark borders instead of murky glassmorphism
# Experience cards
html = html.replace('bg-[#0d1117]/60 backdrop-blur-xl border border-white/5', 'bg-[#050505] border border-green-500/20 shadow-lg')
# Also hover state
html = html.replace('hover:border-white/10 transition-colors', 'hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500')

# Skills & Projects container backgrounds
html = html.replace('bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 p-6 rounded-xl hover:border-white/10 transition-colors', 'bg-[#050505] border border-gray-800 p-6 rounded-xl shadow-2xl')
html = html.replace('bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 p-8 rounded-xl hover:border-white/10 transition-colors', 'bg-[#050505] border border-gray-800 p-8 rounded-xl shadow-2xl')

# 4. Make Headings massive
html = html.replace('text-3xl font-bold', 'text-5xl font-bold tracking-tight')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html for Mormal aesthetics.")
