import re

# 1. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Font & Background
css = css.replace('font-family: \'Inter\', sans-serif;', 'font-family: \'Space Grotesk\', sans-serif;')
if "font-family: 'Space Grotesk'" not in css:
    css = css.replace('body {', 'body {\n            font-family: \'Space Grotesk\', sans-serif;')

css = css.replace('background-color: #07090c; /* Deep premium slate/black */', 'background-color: #000000; /* Pure Black for infinite contrast */')

# Matrix Opacity
css = css.replace('opacity: 0.05; /* Barely visible, premium dark mode feel */', 'opacity: 0.15; mix-blend-mode: screen; /* Sharper identity */')

# Cursor CSS
cursor_css = """
        /* High-End Custom Cursor */
        body { cursor: none; }
        a, button { cursor: none; }
        
        #custom-cursor {
            position: fixed;
            top: 0;
            left: 0;
            width: 40px;
            height: 40px;
            border: 1px solid rgba(34, 197, 94, 0.5);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s, background-color 0.3s, border 0.3s;
            mix-blend-mode: difference;
        }
        #custom-cursor.hover {
            width: 80px;
            height: 80px;
            background-color: #22c55e;
            border-color: transparent;
        }
        
        #cursor-dot {
            position: fixed;
            top: 0;
            left: 0;
            width: 6px;
            height: 6px;
            background-color: #22c55e;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s;
        }
        #cursor-dot.hover {
            opacity: 0;
        }
"""
if "/* High-End Custom Cursor */" not in css:
    # replace old cursor css if exists
    if "#custom-cursor {" in css:
        css = re.sub(r'#custom-cursor \{.*?(?=/*)', cursor_css, css, flags=re.DOTALL)
    else:
        css += cursor_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 2. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update JS-generated cards
old_proj_card = 'class="project-card bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 hover:border-white/10 transition-colors'
new_proj_card = 'class="project-card bg-[#050505] border border-green-500/20 shadow-lg hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500'
js = js.replace(old_proj_card, new_proj_card)

old_cert_card = 'class="card-bg absolute inset-0 bg-[#0d1117]/60 backdrop-blur-xl rounded-xl border border-white/5 hover:border-white/10 transition-colors'
new_cert_card = 'class="card-bg absolute inset-0 bg-[#050505] rounded-xl border border-green-500/20 hover:border-green-500/60 transition-all duration-500'
js = js.replace(old_cert_card, new_cert_card)

# Update Cursor Logic
# Find the old mousemove listener and replace it entirely to include trailing logic
old_mouse_logic = """        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Spotlight effect
            spotlight.style.background = `radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(34, 197, 94, 0.05) 0%, transparent 50%)`;
            
            // Custom cursor
            cursor.style.left = mouseX + 'px';
            cursor.style.top = mouseY + 'px';
        });"""

new_mouse_logic = """        let cursorX = 0;
        let cursorY = 0;
        const cursorDot = document.getElementById('cursor-dot');
        
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Spotlight effect
            spotlight.style.background = `radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(34, 197, 94, 0.05) 0%, transparent 50%)`;
            
            // Dot follows exactly
            if (cursorDot) {
                cursorDot.style.left = mouseX + 'px';
                cursorDot.style.top = mouseY + 'px';
            }
        });
        
        // Trailing animation loop for the outer cursor
        function renderCursor() {
            cursorX += (mouseX - cursorX) * 0.15;
            cursorY += (mouseY - cursorY) * 0.15;
            if (cursor) {
                cursor.style.left = cursorX + 'px';
                cursor.style.top = cursorY + 'px';
            }
            requestAnimationFrame(renderCursor);
        }
        renderCursor();
        
        // Hover effects
        const interactiveElements = document.querySelectorAll('a, button, .project-card, .certificate-card, .experience-card');
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.classList.add('hover');
                if (cursorDot) cursorDot.classList.add('hover');
            });
            el.addEventListener('mouseleave', () => {
                cursor.classList.remove('hover');
                if (cursorDot) cursorDot.classList.remove('hover');
            });
        });
        
        // Ensure dynamically rendered elements get the hover effect via mutation observer or event delegation
        document.body.addEventListener('mouseover', (e) => {
            const target = e.target.closest('a, button, .project-card, .certificate-card, .experience-card');
            if (target) {
                cursor.classList.add('hover');
                if (cursorDot) cursorDot.classList.add('hover');
            }
        });
        document.body.addEventListener('mouseout', (e) => {
            const target = e.target.closest('a, button, .project-card, .certificate-card, .experience-card');
            if (target) {
                cursor.classList.remove('hover');
                if (cursorDot) cursorDot.classList.remove('hover');
            }
        });"""

if "document.addEventListener('mousemove'" in js and "function renderCursor" not in js:
    # Just replace the basic mouse listener block
    js = re.sub(r'        document\.addEventListener\(\'mousemove\', \(e\) => \{.*?\}\);', new_mouse_logic, js, flags=re.DOTALL)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated CSS and JS for Mormal aesthetics.")
