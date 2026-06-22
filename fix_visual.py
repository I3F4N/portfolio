import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire relative wrapper around certificates container
start_marker = '<div class="relative">'
end_marker = '</section>'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

old_html = html[start_idx:end_idx]

new_html = """<div class="relative w-full">
<div id="certificates-container" class="pb-32 overflow-hidden transition-[max-height] duration-700 ease-in-out relative">
<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
<!-- Certificates will be populated by JS -->
</div>
<div id="cert-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>
<div id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
<button id="toggle-certs-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
</div>
</div>
</div>
"""

html = html[:start_idx] + new_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Completely replace populateCertificates
start_func = js.find('let certsVisible = 6;')
end_func = js.find('// --- Modal Logic ---')

old_js = js[start_func:end_func]

new_js = """let certsExpanded = false;
        function populateCertificates() {
            certificateGrid.innerHTML = '';
            
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

            certificatesData.forEach((cert) => {
                const card = createCard(cert);
                certificateGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            let toggleCertsBtn = document.getElementById('toggle-certs-btn');
            const fadeEl = document.getElementById('cert-fade');
            
            const updateLayout = () => {
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
            };
            
            updateLayout();
            
            if (toggleCertsBtn && !toggleCertsBtn.dataset.bound) {
                toggleCertsBtn.dataset.bound = "true";
                toggleCertsBtn.addEventListener('click', () => {
                    certsExpanded = !certsExpanded;
                    if (!certsExpanded) lenis.scrollTo('#certificates', { offset: -100 });
                    updateLayout();
                });
            }
            
            window.addEventListener('resize', updateLayout);
        }

        """

js = js[:start_func] + new_js + js[end_func:]

# Clean up any leftover resize listeners from before
js = re.sub(r'window\.addEventListener\(\'resize\', \(\) => \{.*?\}\);\s*enableInteractiveTerminal\(\);', 'enableInteractiveTerminal();', js, flags=re.DOTALL)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Restored exact original CSS layout for Certificates toggle.")
