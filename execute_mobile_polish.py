import re

def update_file(filename, replacements):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find segment in {filename}:\n{old[:50]}...")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update index.html
index_old_navbar = """    <div class="fixed top-0 left-0 w-full bg-[#0d1117]/90 backdrop-blur-md border-b border-green-500/20 z-[70] lg:hidden flex justify-between items-center px-6 py-4" id="mobile-navbar">
        <div class="flex items-center gap-2"><span class="text-green-400 font-mono font-bold tracking-widest text-sm">~/irfan</span><span id="mobile-section-indicator" class="text-gray-500 font-mono text-xs hidden lg:hidden">/</span></div>"""

index_new_navbar = """    <div class="fixed top-0 left-0 w-full bg-[#0d1117]/90 backdrop-blur-md border-b border-green-500/20 z-[70] lg:hidden flex justify-between items-center px-6 py-4" id="mobile-navbar">
        <div class="flex items-center gap-2"><span class="text-green-400 font-mono font-bold tracking-widest text-sm">~/irfan</span><span id="mobile-section-indicator" class="text-gray-500 font-mono text-xs hidden lg:hidden">/</span><span class="animate-cursor-blink text-green-400 font-mono font-bold ml-1 hidden lg:hidden" id="mobile-cursor">_</span></div>
        <div id="mobile-progress-bar" class="absolute bottom-0 left-0 h-[2px] bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)] w-0 transition-all duration-150 ease-out z-[71]"></div>"""

update_file('index.html', [(index_old_navbar, index_new_navbar)])

# 2. Update style.css
css_old_hover = """            /* --- Disable hover transforms on mobile (perf) --- */
            .clickable-tag:hover, .project-card:hover,
            .certificate-card:hover, .experience-card:hover {
                transform: none !important;
                box-shadow: none !important;
            }"""

css_new_hover = """            /* --- Disable hover transforms on mobile (perf) --- */
            .clickable-tag:hover, .project-card:hover,
            .certificate-card:hover, .experience-card:hover {
                transform: none !important;
                box-shadow: none !important;
            }
            
            /* --- Mobile Tactile Feedback --- */
            .clickable-tag:active, .project-card:active,
            .certificate-card:active, .experience-card:active {
                transform: scale(0.98) !important;
                border-color: rgba(34, 197, 94, 0.5) !important;
                transition: transform 0.1s ease-out, border-color 0.1s ease-out !important;
            }"""

css_animations = """
/* Mobile Polish Animations */
@keyframes cursor-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
.animate-cursor-blink {
    animation: cursor-blink 1s step-end infinite;
}

.mobile-nav-item {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.4s ease, transform 0.4s ease;
}
.mobile-menu-active .mobile-nav-item {
    opacity: 1;
    transform: translateY(0);
}
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()
if 'animate-cursor-blink' not in css_content:
    with open('style.css', 'a', encoding='utf-8') as f:
        f.write(css_animations)
update_file('style.css', [(css_old_hover, css_new_hover)])

# 3. Update script.js
js_old_progress = """                    // 1. Check if we are at the absolute bottom of the page"""
js_new_progress = """                    // Update mobile scroll progress bar
                    const progressBar = document.getElementById('mobile-progress-bar');
                    if (progressBar && window.innerWidth < 1024) {
                        const scrollPercent = (window.scrollY / (document.body.offsetHeight - window.innerHeight)) * 100;
                        progressBar.style.width = scrollPercent + '%';
                    }

                    // 1. Check if we are at the absolute bottom of the page"""

js_old_cursor = """                                indicator.classList.remove('hidden');
                            }"""
js_new_cursor = """                                indicator.classList.remove('hidden');
                                const cursor = document.getElementById('mobile-cursor');
                                if (cursor) cursor.classList.remove('hidden');
                            }"""

js_old_menu_open = """                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');"""
js_new_menu_open = """                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');
                    // Add staggered cascade class
                    setTimeout(() => mobileNavList.classList.add('mobile-menu-active'), 50);"""

js_old_menu_close = """                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');"""
js_new_menu_close = """                                mobileNavList.classList.remove('mobile-menu-active');
                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');"""

js_old_menu_close_2 = """                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');"""
js_new_menu_close_2 = """                    mobileNavList.classList.remove('mobile-menu-active');
                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');"""

js_old_populate = """                const li = document.createElement('li');
                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block hover:text-white transition-colors" data-target="${sectionId}">
                                    <span class="mr-2 opacity-50">0${index + 1}.</span>${sectionTitle}
                                </a>`;
                mobileNavList.appendChild(li);"""

js_new_populate = """                const li = document.createElement('li');
                li.className = 'mobile-nav-item';
                li.style.transitionDelay = `${index * 0.08}s`;
                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block hover:text-white transition-colors" data-target="${sectionId}">
                                    <span class="mr-2 opacity-50">0${index + 1}.</span>${sectionTitle}
                                </a>`;
                
                // Add click listener so links actually close the menu on mobile!
                li.addEventListener('click', (e) => {
                    e.preventDefault();
                    lenis.scrollTo(`#${sectionId}`, { offset: -80 });
                    
                    const mobileMenu = document.getElementById('mobile-menu');
                    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                    const mobileNavList = document.getElementById('mobile-nav-list');
                    
                    if (mobileNavList) mobileNavList.classList.remove('mobile-menu-active');
                    if (mobileMenu) {
                        mobileMenu.classList.remove('opacity-100');
                        mobileMenu.classList.add('opacity-0');
                    }
                    if (mobileMenuBtn) {
                        mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    }
                    setTimeout(() => {
                        if (mobileMenu) {
                            mobileMenu.classList.add('hidden');
                            mobileMenu.classList.remove('flex');
                        }
                    }, 300);
                });
                
                mobileNavList.appendChild(li);"""

update_file('script.js', [
    (js_old_progress, js_new_progress),
    (js_old_cursor, js_new_cursor),
    (js_old_menu_open, js_new_menu_open),
    (js_old_menu_close, js_new_menu_close),
    (js_old_menu_close_2, js_new_menu_close_2),
    (js_old_populate, js_new_populate)
])
