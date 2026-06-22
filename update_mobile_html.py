import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update section margins (mb-48 to mb-24 lg:mb-48)
html = html.replace('class="mb-48', 'class="mb-24 lg:mb-48')

# 2. Update layout-wrapper padding
html = html.replace('pb-32 pt-12 md:pt-32', 'pb-16 lg:pb-32 pt-12 lg:pt-32')

# 3. Inject Mobile Navbar HTML right after <div id="layout-wrapper"...>
mobile_navbar_html = """
    <!-- Mobile Navbar -->
    <div class="fixed top-0 left-0 w-full bg-[#0d1117]/90 backdrop-blur-md border-b border-green-500/20 z-50 lg:hidden flex justify-between items-center px-6 py-4" id="mobile-navbar">
        <div class="text-green-400 font-mono font-bold tracking-widest text-lg">~/irfan</div>
        <button id="mobile-menu-btn" class="text-green-400 focus:outline-none">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
    </div>
    
    <!-- Mobile Fullscreen Menu -->
    <div id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-40 hidden flex-col items-center justify-center pt-16 opacity-0 transition-opacity duration-300">
        <ul id="mobile-nav-list" class="space-y-8 text-center font-mono text-xl tracking-widest text-gray-400">
            <!-- Populated by JS -->
        </ul>
    </div>
"""

# Find the wrapper and inject right after it
wrapper_match = re.search(r'(<div id="layout-wrapper"[^>]*>)', html)
if wrapper_match:
    wrapper_tag = wrapper_match.group(1)
    html = html.replace(wrapper_tag, wrapper_tag + mobile_navbar_html)

# Also ensure toggle-certs-wrapper doesn't stretch weirdly on mobile by adding mt-4 instead of absolute bottom-0
# Actually, we need to remove the CSS expandable-container entirely.
# Let's clean up index.html by removing "expandable-container" classes
html = html.replace('class="expandable-container"', '')
html = html.replace('<div class="expand-fade"></div>', '')

# Replace absolute positioning of toggle buttons with relative/mt-8
html = html.replace('class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4"', 'class="w-full flex justify-center pt-8 pb-4 z-10 px-4"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html margins, layout padding, and injected mobile navbar.")
