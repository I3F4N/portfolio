import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.no-scrollbar' not in css:
    css += """

/* Hide scrollbar for minimap */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
"""
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update left sidebar layout
old_sidebar = """<div class="sticky top-32">
                    <div class="h-[80vh] overflow-y-auto no-scrollbar pr-4 relative flex flex-col font-mono">
                        <div id="nav-frame" class="absolute left-0 w-full border border-green-500/40 bg-green-500/5 rounded-[2px] transition-all duration-300 pointer-events-none" style="top: 0; height: 0; opacity: 0;"></div>
                        <ul id="nav-list" class="space-y-1 relative z-10 w-full pb-32">
                            <!-- Populated by JS minimap logic -->
                        </ul>
                    </div>
                </div>"""

new_sidebar = """<div class="sticky top-12 flex flex-col h-[85vh]">
                    <div class="flex-1 overflow-y-auto no-scrollbar pr-4 relative flex flex-col font-mono">
                        <div id="nav-frame" class="absolute left-0 w-full border border-green-500/40 bg-green-500/5 rounded-[2px] transition-all duration-300 pointer-events-none" style="top: 0; height: 0; opacity: 0;"></div>
                        <ul id="nav-list" class="space-y-1 relative z-10 w-full pb-12">
                            <!-- Populated by JS minimap logic -->
                        </ul>
                    </div>
                    
                    <!-- Persistent Interactive Terminal -->
                    <div class="h-64 mt-4 border border-green-500/20 rounded-xl bg-[#050505]/90 shadow-[0_0_30px_rgba(34,197,94,0.05)] p-4 font-mono text-xs overflow-y-auto no-scrollbar relative z-20 backdrop-blur-sm" id="interactive-terminal">
                        <div id="mini-output"></div>
                        <div class="flex items-center mt-2">
                            <span class="text-green-400">irfan@:~$</span>
                            <input type="text" id="mini-input" class="flex-1 bg-transparent border-none outline-none text-green-400 ml-2" autocomplete="off" spellcheck="false" />
                        </div>
                    </div>
                </div>"""

html = html.replace(old_sidebar, new_sidebar)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html and style.css updated.")
