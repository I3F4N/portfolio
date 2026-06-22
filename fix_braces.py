import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add the missing closing braces for populateCertificates()
js = js.replace("                populateCertificates();\n            });\n        }", "                populateCertificates();\n            });\n        }\n            }\n        }")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed syntax error.")
