import re

def update_file(filename, replacements):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find segment in {filename}:\n{old[:50]}...")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

js_old = """            let toggleCertsBtn = document.getElementById('toggle-certs-btn');
            const fadeEl = document.getElementById('cert-fade');
            
            const updateLayout = () => {"""

js_new = """            let toggleCertsBtn = document.getElementById('toggle-certs-btn');
            const fadeEl = document.getElementById('cert-fade');
            const certificatesContainer = document.getElementById('certificates-container');
            
            const updateLayout = () => {"""

update_file('script.js', [(js_old, js_new)])

print("ReferenceError fixed.")
