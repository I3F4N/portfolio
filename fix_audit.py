import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove duplicate Mobile Navbar Block 2
block_to_remove = """    <!-- Mobile Navbar -->
    <div id="mobile-navbar" class="fixed top-0 left-0 w-full bg-[#0d1117]/90 backdrop-blur-md border-b border-green-500/30 z-[100] flex items-center justify-between px-4 py-3 lg:hidden transition-transform duration-300 transform -translate-y-full">
        <div class="text-green-400 font-mono text-sm font-bold tracking-widest">&gt; ./irfan.sh</div>
        <button id="mobile-menu-btn" class="text-green-400 hover:text-green-300 focus:outline-none">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
        </button>
    </div>

    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu-overlay" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-xl z-[90] hidden flex-col pt-20 px-6 overflow-y-auto">
        <ul id="mobile-nav-list" class="space-y-6 text-center font-mono text-xl mt-8 pb-12">
            <!-- Populated by JS -->
        </ul>
    </div>"""
html = html.replace(block_to_remove, '')

# 2. Fix contradictory tailwind classes on h2 glitch-titles
html = html.replace('mb-12 text-green-400 mb-6 border-b-2', 'mb-12 text-green-400 border-b-2')

# 3. Add screen-reader (sr-only) text to social icons for accessibility
html = html.replace('title="GitHub"><svg', 'title="GitHub"><span class="sr-only">GitHub</span><svg')
html = html.replace('title="LinkedIn"><svg', 'title="LinkedIn"><span class="sr-only">LinkedIn</span><svg')
html = html.replace('title="Email"><svg', 'title="Email"><span class="sr-only">Email</span><svg')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied HTML structural fixes.")
