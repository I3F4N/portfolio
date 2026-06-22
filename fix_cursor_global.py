import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the global cursor: none rules that were previously tied to the custom cursor
css = re.sub(r'body\s*\{\s*cursor:\s*none;\s*\}', '', css)
css = re.sub(r'a,\s*button\s*\{\s*cursor:\s*none;\s*\}', '', css)
css = re.sub(r'\*:(not\(input,\s*textarea\))\s*\{\s*cursor:\s*none;\s*\}', '', css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Removed cursor: none globals.")
