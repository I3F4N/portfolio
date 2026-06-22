import re

# 1. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Card styles
old_card = 'class="project-card bg-[#161b22]/70'
new_card = 'class="project-card bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 hover:border-white/10 transition-colors'
js = js.replace(old_card, new_card)

old_cert = 'class="certificate-card group relative h-64 perspective-1000"'
new_cert = 'class="certificate-card group relative h-64 perspective-1000" style="perspective: 1000px;"'
old_cert_bg = 'class="card-bg absolute inset-0 bg-[#161b22]/70 rounded-md border border-gray-700'
new_cert_bg = 'class="card-bg absolute inset-0 bg-[#0d1117]/60 backdrop-blur-xl rounded-xl border border-white/5 hover:border-white/10 transition-colors'
js = js.replace(old_cert_bg, new_cert_bg)

# Text styles inside JS
js = js.replace('text-blue-400', 'text-gray-100')
js = js.replace('text-gray-400', 'text-gray-400') # keeping this

# Boot sequence speed up (approx 5x faster)
js = js.replace('await typeText("Booting secure portfolio environment...", 30);', 'await typeText("Booting secure portfolio environment...", 5);')
js = js.replace('await sleep(500);', 'await sleep(100);')
js = js.replace('await typeText("Establishing secure connection...", 20);', 'await typeText("Establishing secure connection...", 4);')
js = js.replace('await sleep(300);', 'await sleep(50);')
js = js.replace('await typeText("Decrypting payload...", 20);', 'await typeText("Decrypting payload...", 4);')
js = js.replace('await sleep(1000);', 'await sleep(200);')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add matrix opacity rule
matrix_opacity = """
        #matrix-canvas {
            opacity: 0.05; /* Barely visible, premium dark mode feel */
        }
"""
if "#matrix-canvas {" not in css:
    css += matrix_opacity

# Darken body background slightly to make sure contrast is high
css = css.replace('background-color: #0d1117;', 'background-color: #07090c; /* Deep premium slate/black */')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated JS and CSS for premium aesthetics.")
