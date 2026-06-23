import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove pb-28 from the containers
html = html.replace('class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative pb-28" id="certificates-container"', 'class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative" id="certificates-container"')
html = html.replace('class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative pb-28" id="projects-container"', 'class="overflow-hidden transition-[max-height] duration-700 ease-in-out relative" id="projects-container"')

# 2. Change pb-32 on the grids to pb-20 (5rem padding at the bottom)
html = html.replace('class="grid grid-cols-2 lg:grid-cols-3 gap-8 pb-32" id="certificate-grid"', 'class="grid grid-cols-2 lg:grid-cols-3 gap-8 pb-20" id="certificate-grid"')
html = html.replace('class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32" id="project-grid"', 'class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-20" id="project-grid"')

# 3. Adjust the button wrappers to have pb-4 instead of pb-8 so it sits nicely in the pb-20 space.
# Find the exact toggle wrappers.
html = html.replace('class="absolute bottom-0 w-full flex justify-center pb-8 z-20 px-4 pointer-events-none" id="toggle-certs-wrapper"', 'class="absolute bottom-0 w-full flex justify-center pb-4 z-20 px-4 pointer-events-none" id="toggle-certs-wrapper"')
html = html.replace('class="absolute bottom-0 w-full flex justify-center pb-8 z-20 px-4 pointer-events-none"', 'class="absolute bottom-0 w-full flex justify-center pb-4 z-20 px-4 pointer-events-none"')


# Cache bust
import time
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html padding logic")
