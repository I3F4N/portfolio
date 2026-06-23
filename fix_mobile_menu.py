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

old_html_menu = """    <div id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-[60] hidden items-center justify-center pt-24 opacity-0 transition-opacity duration-300">
        <ul id="mobile-nav-list" class="space-y-8 text-center font-mono text-xl tracking-widest text-gray-400">"""

new_html_menu = """    <div id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-[60] hidden flex-col justify-start overflow-y-auto pt-24 pb-8 opacity-0 transition-opacity duration-300">
        <ul id="mobile-nav-list" class="space-y-4 text-center font-mono text-xl tracking-widest text-gray-400 w-full">"""

update_file('index.html', [
    (old_html_menu, new_html_menu)
])

old_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block py-4 text-3xl font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">"""
new_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block py-2 text-xl md:text-2xl font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">"""

old_js_click = """                    if (mobileNavList) mobileNavList.classList.remove('mobile-menu-active');
                    if (mobileMenu) {
                        mobileMenu.classList.remove('opacity-100');"""
new_js_click = """                    document.body.style.overflow = '';
                    if (mobileNavList) mobileNavList.classList.remove('mobile-menu-active');
                    if (mobileMenu) {
                        mobileMenu.classList.remove('opacity-100');"""

old_js_open = """                    mobileMenu.classList.add('opacity-100');
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
                } else {
                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    setTimeout(() => {"""
new_js_open = """                    mobileMenu.classList.add('opacity-100');
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
                    document.body.style.overflow = 'hidden';
                } else {
                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    document.body.style.overflow = '';
                    setTimeout(() => {"""

update_file('script.js', [
    (old_js_link, new_js_link),
    (old_js_click, new_js_click),
    (old_js_open, new_js_open)
])

print("Fixed mobile menu scrolling and sizing.")
