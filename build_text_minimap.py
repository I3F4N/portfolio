import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the blocky minimap container with the new textual one
old_nav = r'<div class="flex flex-col items-end opacity-50 hover:opacity-100 transition-opacity duration-500">.*?</div>\s*</div>'
new_nav = """<div class="h-[80vh] overflow-y-auto no-scrollbar pr-4 relative flex flex-col font-mono">
                        <div id="nav-frame" class="absolute left-0 w-full border border-green-500/40 bg-green-500/5 rounded-[2px] transition-all duration-300 pointer-events-none" style="top: 0; height: 0; opacity: 0;"></div>
                        <ul id="nav-list" class="space-y-1 relative z-10 w-full pb-32">
                            <!-- Populated by JS minimap logic -->
                        </ul>
                    </div>"""
html = re.sub(old_nav, new_nav, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace buildVisualMinimap with buildTextMinimap
regex_minimap = r'// --- Visual Minimap Engine ---.*?function buildVisualMinimap\(\) \{.*?\n        \}'
new_minimap = """        // --- Text Minimap & Frame Tracker ---
        function buildTextMinimap() {
            const navList = document.getElementById('nav-list');
            const navFrame = document.getElementById('nav-frame');
            if (!navList || !navFrame) return;
            
            // Allow DOM to settle
            setTimeout(() => {
                navList.innerHTML = '';
                
                const elements = document.querySelectorAll('#main-content section, #main-content .project-card, #main-content .experience-card');
                
                elements.forEach((el, index) => {
                    const li = document.createElement('li');
                    
                    if (el.tagName.toLowerCase() === 'section') {
                        // Ensure section has an ID
                        const titleEl = el.querySelector('h2');
                        const title = titleEl ? titleEl.innerText.replace('./', '').replace('.sh', '').toUpperCase() : 'SECTION';
                        li.className = 'mt-6 mb-2 first:mt-0';
                        li.innerHTML = `<a href="#${el.id}" class="nav-link block text-xs font-bold text-gray-500 hover:text-green-400 tracking-widest px-3 py-2 transition-colors" data-target="${el.id}">${title}</a>`;
                    } else {
                        // Project or Experience Card
                        const titleEl = el.querySelector('h3');
                        const title = titleEl ? titleEl.innerText : 'Item';
                        
                        // Ensure element has an ID
                        if (!el.id) el.id = 'minimap-item-' + index;
                        
                        li.className = 'my-0';
                        // Shorten title if too long
                        const shortTitle = title.length > 25 ? title.substring(0, 22) + '...' : title;
                        li.innerHTML = `<a href="#${el.id}" class="nav-link block text-[10px] text-gray-600 hover:text-gray-300 px-3 py-1 transition-colors whitespace-nowrap overflow-hidden text-ellipsis" data-target="${el.id}">${shortTitle}</a>`;
                    }
                    
                    navList.appendChild(li);
                });
                
                // Bind Clicks
                document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetId = link.getAttribute('data-target');
                        lenis.scrollTo('#' + targetId, { offset: -50 });
                    });
                });
                
                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    let activeId = '';
                    let activeLinkEl = null;
                    
                    // Find the lowest element that has passed the top of the viewport (or is near it)
                    for (let i = elements.length - 1; i >= 0; i--) {
                        const el = elements[i];
                        const rect = el.getBoundingClientRect();
                        // If the top of the element is above the middle of the screen
                        if (rect.top <= window.innerHeight * 0.4 && rect.bottom >= window.innerHeight * 0.2) {
                            activeId = el.id;
                            break;
                        }
                    }
                    
                    // Fallback to first element if at very top
                    if (!activeId && elements.length > 0 && window.scrollY < 100) {
                        activeId = elements[0].id;
                    }
                    
                    if (activeId) {
                        activeLinkEl = document.querySelector(`#nav-list .nav-link[data-target="${activeId}"]`);
                        
                        if (activeLinkEl) {
                            navFrame.style.opacity = '1';
                            
                            // Get exactly where the active <li> is in the scrollable nav list
                            const li = activeLinkEl.parentElement;
                            const top = li.offsetTop;
                            const height = li.offsetHeight;
                            
                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';
                            
                            // Auto-scroll the sidebar container if the active item goes out of view
                            const container = navList.parentElement;
                            const containerTop = container.scrollTop;
                            const containerBottom = containerTop + container.clientHeight;
                            
                            if (top < containerTop) {
                                container.scrollTo({ top: top - 50, behavior: 'smooth' });
                            } else if (top + height > containerBottom) {
                                container.scrollTo({ top: (top + height) - container.clientHeight + 50, behavior: 'smooth' });
                            }
                        }
                    } else {
                        navFrame.style.opacity = '0';
                    }
                });
                
            }, 1000);
        }"""
        
js = re.sub(regex_minimap, new_minimap, js, flags=re.DOTALL)

# Also update the function call inside executeCommand
js = js.replace('buildVisualMinimap(); initializeAllAnimations();', 'buildTextMinimap(); initializeAllAnimations();')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated sidebar to Text Minimap with sliding frame.")
