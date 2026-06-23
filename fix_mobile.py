import re

# ============================================================
# COMPREHENSIVE MOBILE EXPERIENCE OVERHAUL
# ============================================================

# --- STYLE.CSS ---
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the existing mobile media query with a comprehensive one
old_mobile = """        /* Mobile Typography & Readability Optimization */
        @media (max-width: 768px) {
            html { font-size: 14px; } /* Base font size reduction */
            body {
            font-family: 'Space Grotesk', sans-serif; line-height: 1.5; }
            h1.glitch-title { font-size: 2.5rem !important; }
            h2.glitch-title { font-size: 1.75rem !important; margin-bottom: 1rem !important; }
            h3 { font-size: 1.25rem !important; }
            p { font-size: 0.95rem; line-height: 1.6; }
            .experience-card, .project-card, .certificate-card {
                padding: 1.25rem !important;
            }
            
            #skills-grid {
                padding-bottom: 1rem !important;
            }
            #project-grid {
                padding-bottom: 1rem !important;
            }
        }"""

new_mobile = """        /* ========================================
           MOBILE EXPERIENCE OPTIMIZATION
           ======================================== */
        @media (max-width: 768px) {
            /* --- Typography --- */
            html { font-size: 14px; }
            body { font-family: 'Space Grotesk', sans-serif; line-height: 1.6; }
            h2.glitch-title {
                font-size: 1.6rem !important;
                margin-bottom: 1.5rem !important;
                padding-bottom: 0.75rem !important;
                line-height: 1.3;
            }
            h3 { font-size: 1.15rem !important; }
            p, li { font-size: 0.9rem; line-height: 1.65; }

            /* --- Section Spacing (tighter on mobile) --- */
            section.mb-24 { margin-bottom: 3rem !important; }
            section.mb-48 { margin-bottom: 3rem !important; }

            /* --- Layout Wrapper --- */
            #layout-wrapper {
                padding-top: 4.5rem !important; /* Space for mobile navbar */
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-bottom: 2rem !important;
            }

            /* --- Grid gap on mobile --- */
            #layout-wrapper > .grid {
                gap: 1.5rem !important;
            }

            /* --- Cards --- */
            .experience-card, .project-card, .certificate-card {
                padding: 1.25rem !important;
            }
            .experience-card {
                border-radius: 0.75rem;
            }

            /* --- Experience logos: smaller on mobile --- */
            .experience-card img {
                width: 5rem !important; /* 80px instead of 192px */
                height: auto;
            }
            /* Education logos slightly larger */
            #education .experience-card img {
                width: 4.5rem !important;
            }

            /* --- Experience card flex layout on mobile --- */
            .experience-card .flex {
                gap: 1rem !important;
                align-items: flex-start !important;
            }
            .experience-card .flex.flex-col {
                flex-direction: row !important; /* Keep logo beside text on mobile */
            }

            /* --- Certificates --- */
            #certificates-container {
                max-height: none !important;
                padding-bottom: 1rem !important;
            }
            #cert-fade, #toggle-certs-wrapper {
                display: none !important;
            }
            .certificate-card {
                height: 10rem !important; /* Shorter on mobile */
            }
            #certificate-grid {
                gap: 0.75rem !important;
                grid-template-columns: repeat(2, 1fr) !important; /* 2 columns on mobile */
            }
            .certificate-card .card-content h3 {
                font-size: 0.8rem !important;
            }
            .certificate-card .card-content p {
                font-size: 0.7rem !important;
            }
            .certificate-card .card-content {
                padding: 0.5rem !important;
            }

            /* --- Skills grid --- */
            #skills-grid {
                padding: 1rem !important;
                gap: 0.5rem !important;
            }
            .skill-tag {
                font-size: 0.75rem !important;
                padding: 0.35rem 0.75rem !important;
            }

            /* --- Projects grid: single column on mobile --- */
            #project-grid {
                grid-template-columns: 1fr !important;
                gap: 0.75rem !important;
                padding-bottom: 0 !important;
            }

            /* --- Interests grid --- */
            #interests-grid {
                padding: 1rem !important;
                gap: 0.5rem !important;
            }

            /* --- Contact --- */
            #contact .text-center {
                padding: 1.5rem !important;
            }

            /* --- Glitch title pseudo-elements: disable on mobile for perf --- */
            .glitch-title::before,
            .glitch-title::after {
                display: none !important;
            }

            /* --- Modal on mobile --- */
            .modal-content {
                width: 95% !important;
                padding: 1.5rem !important;
                max-height: 85vh;
                overflow-y: auto;
            }

            /* --- Floating terminal position on mobile --- */
            #floating-terminal-wrapper {
                bottom: 1rem !important;
                right: 1rem !important;
            }
            #floating-terminal-window {
                bottom: 3.5rem !important;
            }

            /* --- Boot sequence terminal on mobile --- */
            #terminal-body {
                height: 300px !important;
                font-size: 0.75rem;
            }

            /* --- Disable hover transforms on mobile (perf) --- */
            .clickable-tag:hover, .project-card:hover,
            .certificate-card:hover, .experience-card:hover {
                transform: none !important;
                box-shadow: none !important;
            }
        }

        /* Tablet tweaks (769px - 1024px) */
        @media (min-width: 769px) and (max-width: 1024px) {
            #certificate-grid {
                grid-template-columns: repeat(2, 1fr) !important;
            }
            #project-grid {
                grid-template-columns: repeat(2, 1fr) !important;
            }
        }"""

css = css.replace(old_mobile, new_mobile)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css with mobile overhaul")

# --- INDEX.HTML ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Improve mobile navbar: add active section indicator
html = html.replace(
    '<div class="text-green-400 font-mono font-bold tracking-widest text-lg">~/irfan</div>',
    '<div class="flex items-center gap-2"><span class="text-green-400 font-mono font-bold tracking-widest text-sm">~/irfan</span><span id="mobile-section-indicator" class="text-gray-500 font-mono text-xs hidden lg:hidden">/</span></div>'
)

# Make mobile menu z-index higher than navbar so it properly overlays
html = html.replace(
    'id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-40',
    'id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-[60]'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with mobile improvements")

# --- SCRIPT.JS ---
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add mobile section indicator that shows current section in navbar
# Find the scroll tracker inside buildTextMinimap and add mobile indicator update
old_scroll_active = """                    if (activeLinkEl) {
                            navFrame.style.opacity = '1';
                            
                            // Get exactly where the active <li> is in the scrollable nav list
                            const li = activeLinkEl.parentElement;
                            const top = li.offsetTop;
                            const height = li.offsetHeight;
                            
                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';
                            

                        }"""

new_scroll_active = """                    if (activeLinkEl) {
                            navFrame.style.opacity = '1';
                            
                            // Get exactly where the active <li> is in the scrollable nav list
                            const li = activeLinkEl.parentElement;
                            const top = li.offsetTop;
                            const height = li.offsetHeight;
                            
                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';

                            // Update mobile section indicator
                            const indicator = document.getElementById('mobile-section-indicator');
                            if (indicator) {
                                const sectionName = activeLinkEl.textContent.trim();
                                indicator.textContent = '/ ' + sectionName.toLowerCase();
                                indicator.classList.remove('hidden');
                            }
                        }"""

js = js.replace(old_scroll_active, new_scroll_active)

# Fix hamburger icon to animate to X when menu is open
old_menu_open = """                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');"""

new_menu_open = """                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');
                    // Animate hamburger to X
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';"""

js = js.replace(old_menu_open, new_menu_open)

old_menu_close = """                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    setTimeout(() => {
                        mobileMenu.classList.add('hidden');
                        mobileMenu.classList.remove('flex');
                    }, 300);
                }
            });
        }"""

new_menu_close = """                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    // Animate X back to hamburger
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    setTimeout(() => {
                        mobileMenu.classList.add('hidden');
                        mobileMenu.classList.remove('flex');
                    }, 300);
                }
            });
        }"""

js = js.replace(old_menu_close, new_menu_close)

# Also restore hamburger when clicking a nav item in the menu
old_nav_close = """                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                setTimeout(() => {
                                    mobileMenu.classList.add('hidden');
                                    mobileMenu.classList.remove('flex');
                                }, 300);"""

new_nav_close = """                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                                setTimeout(() => {
                                    mobileMenu.classList.add('hidden');
                                    mobileMenu.classList.remove('flex');
                                }, 300);"""

js = js.replace(old_nav_close, new_nav_close)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js with mobile improvements")
print("\nAll mobile optimizations applied.")
