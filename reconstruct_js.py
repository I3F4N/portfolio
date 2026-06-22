import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update JS generated cards to minimalist border-gray-900 default, heavy green hover
old_proj_card = 'class="project-card bg-[#050505] border border-green-500/20 shadow-lg hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500'
new_proj_card = 'class="project-card bg-[#050505] border border-gray-900 hover:border-green-500/80 hover:-translate-y-3 hover:shadow-[0_0_40px_rgba(34,197,94,0.2)] transition-all duration-500'
js = js.replace(old_proj_card, new_proj_card)

old_cert_card = 'class="card-bg absolute inset-0 bg-[#050505] rounded-xl border border-green-500/20 hover:border-green-500/60 transition-all duration-500'
new_cert_card = 'class="card-bg absolute inset-0 bg-[#050505] rounded-xl border border-gray-900 hover:border-green-500/80 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500'
js = js.replace(old_cert_card, new_cert_card)

# 2. Fix Boot Sequence Logic
# Since we removed the terminal window, we need to hide the boot overlay after it finishes
js = js.replace('mainContent.classList.remove(\'hidden\');', 'const bootOverlay = document.getElementById("boot-overlay");\n                if(bootOverlay) bootOverlay.classList.add("opacity-0");\n                setTimeout(() => {\n                    if(bootOverlay) bootOverlay.style.display = "none";\n                    mainContent.classList.remove(\'hidden\');\n', 1)
# and add the closing brace for setTimeout
js = js.replace('setTimeout(() => mainContent.classList.add(\'opacity-100\'), 50);', 'setTimeout(() => mainContent.classList.add(\'opacity-100\'), 50);\n                }, 1000);')

# In skipBootSequence
js = js.replace('mainContent.classList.remove(\'hidden\');', 'const bootOverlay = document.getElementById("boot-overlay");\n            if(bootOverlay) {\n                bootOverlay.classList.add("opacity-0");\n                setTimeout(() => bootOverlay.style.display = "none", 500);\n            }\n            mainContent.classList.remove(\'hidden\');', 1)

# 3. Active state for the new sticky sidebar navigation
active_nav_logic = """
        // Scroll spy for sticky sidebar navigation
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('#desktop-nav .nav-link');
        
        lenis.on('scroll', (e) => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 300) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                const span = link.querySelector('span');
                if (link.getAttribute('href').includes(current)) {
                    link.classList.add('text-white');
                    link.classList.remove('text-gray-500');
                    if(span) { span.style.width = '1rem'; span.style.marginRight = '1rem'; }
                } else {
                    link.classList.remove('text-white');
                    link.classList.add('text-gray-500');
                    if(span) { span.style.width = '0'; span.style.marginRight = '0'; }
                }
            });
        });
"""
if "// Scroll spy for sticky sidebar navigation" not in js:
    js += active_nav_logic


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js for layout interactions.")
