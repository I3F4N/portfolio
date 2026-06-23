import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update font size logic for matrix
old_font_logic = """        const fontSize = 16;
        let columns = Math.floor(width / fontSize);"""

new_font_logic = """        const fontSize = window.innerWidth < 768 ? 22 : 16; // Larger font on mobile = fewer calculations = better performance
        let columns = Math.floor(width / fontSize);"""

js = js.replace(old_font_logic, new_font_logic)

# 2. Revert the pause-on-scroll logic and use a steady 30fps
old_matrix = """        function animateMatrix(time) {
            // Completely pause matrix on scroll for huge performance gains on weak devices
            if (isTabActive && !isScrolling) {
                const interval = 40; // ~25fps idle
                if (time - lastTime > interval) {
                    drawMatrix();
                    lastTime = time;
                }
            }
            requestAnimationFrame(animateMatrix);
        }"""

new_matrix = """        function animateMatrix(time) {
            if (isTabActive) {
                const interval = 33; // Steady ~30fps
                if (time - lastTime > interval) {
                    drawMatrix();
                    lastTime = time;
                }
            }
            requestAnimationFrame(animateMatrix);
        }"""

js = js.replace(old_matrix, new_matrix)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
