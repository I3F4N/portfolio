import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove pb from grid
html = html.replace('id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-12 md:pb-32"', 'id="certificate-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"')

# 2. Add pb to container so there's always space before education.sh
html = html.replace('<div id="certificates-container" >', '<div id="certificates-container" class="pb-12 md:pb-32">')

# 3. Update the wrapper to aggressively overlap the bottom row of cards (approx 160px)
old_wrapper = 'class="w-full flex justify-center pt-24 pb-8 -mt-24 relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent"'
new_wrapper = 'class="w-full flex justify-center pt-48 pb-8 -mt-[200px] pointer-events-none relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent"'
html = html.replace(old_wrapper, new_wrapper)

# 4. Make the button pointer-events-auto so it's clickable even though wrapper is none (to allow clicking cards behind the gradient if needed, though they are faded)
html = html.replace('id="toggle-certs-btn" class="', 'id="toggle-certs-btn" class="pointer-events-auto ')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Now update the javascript logic to match
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = "wrapper.className = 'w-full flex justify-center pt-24 pb-8 -mt-24 relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent';"
new_logic = "wrapper.className = 'w-full flex justify-center pt-48 pb-8 -mt-[200px] pointer-events-none relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent';"
js = js.replace(old_logic, new_logic)

old_logic2 = "wrapper.className = 'w-full flex justify-center pt-8 pb-8 relative z-10 px-4';"
new_logic2 = "wrapper.className = 'w-full flex justify-center pt-8 pb-8 relative z-10 px-4 pointer-events-auto';"
js = js.replace(old_logic2, new_logic2)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated negative margin layout.")
