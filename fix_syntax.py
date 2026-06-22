import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix duplicate const declarations
js = js.replace("const mobileNavbar = document.getElementById('mobile-navbar');\n            const mobileNavbar = document.getElementById('mobile-navbar');", "const mobileNavbar = document.getElementById('mobile-navbar');")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed syntax error.")
