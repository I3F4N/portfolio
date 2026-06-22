import re

# 1. Update style.css for PC UI
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pc_ui_css = """
        /* PC UI Optimizations */
        @media (min-width: 769px) {
            /* Disable expand/collapse for Skills and Projects on Desktop since they fit well */
            #skills-container, #projects-container {
                max-height: none !important;
                overflow: visible !important;
            }
            #toggle-skills-wrapper, #skills-container + .expand-fade,
            #toggle-projects-wrapper, #projects-container + .expand-fade {
                display: none !important;
            }
            #skills-grid {
                padding-bottom: 1rem !important;
            }
            #project-grid {
                padding-bottom: 1rem !important;
            }
        }
"""

if "/* PC UI Optimizations */" not in css:
    css += pc_ui_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update script.js for Matrix FPS
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace > 33 with > 8 to support 120 FPS natively (requestAnimationFrame runs at monitor Hz)
js = js.replace('if (time - lastTime > 33) {', 'if (time - lastTime > 8) {')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Applied PC UI updates and unlocked Matrix FPS.")
