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


js_old1 = """                    // Populate if empty
                    if (mobileNavList.children.length === 0) {
                        const sections = document.querySelectorAll('main > section');
                        sections.forEach(section => {
                            const sectionId = section.id;
                            const sectionTitle = section.querySelector('h2').getAttribute('data-text');
                            const li = document.createElement('li');
                            li.innerHTML = `<a href="#${sectionId}" class="block w-full py-4 uppercase hover:text-green-400 transition-colors">${sectionTitle.replace('./', '').replace('.sh', '')}</a>`;
                            li.addEventListener('click', (e) => {
                                e.preventDefault();
                                lenis.scrollTo(`#${sectionId}`, { offset: -80 });
                                mobileNavList.classList.remove('mobile-menu-active');
                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                                setTimeout(() => {
                                    mobileMenu.classList.add('hidden');
                                    mobileMenu.classList.remove('flex');
                                }, 300);
                            });
                            mobileNavList.appendChild(li);
                        });
                    }"""
js_new1 = """                    // Populate if empty
                    if (mobileNavList.children.length === 0) {
                        populateMobileNav();
                    }"""

js_old2 = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if (!isPC) {
                    certificatesContainer.style.maxHeight = 'none';
                    if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'none';
                    if(fadeEl) fadeEl.style.opacity = '0';
                } else {
                    if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                    if (!certsExpanded) {
                        certificatesContainer.style.maxHeight = '650px';
                        if(fadeEl) fadeEl.style.opacity = '1';
                        if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show More';
                    } else {
                        certificatesContainer.style.maxHeight = '4000px';
                        if(fadeEl) fadeEl.style.opacity = '0';
                        if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show Less';
                    }
                }
            };"""
js_new2 = """            const updateLayout = () => {
                if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = '650px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show More';
                } else {
                    certificatesContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show Less';
                }
            };"""

js_old3 = """            'Football': { title: 'Football', description: 'A passionate football player and fan, enjoying both the physical demands and the strategic elements of the sport.' },
            'Puzzle Solving': { title: 'Puzzle Solving', description: 'A dedicated puzzle solver with a particular interest in all types of Rubik\\'s cubes. I enjoy the mental challenge and pattern recognition required to solve complex puzzles quickly.' },
        };"""
js_new3 = """            'Football': { title: 'Football', description: 'A passionate football player and fan, enjoying both the physical demands and the strategic elements of the sport.' },
            'Puzzle Solving': { title: 'Puzzle Solving', description: 'A dedicated puzzle solver with a particular interest in all types of Rubik\\'s cubes. I enjoy the mental challenge and pattern recognition required to solve complex puzzles quickly.' },
            'Travelling': { title: 'Travelling', description: 'I love exploring the ocean and mountains. I have travelled extensively throughout India, spending months at a time in places like Lakshadweep.' },
            'Scuba Diving': { title: 'Scuba Diving', description: 'Passionate about exploring the underwater world. My travels to Lakshadweep and other coastal regions have fueled my love for scuba diving and marine environments.' },
        };"""

js_old4 = """                'Puzzle Solving': 'border-teal-500/40 text-teal-400 bg-teal-900/20 hover:bg-teal-500/20 hover:shadow-[0_0_15px_rgba(20,184,166,0.2)]'
            };"""
js_new4 = """                'Puzzle Solving': 'border-teal-500/40 text-teal-400 bg-teal-900/20 hover:bg-teal-500/20 hover:shadow-[0_0_15px_rgba(20,184,166,0.2)]',
                'Travelling': 'border-indigo-500/40 text-indigo-400 bg-indigo-900/20 hover:bg-indigo-500/20 hover:shadow-[0_0_15px_rgba(99,102,241,0.2)]',
                'Scuba Diving': 'border-cyan-500/40 text-cyan-400 bg-cyan-900/20 hover:bg-cyan-500/20 hover:shadow-[0_0_15px_rgba(6,182,212,0.2)]'
            };"""

js_old5 = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block hover:text-white transition-colors" data-target="${sectionId}">
                                    <span class="mr-2 opacity-50">0${index + 1}.</span>${sectionTitle}
                                </a>`;"""
js_new5 = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block py-4 text-3xl font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">
                                    <span class="mr-3 opacity-30 text-xl font-mono block mb-1">0${index + 1}.</span>${sectionTitle.replace('./', '').replace('.sh', '')}
                                </a>`;"""


update_file('script.js', [
    (js_old1, js_new1),
    (js_old2, js_new2),
    (js_old3, js_new3),
    (js_old4, js_new4),
    (js_old5, js_new5)
])

# Fix CSS overrides
css_old = """        .skill-tag {
            transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
        }
        .skill-tag:hover {
            background-color: #58a6ff;
            color: #0d1117;
            transform: scale(1.05);
        }"""
css_new = """        .skill-tag {
            transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .skill-tag:hover {
            transform: scale(1.05);
            /* Removed the hardcoded background/text color so Tailwind hover classes work correctly */
        }"""
        
update_file('style.css', [
    (css_old, css_new)
])
