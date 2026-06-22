import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace main-content with layout-wrapper for the unhiding logic
js = js.replace("const mainContent = document.getElementById('main-content');", "const mainContent = document.getElementById('layout-wrapper');")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js to unhide layout-wrapper.")
