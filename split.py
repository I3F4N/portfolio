import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract styles
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    styles = style_match.group(1).strip()
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(styles)
    content = content.replace(style_match.group(0), '<link rel="stylesheet" href="style.css">')

# Extract the main script. The script we want to extract is the last <script> block.
# We'll find all <script>...</script> blocks
script_matches = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
if script_matches:
    # The last one is the custom logic
    last_script = script_matches[-1]
    script_content = last_script.group(1).strip()
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    content = content.replace(last_script.group(0), '<script src="script.js" defer></script>')

# Defer other external scripts
content = content.replace('<script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>', '<script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js" defer></script>')
content = content.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.7.77/Tone.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.7.77/Tone.js" defer></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Split complete.")
