import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Certificate Height
js = js.replace("className = 'certificate-card h-64", "className = 'certificate-card h-48 md:h-64")

# 2. Add Mobile Menu Toggle Logic
mobile_menu_logic = """
        // --- Mobile Navbar Logic ---
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileNavList = document.getElementById('mobile-nav-list');

        if (mobileMenuBtn && mobileMenu && mobileNavList) {
            mobileMenuBtn.addEventListener('click', () => {
                const isHidden = mobileMenu.classList.contains('hidden');
                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');
                    // Populate if empty
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
                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                setTimeout(() => mobileMenu.classList.add('hidden'), 300);
                            });
                            mobileNavList.appendChild(li);
                        });
                    }
                } else {
                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    setTimeout(() => mobileMenu.classList.add('hidden'), 300);
                }
            });
        }
"""
# Inject mobile_menu_logic before "function populateSkills()"
js = js.replace('function populateSkills()', mobile_menu_logic + '\n        function populateSkills()')


# 3. Pagination Engines
pagination_logic = """
        let skillsVisible = 12;
        function populateSkills() {
            skillsGrid.innerHTML = '';
            const allSkills = Object.keys(skillsData);
            const toShow = allSkills.slice(0, skillsVisible);
            
            toShow.forEach((skill, index) => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag bg-gray-700 text-gray-300 py-2 px-4 rounded-full reveal reveal-child clickable-tag';
                tag.textContent = skill;
                tag.style.setProperty('--delay', `${0.1 + (index % 12) * 0.05}s`);
                tag.addEventListener('click', () => openDetailModal(skillsData[skill]));
                skillsGrid.appendChild(tag);
                revealObserver.observe(tag);
            });
            
            // Handle Toggle Button
            let toggleBtn = document.getElementById('toggle-skills-btn');
            if (!toggleBtn && allSkills.length > 12) {
                const wrapper = document.createElement('div');
                wrapper.className = 'w-full flex justify-center pt-8 pb-4 z-10 px-4 mt-4';
                wrapper.innerHTML = `<button id="toggle-skills-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>`;
                document.getElementById('skills').appendChild(wrapper);
                toggleBtn = document.getElementById('toggle-skills-btn');
                
                toggleBtn.addEventListener('click', () => {
                    if (skillsVisible >= allSkills.length) {
                        skillsVisible = 12;
                        toggleBtn.textContent = 'Show More';
                        lenis.scrollTo('#skills', { offset: -100 });
                    } else {
                        skillsVisible += 12;
                        if (skillsVisible >= allSkills.length) toggleBtn.textContent = 'Show Less';
                    }
                    populateSkills();
                });
            } else if (toggleBtn && skillsVisible >= allSkills.length) {
                toggleBtn.textContent = 'Show Less';
            }
        }
        
        // Remove old populateSkills string match
"""

js = re.sub(r'function populateSkills\(\)\s*\{.*?\}\s*(?=function populateInterests)', pagination_logic, js, flags=re.DOTALL)

proj_pagination = """
        let projectsVisible = 4;
        function populateProjects() {
            projectGrid.innerHTML = '';
            const toShow = projects.slice(0, projectsVisible);
            
            toShow.forEach((project, index) => {
                const card = document.createElement('div');
                card.id = 'proj-' + index;
                card.className = 'project-card bg-[#161b22]/70 p-6 rounded-lg reveal reveal-child';
                card.style.transitionDelay = `${(index % 4) * 100}ms`;
                card.innerHTML = `<h3 class="text-xl font-bold text-gray-100 mb-2">${project.title}</h3><p class="text-gray-400 mb-4">${project.description.substring(0, 100)}...</p><div class="flex flex-wrap gap-2">${project.tech.map(t => `<span class="bg-gray-800 text-xs text-gray-400 py-1 px-2 rounded">${t}</span>`).join('')}</div>`;
                card.addEventListener('click', () => openDetailModal(project));
                projectGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            let toggleBtn = document.getElementById('toggle-projects-btn');
            if (!toggleBtn && projects.length > 4) {
                const wrapper = document.createElement('div');
                wrapper.className = 'w-full flex justify-center pt-8 pb-4 z-10 px-4 mt-4';
                wrapper.innerHTML = `<button id="toggle-projects-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>`;
                document.getElementById('projects').appendChild(wrapper);
                toggleBtn = document.getElementById('toggle-projects-btn');
                
                toggleBtn.addEventListener('click', () => {
                    if (projectsVisible >= projects.length) {
                        projectsVisible = 4;
                        toggleBtn.textContent = 'Show More';
                        lenis.scrollTo('#projects', { offset: -100 });
                    } else {
                        projectsVisible += 4;
                        if (projectsVisible >= projects.length) toggleBtn.textContent = 'Show Less';
                    }
                    populateProjects();
                });
            } else if (toggleBtn && projectsVisible >= projects.length) {
                toggleBtn.textContent = 'Show Less';
            }
        }
"""
js = re.sub(r'function populateProjects\(\)\s*\{.*?\}\s*(?=function populateCertificates)', proj_pagination, js, flags=re.DOTALL)


cert_pagination = """
        let certsVisible = 6;
        function populateCertificates() {
            certificateGrid.innerHTML = '';
            const toShow = certificatesData.slice(0, certsVisible);
            
            const createCard = (cert) => {
                const card = document.createElement('div');
                card.className = 'certificate-card h-48 md:h-64 bg-[#161b22]/70 rounded-lg flex flex-col justify-end reveal';
                card.innerHTML = `
                    <div class="card-bg" style="background-image: url('${cert.imageUrl}')"></div>
                    <div class="card-content p-4">
                        <h3 class="text-lg font-bold text-gray-100">${cert.title}</h3>
                        <p class="text-sm text-gray-400">${cert.issuer}</p>
                    </div>
                `;
                card.addEventListener('click', () => openDetailModal(cert));
                return card;
            };

            toShow.forEach((cert) => {
                const card = createCard(cert);
                certificateGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            if (certificatesData.length <= 6 && toggleCertsWrapper) {
                 toggleCertsWrapper.style.display = 'none';
            }
        }
"""
js = re.sub(r'function populateCertificates\(\)\s*\{.*?\}\s*(?=toggleCertsBtn\.addEventListener)', cert_pagination, js, flags=re.DOTALL)

cert_toggle_logic = """
        if (toggleCertsBtn) {
            toggleCertsBtn.addEventListener('click', () => {
                if (certsVisible >= certificatesData.length) {
                    certsVisible = 6;
                    toggleCertsBtn.textContent = 'Show More';
                    lenis.scrollTo('#certificates', { offset: -100 });
                } else {
                    certsVisible += 6;
                    if (certsVisible >= certificatesData.length) toggleCertsBtn.textContent = 'Show Less';
                }
                populateCertificates();
            });
        }
"""
js = re.sub(r'toggleCertsBtn\.addEventListener\(\'click\', \(\) => \{.*?\}\);', cert_toggle_logic, js, flags=re.DOTALL)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js with pagination engines and mobile navbar logic.")
