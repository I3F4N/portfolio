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

html_old = """                <div class="flex items-center mt-2">
                    <span class="prompt"></span>
                    <span id="command-input" class="flex-1 text-green-400 ml-2"></span>
                    <span class="cursor animate-pulse">_</span>
                </div>
            </div>
            <div id="skip-hint" class="text-center text-gray-500 text-xs mt-6 transition-opacity duration-500">"""

html_new = """                <div class="flex items-center mt-2">
                    <span class="prompt"></span>
                    <span id="command-input" class="flex-1 text-green-400 ml-2"></span>
                    <span class="cursor animate-pulse">_</span>
                </div>
            </div>
            
            <!-- Boot progress indicator -->
            <div id="boot-progress-container" class="mt-4 font-mono text-sm text-green-400/80 flex items-center gap-4 transition-opacity duration-300">
                <span>SYS_LOAD:</span>
                <div class="flex-1 h-1.5 bg-green-900/40 overflow-hidden rounded-full">
                    <div id="boot-progress-bar" class="h-full bg-green-400 shadow-[0_0_10px_rgba(34,197,94,0.8)] transition-all duration-[50ms]" style="width: 0%"></div>
                </div>
                <span id="boot-progress-text" class="w-12 text-right">0%</span>
            </div>
            
            <div id="skip-hint" class="text-center text-gray-500 text-xs mt-6 transition-opacity duration-500">"""

update_file('index.html', [(html_old, html_new)])

print("index.html fixed.")
