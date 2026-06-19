import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = """        #certificates-container.expanded {
            max-height: 2000px; /* Large enough for all certs */
        }"""
replacement = """        #certificates-container.expanded {
            max-height: 8000px; /* Needs to be larger to accommodate all cards without clipping */
        }"""

css = css.replace(target, replacement)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated max-height to 8000px.")
