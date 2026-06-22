import re

# 1. Update JS Variables
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("const outputEl = document.getElementById('output');", "let outputEl = document.getElementById('output');")
js = js.replace("const terminalBody = document.getElementById('terminal-body');", "let terminalBody = document.getElementById('terminal-body');")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update About Section Text
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_about_text = "Cybersecurity &amp; Infrastructure Professional with comprehensive expertise spanning network architecture, operating systems, and software development — from physical layer to application level. Strong foundation in PC hardware, OS internals, and networking fundamentals. Specializes in designing secure, scalable IT environments by embedding security into infrastructure and application design from the ground up, rather than treating it as an afterthought. Focused on delivering efficient, secure solutions that solve business problems without adding friction for end users."

html = re.sub(r'<p data-scramble-text>.*?</p>', f'<p data-scramble-text>{new_about_text}</p>', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updates applied.")
