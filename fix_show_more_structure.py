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

old_cert = """<div id="cert-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>"""
new_cert = """<div id="cert-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>"""

old_proj = """                    <div id="projects-container" class="relative overflow-hidden transition-all duration-700 ease-in-out" style="max-height: 900px;">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        </div>
                    </div>
                    <div id="proj-fade" class="expand-fade w-full mt-[-200px] pointer-events-none transition-opacity duration-500 relative z-10"></div>
                    <div class="flex justify-center mt-8 relative z-20">
                        <button id="toggle-projects-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
                    </div>"""

new_proj = """                    <div id="projects-container" class="pb-32 overflow-hidden transition-[max-height] duration-700 ease-in-out relative" style="max-height: 900px;">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        </div>
                        <div id="proj-fade" class="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-[#000000] via-[#000000]/90 to-transparent pointer-events-none transition-opacity duration-500 z-0"></div>
                        <div class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
                            <button id="toggle-projects-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show More</button>
                        </div>
                    </div>"""

update_file('index.html', [
    (old_cert, new_cert),
    (old_proj, new_proj)
])

print("Fixed HTML structure for show more.")
