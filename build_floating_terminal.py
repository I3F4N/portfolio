import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the old #interactive-terminal from the sidebar
regex_interactive = r'<!-- Persistent Interactive Terminal -->.*?</div>\s*</div>\s*</div>\s*<!-- Right Scrollable Content -->'
# Careful, the replacement string should keep the closing divs for the sidebar
replacement = """</div>
            </div>
            <!-- Right Scrollable Content -->"""
html = re.sub(r'<!-- Persistent Interactive Terminal -->.*?</div>\s*</div>\s*</div>\s*<!-- Right Scrollable Content -->', replacement, html, flags=re.DOTALL)

# 2. Append the Floating Terminal Widget to the body
floating_widget_html = """
    <!-- Floating Terminal Widget -->
    <div id="floating-terminal-wrapper" class="fixed bottom-6 right-6 z-[90] font-mono">
        
        <!-- The Terminal Window (Hidden by default) -->
        <div id="floating-terminal-window" class="hidden absolute bottom-16 right-0 w-[90vw] md:w-[400px] h-[60vh] md:h-[500px] bg-[#050505]/95 backdrop-blur-md border border-green-500/30 rounded-xl shadow-[0_0_40px_rgba(34,197,94,0.15)] flex flex-col overflow-hidden transition-all duration-300 transform origin-bottom-right">
            <!-- Header -->
            <div class="bg-gray-900/80 px-4 py-2 border-b border-green-500/20 flex justify-between items-center cursor-pointer" id="floating-terminal-header">
                <span class="text-xs text-green-400/70">terminal@irfan-network:~</span>
                <span class="text-gray-500 hover:text-white transition-colors" id="close-terminal-btn">&times;</span>
            </div>
            
            <!-- Body -->
            <div id="interactive-terminal" class="flex-1 p-4 overflow-y-auto no-scrollbar text-xs">
                <div class="text-gray-500 mb-2">// Interactive Console</div>
                <div class="text-gray-400 mb-4">Welcome to the network. Type <span class="text-green-400 font-bold">'help'</span> to see available commands.</div>
                <div id="mini-output"></div>
                <div class="flex items-center mt-2">
                    <span class="text-green-400">irfan@:~$</span>
                    <input type="text" id="mini-input" class="flex-1 bg-transparent border-none outline-none text-green-400 ml-2" autocomplete="off" spellcheck="false" />
                </div>
            </div>
        </div>

        <!-- The Floating Button -->
        <button id="terminal-toggle-btn" class="w-14 h-14 bg-[#050505] border border-green-500/50 rounded-full flex items-center justify-center text-green-400 shadow-[0_0_20px_rgba(34,197,94,0.2)] hover:bg-green-500/10 hover:shadow-[0_0_30px_rgba(34,197,94,0.4)] hover:scale-105 transition-all duration-300">
            >_
        </button>
        
    </div>
"""
if 'Floating Terminal Widget' not in html:
    html = html.replace('<!-- Modals -->', floating_widget_html + '\n    <!-- Modals -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update script.js to handle the toggle logic
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add the toggle logic right inside enableInteractiveTerminal
old_terminal_setup = """        function enableInteractiveTerminal() {
            // Re-bind terminal globals to the new sidebar terminal
            outputEl = document.getElementById('mini-output');
            terminalBody = document.getElementById('interactive-terminal');
            
            const inputField = document.getElementById('mini-input');
            if(!inputField) return;
            
            inputField.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    const val = this.value;
                    if (val.trim() === '') return;
                    
                    const newLine = document.createElement('div');
                    newLine.classList.add('prompt');
                    newLine.innerHTML = val;
                    outputEl.appendChild(newLine);
                    
                    this.value = '';
                    executeCommand(val);
                }
            });
            // Keep focus when clicking terminal
            terminalBody.addEventListener('click', () => {
                inputField.focus();
            });
        }"""

new_terminal_setup = """        function enableInteractiveTerminal() {
            // Bind to the floating terminal
            outputEl = document.getElementById('mini-output');
            terminalBody = document.getElementById('interactive-terminal');
            
            const inputField = document.getElementById('mini-input');
            const toggleBtn = document.getElementById('terminal-toggle-btn');
            const terminalWindow = document.getElementById('floating-terminal-window');
            const closeBtn = document.getElementById('close-terminal-btn');
            const header = document.getElementById('floating-terminal-header');
            
            if(!inputField || !toggleBtn) return;
            
            // Toggle Logic
            function toggleTerminal() {
                terminalWindow.classList.toggle('hidden');
                if (!terminalWindow.classList.contains('hidden')) {
                    setTimeout(() => inputField.focus(), 100);
                }
            }
            
            toggleBtn.addEventListener('click', toggleTerminal);
            closeBtn.addEventListener('click', toggleTerminal);
            header.addEventListener('click', (e) => {
                if(e.target !== closeBtn) toggleTerminal();
            });
            
            inputField.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    const val = this.value;
                    if (val.trim() === '') return;
                    
                    const newLine = document.createElement('div');
                    newLine.classList.add('prompt');
                    newLine.innerHTML = val;
                    outputEl.appendChild(newLine);
                    
                    this.value = '';
                    executeCommand(val);
                }
            });
            
            // Keep focus when clicking inside terminal body
            terminalBody.addEventListener('click', () => {
                inputField.focus();
            });
        }"""

js = js.replace(old_terminal_setup, new_terminal_setup)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Floating terminal and logic installed.")
