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

old_cert_html = """<div id="certificates-container" class="pb-32 overflow-hidden transition-[max-height] duration-700 ease-in-out relative">
<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">"""

new_cert_html = """<div id="certificates-container" class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative">
<div id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">"""

old_proj_html = """<div id="projects-container" class="pb-32 overflow-hidden transition-[max-height] duration-700 ease-in-out relative" style="max-height: 900px;">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">"""

new_proj_html = """<div id="projects-container" class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative" style="max-height: 900px;">
                        <div id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">"""

update_file('index.html', [
    (old_cert_html, new_cert_html),
    (old_proj_html, new_proj_html)
])

old_js_proj = """                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '1100px' : '900px';"""

new_js_proj = """                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '900px' : '850px';"""

old_js_cert = """                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '1024px' : '832px';"""

new_js_cert = """                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '850px' : '640px';"""

old_js_resize = """                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '1024px' : '832px';"""

new_js_resize = """                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '850px' : '640px';"""

old_js_resize_proj = """                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '1100px' : '900px';"""

new_js_resize_proj = """                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '900px' : '850px';"""

update_file('script.js', [
    (old_js_proj, new_js_proj),
    (old_js_cert, new_js_cert),
    (old_js_resize, new_js_resize),
    (old_js_resize_proj, new_js_resize_proj)
])

print("Fixed row targeting for show more buttons.")
