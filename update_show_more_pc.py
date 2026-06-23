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

old_proj = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if (isPC) {
                    projectsContainer.style.maxHeight = 'none';
                    if (toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'none';
                    if (fadeEl) fadeEl.style.opacity = '0';
                } else {
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
                }
            };"""

new_proj = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '900px' : '850px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show More';
                } else {
                    projectsContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show Less';
                }
            };"""

old_certs = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if (isPC) {
                    certificatesContainer.style.maxHeight = 'none';
                    if (toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'none';
                    if (fadeEl) fadeEl.style.opacity = '0';
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

new_certs = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '850px' : '650px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show More';
                } else {
                    certificatesContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show Less';
                }
            };"""

old_resize = """        // Resize listener for responsive layouts
        window.addEventListener('resize', () => {
            const isPC = window.innerWidth >= 768;
            
            // Certificates
            const certsContainer = document.getElementById('certificates-container');
            const certsFade = document.getElementById('cert-fade');
            const certsBtn = document.getElementById('toggle-certs-btn');
            if (certsContainer) {
                if (isPC) {
                    certsContainer.style.maxHeight = 'none';
                    if (certsBtn) certsBtn.parentElement.style.display = 'none';
                    if (certsFade) certsFade.style.opacity = '0';
                } else {
                    if (certsBtn) certsBtn.parentElement.style.display = 'flex';
                    if (!certsExpanded) {
                        certsContainer.style.maxHeight = '650px';
                        if (certsFade) certsFade.style.opacity = '1';
                        if (certsBtn) certsBtn.textContent = 'Show More';
                    } else {
                        certsContainer.style.maxHeight = '4000px';
                        if (certsFade) certsFade.style.opacity = '0';
                        if (certsBtn) certsBtn.textContent = 'Show Less';
                    }
                }
            }
            
            // Projects
            const projContainer = document.getElementById('projects-container');
            const projFade = document.getElementById('proj-fade');
            const projBtn = document.getElementById('toggle-projects-btn');
            if (projContainer) {
                if (isPC) {
                    projContainer.style.maxHeight = 'none';
                    if (projBtn) projBtn.parentElement.style.display = 'none';
                    if (projFade) projFade.style.opacity = '0';
                } else {
                    if (projBtn) projBtn.parentElement.style.display = 'flex';
                    if (!projectsExpanded) {
                        projContainer.style.maxHeight = '850px';
                        if (projFade) projFade.style.opacity = '1';
                        if (projBtn) projBtn.textContent = 'Show More';
                    } else {
                        projContainer.style.maxHeight = '4000px';
                        if (projFade) projFade.style.opacity = '0';
                        if (projBtn) projBtn.textContent = 'Show Less';
                    }
                }
            }
        });"""

new_resize = """        // Resize listener for responsive layouts
        window.addEventListener('resize', () => {
            const isPC = window.innerWidth >= 768;
            
            // Certificates
            const certsContainer = document.getElementById('certificates-container');
            const certsFade = document.getElementById('cert-fade');
            const certsBtn = document.getElementById('toggle-certs-btn');
            if (certsContainer) {
                if (certsBtn) certsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '850px' : '650px';
                    if (certsFade) certsFade.style.opacity = '1';
                    if (certsBtn) certsBtn.textContent = 'Show More';
                } else {
                    certsContainer.style.maxHeight = '4000px';
                    if (certsFade) certsFade.style.opacity = '0';
                    if (certsBtn) certsBtn.textContent = 'Show Less';
                }
            }
            
            // Projects
            const projContainer = document.getElementById('projects-container');
            const projFade = document.getElementById('proj-fade');
            const projBtn = document.getElementById('toggle-projects-btn');
            if (projContainer) {
                if (projBtn) projBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '900px' : '850px';
                    if (projFade) projFade.style.opacity = '1';
                    if (projBtn) projBtn.textContent = 'Show More';
                } else {
                    projContainer.style.maxHeight = '4000px';
                    if (projFade) projFade.style.opacity = '0';
                    if (projBtn) projBtn.textContent = 'Show Less';
                }
            }
        });"""

update_file('script.js', [
    (old_proj, new_proj),
    (old_certs, new_certs),
    (old_resize, new_resize)
])

print("Updated script to enforce show more on PC at 3rd row.")
