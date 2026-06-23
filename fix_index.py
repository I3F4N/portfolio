import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the plain nav-frame with a HUD targeting box
old_frame = '<div id="nav-frame" class="absolute left-0 w-full border border-green-500/40 bg-green-500/5 rounded-[2px] transition-all duration-300 pointer-events-none" style="top: 0; height: 0; opacity: 0;"></div>'

new_frame = """<div id="nav-frame" class="absolute left-0 w-full transition-all duration-300 pointer-events-none z-0" style="top: 0; height: 0; opacity: 0;">
                            <!-- Cyberpunk HUD corner brackets -->
                            <div class="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-green-400"></div>
                            <div class="absolute top-0 right-0 w-2 h-2 border-t-2 border-r-2 border-green-400"></div>
                            <div class="absolute bottom-0 left-0 w-2 h-2 border-b-2 border-l-2 border-green-400"></div>
                            <div class="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-green-400"></div>
                            <!-- Scanline/Targeting background -->
                            <div class="absolute inset-0 bg-green-500/10 border-l border-r border-green-500/30 shadow-[inset_0_0_15px_rgba(34,197,94,0.15)]"></div>
                        </div>"""

html = html.replace(old_frame, new_frame)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make the minimap items transform visually when targeted
# Also add CSS transition class to the links so translate-x works smoothly
js = js.replace(
    'class="nav-link block text-base font-bold text-gray-400 hover:text-green-400 tracking-widest px-3 py-2 transition-colors"',
    'class="nav-link block text-base font-bold text-gray-400 hover:text-green-400 tracking-widest px-3 py-2 transition-all duration-300"'
)
js = js.replace(
    'class="nav-link block text-xs text-gray-500 hover:text-gray-300 px-3 py-1 transition-colors whitespace-nowrap overflow-hidden text-ellipsis"',
    'class="nav-link block text-xs text-gray-500 hover:text-gray-300 px-3 py-1 transition-all duration-300 whitespace-nowrap overflow-hidden text-ellipsis"'
)

# Add logic to toggle active classes
old_active_logic = """                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';"""

new_active_logic = """                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';
                            
                            // Visual pop for active item
                            document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                                link.classList.remove('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                            });
                            activeLinkEl.classList.add('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');"""

js = js.replace(old_active_logic, new_active_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Index styling polished.")
