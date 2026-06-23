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

old_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block w-full py-2 text-[clamp(14px,3vh,24px)] font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">
                                    <span class="mr-3 opacity-30 text-xl font-mono block mb-1">0${index + 1}.</span>${sectionTitle.replace('./', '').replace('.sh', '')}
                                </a>`;"""

new_js_link = """                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block w-full py-2 text-[clamp(14px,3vh,24px)] font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">
                                    ${sectionTitle.replace('./', '').replace('.sh', '')}
                                </a>`;"""

update_file('script.js', [
    (old_js_link, new_js_link)
])

old_html_grid = """<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">"""
new_html_grid = """<div id="certificate-grid" class="grid grid-cols-2 lg:grid-cols-3 gap-8 pb-32">"""

update_file('index.html', [
    (old_html_grid, new_html_grid)
])

print("Removed mobile menu numbers and enforced 2 columns for certificates on mobile.")
