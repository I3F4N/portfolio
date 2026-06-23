import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_click_logic = """                li.addEventListener('click', (e) => {
                    e.preventDefault();
                    lenis.scrollTo(`#${sectionId}`, { offset: -80, duration: 0.8 });
                    
                    const mobileMenu = document.getElementById('mobile-menu');
                    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                    const html = document.documentElement;
                    
                    if (mobileMenu) {
                        mobileMenu.classList.remove('active');
                        mobileMenu.classList.add('pointer-events-none');
                        mobileMenu.classList.replace('opacity-100', 'opacity-0');
                        setTimeout(() => {
                            mobileMenu.style.display = 'none';
                        }, 500);
                    }
                    if (mobileMenuBtn) {
                        mobileMenuBtn.classList.remove('open');
                    }
                    html.classList.remove('overflow-hidden');
                });"""

new_click_logic = """                li.addEventListener('click', (e) => {
                    e.preventDefault();
                    lenis.scrollTo(`#${sectionId}`, { offset: -80, duration: 0.8 });
                    
                    const mobileMenu = document.getElementById('mobile-menu');
                    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                    
                    // Trigger the exact same close logic as tapping the X button
                    if (mobileMenuBtn && mobileMenu && !mobileMenu.classList.contains('hidden')) {
                        mobileMenuBtn.click();
                    }
                });"""

if old_click_logic in js:
    js = js.replace(old_click_logic, new_click_logic)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed script.js")
else:
    print("Warning: old_click_logic not found in script.js!")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
