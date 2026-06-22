import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will rewrite the entire populateSkills, populateProjects, and populateCertificates functions.
# First, let's extract everything from `function populateSkills()` down to `// --- Modal Logic ---`

start_idx = js.find('function populateSkills()')
end_idx = js.find('// --- Modal Logic ---')

old_code = js[start_idx:end_idx]

new_code = """function populateSkills() {
            skillsGrid.innerHTML = '';
            Object.keys(skillsData).forEach((skill, index) => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag bg-gray-700 text-gray-300 py-2 px-4 rounded-full reveal reveal-child clickable-tag';
                tag.textContent = skill;
                tag.style.setProperty('--delay', `${0.1 + (index % 12) * 0.05}s`);
                tag.addEventListener('click', () => openDetailModal(skillsData[skill]));
                skillsGrid.appendChild(tag);
                revealObserver.observe(tag);
            });
            const toggleBtn = document.getElementById('toggle-skills-btn');
            if (toggleBtn) toggleBtn.parentElement.style.display = 'none';
        }

        function populateInterests() {
            interestsGrid.innerHTML = '';
            const interestColors = {
                'Esports': 'bg-red-800/50 text-red-300',
                'Gym & Powerlifting': 'bg-gray-600/50 text-gray-200',
                'Sneaker Collecting': 'bg-purple-800/50 text-purple-300',
                'Perfume Collecting': 'bg-pink-800/50 text-pink-300',
                'PC Building': 'bg-blue-800/50 text-blue-300',
            };
            Object.keys(interestsData).forEach((interest, index) => {
                const tag = document.createElement('span');
                const colorClass = interestColors[interest] || 'bg-gray-800/50 text-gray-300';
                tag.className = `skill-tag ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag`;
                tag.textContent = interest;
                tag.style.setProperty('--delay', `${0.1 + index * 0.1}s`);
                tag.addEventListener('click', () => openDetailModal(interestsData[interest]));
                interestsGrid.appendChild(tag);
                revealObserver.observe(tag);
            });
        }

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
            const toggleBtn = document.getElementById('toggle-projects-btn');
            if (toggleBtn) toggleBtn.parentElement.style.display = 'none';
        }

        let certsVisible = 6;
        function populateCertificates() {
            certificateGrid.innerHTML = '';
            const isPC = window.innerWidth >= 768; // md breakpoint
            const toShow = isPC ? certificatesData.slice(0, certsVisible) : certificatesData;
            
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
            
            let toggleCertsBtn = document.getElementById('toggle-certs-btn');
            if (toggleCertsBtn) {
                if (!isPC || certificatesData.length <= 6) {
                    toggleCertsBtn.parentElement.style.display = 'none';
                } else {
                    toggleCertsBtn.parentElement.style.display = 'flex';
                    // clear old event listeners
                    const newBtn = toggleCertsBtn.cloneNode(true);
                    toggleCertsBtn.parentNode.replaceChild(newBtn, toggleCertsBtn);
                    toggleCertsBtn = newBtn;
                    
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
            }
        }

        """

js = js[:start_idx] + new_code + js[end_idx:]

# Let's also remove `let skillsVisible = 12;` and `let projectsVisible = 4;` if they exist right before populateSkills.
# We'll just run a regex to clean them up.
js = re.sub(r'let skillsVisible = 12;\s*function populateSkills', 'function populateSkills', js)
js = re.sub(r'let projectsVisible = 4;\s*function populateProjects', 'function populateProjects', js)

# Since we check window.innerWidth in populateCertificates, we should re-call it on window resize.
resize_logic = """
        window.addEventListener('resize', () => {
            if (window.innerWidth < 768) {
                // Force mobile render if crossing breakpoint
                populateCertificates();
            } else if (certificateGrid.children.length > 6 && certsVisible === 6) {
                // If it expanded on mobile but we're back to PC
                populateCertificates();
            }
        });
        
        enableInteractiveTerminal();
"""
js = js.replace('enableInteractiveTerminal();', resize_logic)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Rewrote render functions.")
