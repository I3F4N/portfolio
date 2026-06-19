import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = """        .certificates-fade {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: linear-gradient(to top, #0d1117, transparent);
            pointer-events: none;
            transition: opacity 0.5s ease;
            z-index: 5;
        }
         #certificates-container.expanded + .certificates-fade {
            opacity: 0;
        }"""

replacement = """        .certificates-fade {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: linear-gradient(to top, #0d1117, transparent);
            pointer-events: auto; /* Block hover on partially hidden bottom cards */
            transition: opacity 0.5s ease, pointer-events 0.5s ease;
            z-index: 5;
        }
         #certificates-container.expanded + .certificates-fade {
            opacity: 0;
            pointer-events: none; /* Allow interaction when expanded */
        }"""

css = css.replace(target, replacement)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated certificates-fade CSS successfully.")
