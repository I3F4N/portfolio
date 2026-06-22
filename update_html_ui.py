import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Skip hint
html = html.replace('Press [Enter] or [Esc] to skip boot sequence', 'Press [Enter], [Esc] or Double-Tap to skip boot sequence')

# 2. Update Certificates button
old_certs_btn = """<button id="toggle-certs-btn" class="bg-gray-800 text-green-400 border border-green-400/50 font-bold py-3 px-6 rounded-md hover:bg-green-400/10 transition-colors">
                            Show All Certificates
                        </button>"""
new_certs_btn = """<button id="toggle-certs-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/30 text-green-400 font-mono text-sm py-3 px-4 rounded hover:bg-green-500/10 transition-all flex items-center justify-between group shadow-[0_0_10px_rgba(34,197,94,0.1)] hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_certs.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>"""
html = html.replace(old_certs_btn, new_certs_btn)

# 3. Update Skills structure
old_skills = """<div id="skills-grid" class="flex flex-wrap gap-3 bg-[#161b22]/70 p-6 rounded-md border border-gray-700">
                    <!-- Skills will be populated by JS -->
                </div>"""
new_skills = """<div class="relative">
                    <div id="skills-container" class="expandable-container">
                        <div id="skills-grid" class="flex flex-wrap gap-3 bg-[#161b22]/70 p-6 rounded-md border border-gray-700 pb-24">
                            <!-- Skills will be populated by JS -->
                        </div>
                    </div>
                    <div class="expand-fade"></div>
                     <div id="toggle-skills-wrapper" class="absolute bottom-0 w-full flex justify-center pb-6 z-10 px-4">
                        <button id="toggle-skills-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/30 text-green-400 font-mono text-sm py-3 px-4 rounded hover:bg-green-500/10 transition-all flex items-center justify-between group shadow-[0_0_10px_rgba(34,197,94,0.1)] hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_skills.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>
                    </div>
                </div>"""
html = html.replace(old_skills, new_skills)

# 4. Update Projects structure
old_projects = """<div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                </div>"""
new_projects = """<div class="relative">
                    <div id="projects-container" class="expandable-container">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">
                        </div>
                    </div>
                    <div class="expand-fade"></div>
                     <div id="toggle-projects-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
                        <button id="toggle-projects-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/30 text-green-400 font-mono text-sm py-3 px-4 rounded hover:bg-green-500/10 transition-all flex items-center justify-between group shadow-[0_0_10px_rgba(34,197,94,0.1)] hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_projects.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>
                    </div>
                </div>"""
html = html.replace(old_projects, new_projects)

# 5. Fix certificates fade wrapper class
html = html.replace('class="certificates-fade"', 'class="expand-fade"')

# 6. Add z-10 and px-4 to certs wrapper for consistency
html = html.replace('id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8"', 'id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated HTML structures successfully.")
