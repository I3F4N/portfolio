import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the old side-nav-container
html = re.sub(r'<div id="side-nav-container" class="hidden">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL) # wait, this regex is dangerous. Let's just remove the block.

nav_start = html.find('<div id="side-nav-container" class="hidden">')
nav_end = html.find('</div>    ', nav_start) + 10
html = html[:nav_start] + html[nav_end:]

# 2. Extract terminal-window and skip-hint, and replace them with a full-screen boot overlay
terminal_match = re.search(r'<div class="terminal-window.*?</div>\s*</div>', html, re.DOTALL)
if terminal_match:
    old_terminal = terminal_match.group(0)
    html = html.replace(old_terminal, '')

skip_match = re.search(r'<div id="skip-hint".*?</div>', html, re.DOTALL)
if skip_match:
    old_skip = skip_match.group(0)
    html = html.replace(old_skip, '')

boot_overlay = """
    <!-- Boot Sequence Overlay -->
    <div id="boot-overlay" class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black transition-opacity duration-1000">
        <div class="w-full max-w-3xl font-mono text-green-400 p-4">
            <div id="terminal-body" class="p-6 h-[400px] overflow-y-auto border border-green-500/20 rounded-xl bg-[#050505] shadow-[0_0_50px_rgba(34,197,94,0.1)]">
                <div id="output"></div>
                <div class="flex items-center mt-2">
                    <span class="prompt"></span>
                    <span id="command-input" class="flex-1 text-green-400 ml-2"></span>
                    <span class="cursor animate-pulse">_</span>
                </div>
            </div>
            <div id="skip-hint" class="text-center text-gray-500 text-xs mt-6">
                Press [Enter], [Esc] or Double-Tap to skip boot sequence
            </div>
            
            <div id="mute-button" class="absolute right-8 top-8 text-gray-500 hover:text-white transition-colors cursor-pointer z-50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
            </div>
        </div>
    </div>
"""

# Replace the main container with the new split-screen wrapper
html = html.replace('<div class="container mx-auto p-4 md:p-8">', boot_overlay + '\n    <div class="w-full max-w-[1600px] mx-auto px-4 md:px-12 pb-32">')

# 3. Setup the Grid around main-content
main_content_start = '<div id="main-content" class="hidden opacity-0 transition-opacity duration-1000 mt-12">'
new_main_content = """<div id="main-content" class="hidden opacity-0 transition-opacity duration-1000 pt-12 md:pt-32">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-32">
            
            <!-- Left Sticky Sidebar Navigation -->
            <div class="lg:col-span-3 hidden lg:block">
                <div class="sticky top-32">
                    <nav id="desktop-nav" class="font-mono text-sm tracking-widest text-gray-500 space-y-6 flex flex-col">
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
                    </nav>
                </div>
            </div>

            <!-- Right Scrollable Content -->
            <div class="lg:col-span-9">"""

html = html.replace(main_content_start, new_main_content)

# Close the grid div right before the main container closes
# Find the last </div> before </body>
last_div_idx = html.rfind('</div>\n</body>')
html = html[:last_div_idx] + '        </div>\n    </div>\n' + html[last_div_idx:]

# 4. Spacing and Editorial tweaks
# Make headings massive and add huge margins between sections
html = html.replace('class="mb-16 reveal"', 'class="mb-48 reveal"') # Increase spacing between sections
html = html.replace('class="mb-12 reveal"', 'class="mb-48 reveal"')
html = html.replace('text-5xl font-bold tracking-tight', 'text-6xl lg:text-7xl font-bold tracking-tighter mb-12') # Bigger headers
html = html.replace('<p class="text-lg text-gray-300 mb-6 leading-relaxed">', '<p class="text-xl text-gray-300 mb-8 leading-relaxed max-w-3xl">') # Editorial paragraph widths

# Tile refinement: Remove green border on default, keep it pure black. Add it on hover.
old_proj_card = 'class="project-card bg-[#050505] border border-green-500/20 shadow-lg hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500'
new_proj_card = 'class="project-card bg-[#050505] border border-gray-900 hover:border-green-500/80 hover:-translate-y-3 hover:shadow-[0_0_40px_rgba(34,197,94,0.2)] transition-all duration-500'
html = html.replace(old_proj_card, new_proj_card)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Restructured index.html for asymmetrical grid.")
