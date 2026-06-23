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

html_old = """            <section id="projects" class="mb-24 md:mb-48 reveal">
                <h2 class="glitch-title text-6xl lg:text-7xl font-bold tracking-tighter mb-12 text-green-400 border-b-2 border-green-400/30 pb-2" data-text="./projects.sh">./projects.sh</h2>
                    <div id="projects-container" >
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        </div>
                    </div>
            </section>"""
html_new = """            <section id="projects" class="mb-24 md:mb-48 reveal relative">
                <h2 class="glitch-title text-6xl lg:text-7xl font-bold tracking-tighter mb-12 text-green-400 border-b-2 border-green-400/30 pb-2" data-text="./projects.sh">./projects.sh</h2>
                    <div id="projects-container" class="relative overflow-hidden transition-all duration-700 ease-in-out" style="max-height: 900px;">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        </div>
                    </div>
                    <div id="proj-fade" class="expand-fade w-full mt-[-200px] pointer-events-none transition-opacity duration-500 relative z-10"></div>
                    <div class="flex justify-center mt-8 relative z-20">
                        <button id="toggle-projects-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
                    </div>
            </section>"""

js_old = """        function populateProjects() {
            projectGrid.innerHTML = '';
            projects.forEach((project, index) => {
                const card = document.createElement('div');
                card.id = 'proj-' + index;
                card.className = 'project-card bg-[#161b22]/70 p-6 rounded-lg reveal reveal-child';
                card.style.transitionDelay = `${(index % 4) * 100}ms`;
                card.innerHTML = `<h3 class="text-xl font-bold text-gray-100 mb-2">${project.title}</h3><p class="text-gray-400 mb-4">${project.description.substring(0, 100)}...</p><div class="flex flex-wrap gap-2">${project.tech.map(t => `<span class="bg-gray-800 text-xs text-gray-400 py-1 px-2 rounded">${t}</span>`).join('')}</div>`;
                card.addEventListener('click', () => openDetailModal(project));
                projectGrid.appendChild(card);
                revealObserver.observe(card);
            });
            const toggleBtn = document.getElementById('toggle-projects-btn');
            if (toggleBtn) toggleBtn.parentElement.style.display = 'none';
        }"""
js_new = """        let projectsExpanded = false;
        function populateProjects() {
            projectGrid.innerHTML = '';
            projects.forEach((project, index) => {
                const card = document.createElement('div');
                card.id = 'proj-' + index;
                card.className = 'project-card bg-[#161b22]/70 p-6 rounded-lg reveal reveal-child';
                card.style.transitionDelay = `${(index % 4) * 100}ms`;
                card.innerHTML = `<h3 class="text-xl font-bold text-gray-100 mb-2">${project.title}</h3><p class="text-gray-400 mb-4">${project.description.substring(0, 100)}...</p><div class="flex flex-wrap gap-2">${project.tech.map(t => `<span class="bg-gray-800 text-xs text-gray-400 py-1 px-2 rounded">${t}</span>`).join('')}</div>`;
                card.addEventListener('click', () => openDetailModal(project));
                projectGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            const toggleProjectsBtn = document.getElementById('toggle-projects-btn');
            const fadeEl = document.getElementById('proj-fade');
            const projectsContainer = document.getElementById('projects-container');
            
            const updateLayout = () => {
                if(toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = '850px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show More';
                } else {
                    projectsContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show Less';
                }
            };
            
            if (toggleProjectsBtn) {
                // Remove old event listener if re-populating
                const newBtn = toggleProjectsBtn.cloneNode(true);
                toggleProjectsBtn.parentNode.replaceChild(newBtn, toggleProjectsBtn);
                newBtn.addEventListener('click', () => {
                    projectsExpanded = !projectsExpanded;
                    updateLayout();
                });
                updateLayout();
            }
        }"""

update_file('index.html', [(html_old, html_new)])
update_file('script.js', [(js_old, js_new)])

print("Show more logic added for projects.")
