import re

with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 109 in the file (index 108) is an orphaned `}`
if "}" in lines[108]:
    lines[108] = "\n"

with open('script.js', 'w', encoding='utf-8') as f:
    f.write("".join(lines))

print("Removed syntax error.")
