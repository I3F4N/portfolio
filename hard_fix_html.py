import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Extract the <head> completely
head_match = re.search(r'(<head>.*?</head>)', html, re.DOTALL)
head = head_match.group(1)

# 2. Extract <main> inner content
# Because there might be nested tags, regex for <main> might fail if not careful.
# But <main id="main-content" ...> to </main>
main_start = html.find('<main id="main-content"')
main_end = html.find('</main>', main_start) + len('</main>')
main_block = html[main_start:main_end]

# 3. Extract modal
modal_start = html.find('<div id="detail-modal"')
# Modal has nested divs. We know it ends before the script tags.
script_start = html.find('<script src="https://unpkg.com/@studio-freight/lenis')
modal_end = html.rfind('</div>', modal_start, script_start) + 6
modal_block = html[modal_start:modal_end]

# Clean up any glitch-titles in main block just to be sure
# Actually, the user's content inside main_block is fine, just the wrapper is bad.

# Construct the brand new flawless HTML structure
clean_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
{head}
<body class="text-gray-100 overflow-x-hidden selection:bg-green-500/30 selection:text-green-200">
    <!-- Matrix Canvas sits absolutely in the background -->
    <canvas id="matrix-canvas"></canvas>

    <!-- Boot Sequence Overlay -->
    <div id="boot-overlay" class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black transition-opacity duration-1000">
        <div class="w-full max-w-3xl font-mono text-green-400 p-4 relative">
            <div id="terminal-body" class="p-6 h-[400px] overflow-y-auto border border-green-500/20 rounded-xl bg-[#050505] shadow-[0_0_50px_rgba(34,197,94,0.1)] relative">
                <div id="output"></div>
                <div class="flex items-center mt-2">
                    <span class="prompt"></span>
                    <span id="command-input" class="flex-1 text-green-400 ml-2"></span>
                    <span class="cursor animate-pulse">_</span>
                </div>
            </div>
            <div id="skip-hint" class="text-center text-gray-500 text-xs mt-6 transition-opacity duration-500">
                Press [Enter], [Esc] or Double-Tap to skip boot sequence
            </div>
            
            <div id="mute-button" class="absolute right-8 top-8 text-gray-500 hover:text-white transition-colors cursor-pointer z-50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
            </div>
        </div>
    </div>

    <!-- The Split-Screen Layout Wrapper -->
    <div id="layout-wrapper" class="hidden opacity-0 transition-opacity duration-1000 w-full max-w-[1600px] mx-auto px-4 md:px-12 pb-32 pt-12 md:pt-32">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-32">
            
            <!-- Left Sticky Sidebar Navigation -->
            <div class="lg:col-span-3 hidden lg:block">
                <div class="sticky top-32">
                    <nav id="desktop-nav" class="relative font-mono">
                        <div id="nav-highlighter" class="absolute left-0 w-[2px] bg-green-500 transition-all duration-300 pointer-events-none" style="top: 0; height: 0;"></div>
                        <ul id="nav-list" class="pl-4 space-y-1">
                            <!-- Populated by JS minimap logic -->
                        </ul>
                    </nav>
                </div>
            </div>

            <!-- Right Scrollable Content -->
            <div class="lg:col-span-9">
                <!-- The original main content block stripped of its old hidden class -->
                {main_block.replace('id="main-content" class="hidden mt-12"', 'id="main-content" class="w-full"')}
            </div>
            
        </div>
    </div>

    <!-- Modals -->
    {modal_block}

    <!-- Scripts -->
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.7.77/Tone.js" defer></script>
    <script src="script.js" defer></script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

print("index.html hard-fixed!")
