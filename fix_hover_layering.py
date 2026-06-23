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

old_cert = """<div id="cert-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>
<div id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">"""

new_cert = """<div id="cert-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/95 to-transparent transition-opacity duration-500 z-10"></div>
<div id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-20 px-4 pointer-events-none">
<button id="toggle-certs-btn" class="pointer-events-auto bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
</div>"""

old_proj = """<div id="proj-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>
                        <div class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
                            <button id="toggle-projects-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
                        </div>"""

new_proj = """<div id="proj-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/95 to-transparent transition-opacity duration-500 z-10"></div>
                        <div class="absolute bottom-0 w-full flex justify-center pb-8 z-20 px-4 pointer-events-none">
                            <button id="toggle-projects-btn" class="pointer-events-auto bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
                        </div>"""

update_file('index.html', [
    (old_cert, new_cert),
    (old_proj, new_proj)
])

# For script.js we need to adjust the max-heights and fix the button replace logic if any

old_js_proj = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '900px' : '850px';"""

new_js_proj = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '1100px' : '900px';"""

old_js_cert = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '850px' : '650px';"""

new_js_cert = """            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '1024px' : '832px';"""

old_js_resize = """            if (certsContainer) {
                if (certsBtn) certsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '850px' : '650px';"""

new_js_resize = """            if (certsContainer) {
                if (certsBtn) certsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '1024px' : '832px';"""

old_js_resize_proj = """            if (projContainer) {
                if (projBtn) projBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '900px' : '850px';"""

new_js_resize_proj = """            if (projContainer) {
                if (projBtn) projBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '1100px' : '900px';"""

update_file('script.js', [
    (old_js_proj, new_js_proj),
    (old_js_cert, new_js_cert),
    (old_js_resize, new_js_resize),
    (old_js_resize_proj, new_js_resize_proj)
])

print("Fixed visual layering and hover bugs for show more buttons.")
