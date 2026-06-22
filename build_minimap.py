import re

# 1. Update index.html to prepare the minimap container
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_nav = """                    <nav id="desktop-nav" class="font-mono text-sm tracking-widest text-gray-500 space-y-6 flex flex-col">
                        <!-- Hand-coded for perfection -->
                        <a href="#about" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            About
                        </a>
                        <a href="#experience" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            Experience
                        </a>
                        <a href="#projects" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            Projects
                        </a>
                        <a href="#skills" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            Skills
                        </a>
                        <a href="#certificates" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            Certificates
                        </a>
                        <a href="#contact" class="nav-link hover:text-green-400 transition-colors uppercase flex items-center group">
                            <span class="w-0 h-[1px] bg-green-400 mr-0 transition-all duration-300 group-hover:w-4 group-hover:mr-4"></span>
                            Contact
                        </a>
                    </nav>"""

new_nav = """                    <nav id="desktop-nav" class="relative font-mono">
                        <div id="nav-highlighter" class="absolute left-0 w-[2px] bg-green-500 transition-all duration-300 pointer-events-none" style="top: 0; height: 0;"></div>
                        <ul id="nav-list" class="pl-4 space-y-1">
                            <!-- Populated by JS minimap logic -->
                        </ul>
                    </nav>"""

if "<!-- Hand-coded for perfection -->" in html:
    html = html.replace(old_nav, new_nav)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update script.js to generate the minimap and run the scrollspy
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure cards have IDs when rendered
js = js.replace("card.className = 'project-card", "card.id = 'proj-' + index;\n                card.className = 'project-card")
# For experience, it's not rendered via JS, it's hardcoded in HTML. I will just rely on sections for now, or scan the DOM.
# Actually, let's write a robust buildMinimap function that scans the DOM.

minimap_logic = """
        // --- Minimap Sidebar Navigation ---
        function buildMinimapNav() {
            const navList = document.getElementById('nav-list');
            if (!navList) return;
            navList.innerHTML = ''; // Clear
            
            // Define the structure we want to map
            const structure = [
                { id: 'about', title: 'ABOUT', type: 'section' },
                { id: 'experience', title: 'EXPERIENCE', type: 'section' },
                { id: 'projects', title: 'PROJECTS', type: 'section' }
            ];
            
            // Grab project titles to add to the minimap under Projects
            const projCards = document.querySelectorAll('.project-card');
            const projSubItems = [];
            projCards.forEach((card, idx) => {
                const title = card.querySelector('h3').innerText;
                const id = 'proj-' + idx;
                card.id = id; // ensure it has an ID
                projSubItems.push({ id, title: title.substring(0, 20) + (title.length > 20 ? '...' : ''), type: 'sub' });
            });
            
            const fullStructure = [
                { id: 'about', title: 'ABOUT', type: 'section' },
                { id: 'experience', title: 'EXPERIENCE', type: 'section' },
                { id: 'projects', title: 'PROJECTS', type: 'section' },
                ...projSubItems,
                { id: 'skills', title: 'SKILLS', type: 'section' },
                { id: 'certificates', title: 'CERTIFICATES', type: 'section' },
                { id: 'contact', title: 'CONTACT', type: 'section' }
            ];
            
            fullStructure.forEach(item => {
                const li = document.createElement('li');
                if (item.type === 'section') {
                    li.className = 'mt-4 mb-1';
                    li.innerHTML = `<a href="#${item.id}" class="nav-link block text-xs font-bold text-gray-300 hover:text-green-400 tracking-widest uppercase transition-colors" data-target="${item.id}">${item.title}</a>`;
                } else {
                    li.innerHTML = `<a href="#${item.id}" class="nav-link block text-[10px] text-gray-600 hover:text-gray-300 transition-colors py-[2px]" data-target="${item.id}">${item.title}</a>`;
                }
                navList.appendChild(li);
            });
            
            // Re-bind click events for smooth scroll
            document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('data-target');
                    lenis.scrollTo('#' + targetId, { offset: -100 });
                });
            });
        }
        
        // Advanced Scrollspy for Minimap
        function initMinimapScrollspy() {
            const navLinks = document.querySelectorAll('#nav-list .nav-link');
            const highlighter = document.getElementById('nav-highlighter');
            if (!navLinks.length || !highlighter) return;
            
            lenis.on('scroll', () => {
                let currentId = '';
                // Find which element is currently at the top of the viewport
                const elements = Array.from(navLinks).map(link => document.getElementById(link.getAttribute('data-target'))).filter(Boolean);
                
                for (let i = elements.length - 1; i >= 0; i--) {
                    const el = elements[i];
                    const rect = el.getBoundingClientRect();
                    if (rect.top <= window.innerHeight * 0.3) {
                        currentId = el.id;
                        break;
                    }
                }
                
                // If we found the current section, move the highlighter
                if (currentId) {
                    const activeLink = document.querySelector(`#nav-list .nav-link[data-target="${currentId}"]`);
                    if (activeLink) {
                        navLinks.forEach(l => {
                            if (l.classList.contains('text-xs')) l.classList.replace('text-green-400', 'text-gray-300');
                            if (l.classList.contains('text-[10px]')) l.classList.replace('text-gray-300', 'text-gray-600');
                        });
                        if (activeLink.classList.contains('text-xs')) activeLink.classList.replace('text-gray-300', 'text-green-400');
                        if (activeLink.classList.contains('text-[10px]')) activeLink.classList.replace('text-gray-600', 'text-gray-300');
                        
                        const liOffset = activeLink.parentElement.offsetTop;
                        const liHeight = activeLink.parentElement.offsetHeight;
                        highlighter.style.top = liOffset + 'px';
                        highlighter.style.height = liHeight + 'px';
                    }
                }
            });
        }
"""

# Replace the old scrollspy with the new one
js = js.replace("""        // Scroll spy for sticky sidebar navigation
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
        });""", "")

# Add the new logic just before the end of the script or inside executeCommand setup
if "function buildMinimapNav" not in js:
    js = js.replace("initializeAllAnimations();", "buildMinimapNav(); initMinimapScrollspy(); initializeAllAnimations();")
    js += minimap_logic

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Added minimap navigation.")
