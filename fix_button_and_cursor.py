import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Button
old_btn_wrapper = """                     <div id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
                        <button id="toggle-certs-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-6 rounded-full hover:bg-green-500/15 transition-all flex items-center justify-between group shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_certs.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>
                    </div>"""
new_btn_wrapper = """                     <div id="toggle-certs-wrapper" class="absolute bottom-0 w-full flex justify-center pb-8 z-10 px-4">
                        <button id="toggle-certs-btn" class="bg-[#0d1117] border border-green-500/40 text-green-400 font-mono text-sm py-3 px-8 rounded-full hover:bg-green-500/15 transition-all shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]">Show All Certificates</button>
                    </div>"""
html = html.replace(old_btn_wrapper, new_btn_wrapper)

# Remove custom cursor HTML
html = re.sub(r'<!-- Custom Cursor -->\s*<div id="custom-cursor"></div>\s*<div id="cursor-dot"></div>\s*', '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove Cursor Engine Logic entirely
cursor_engine_regex = r'// --- Custom Cursor ---.*?updateInteractiveElements\(\) \{'
js = re.sub(cursor_engine_regex, 'function updateInteractiveElements() {', js, flags=re.DOTALL)

# Remove the hover logic calling cursor classList
js = re.sub(r'cursor\.classList\.(add|remove)\(\'hover\'\);\s*(if\s*\(cursorDot\)\s*cursorDot\.classList\.(add|remove)\(\'hover\'\);)?', '', js)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'#custom-cursor\s*\{.*?(?=#cursor-dot)', '', css, flags=re.DOTALL)
css = re.sub(r'#cursor-dot\s*\{.*?(?=#cursor-dot\.hover)', '', css, flags=re.DOTALL)
css = re.sub(r'#custom-cursor\.hover\s*\{.*?(?=\/\* Custom Scrollbar)', '', css, flags=re.DOTALL)
css = re.sub(r'#cursor-dot\.hover\s*\{.*?(?=#custom-cursor)', '', css, flags=re.DOTALL)
# Actually, let's just use a broader regex to remove all cursor related blocks since we don't need them
css = re.sub(r'#custom-cursor.*?(?=\/\* Custom Scrollbar)', '', css, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updates applied.")
