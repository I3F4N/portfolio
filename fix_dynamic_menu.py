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

old_html_menu = """    <div id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-[60] hidden flex-col justify-start overflow-y-auto pt-24 pb-8 opacity-0 transition-opacity duration-300">
        <ul id="mobile-nav-list" class="space-y-4 text-center font-mono text-xl tracking-widest text-gray-400 w-full">"""

new_html_menu = """    <div id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-[60] hidden flex-col justify-center items-center opacity-0 transition-opacity duration-300">
        <ul id="mobile-nav-list" class="h-[75vh] flex flex-col justify-evenly text-center font-mono tracking-widest text-gray-400 w-full mt-12">"""

update_file('index.html', [
    (old_html_menu, new_html_menu)
])

old_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block py-2 text-xl md:text-2xl font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">"""
new_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block w-full py-2 text-[clamp(14px,3vh,24px)] font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">"""

update_file('script.js', [
    (old_js_link, new_js_link)
])

print("Fixed mobile menu using dynamic vh values.")
