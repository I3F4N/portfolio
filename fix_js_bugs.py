import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove the auto-scroll logic from the minimap
auto_scroll_logic = """                            // Auto-scroll the sidebar container if the active item goes out of view
                            const container = navList.parentElement;
                            const containerTop = container.scrollTop;
                            const containerBottom = containerTop + container.clientHeight;
                            
                            if (top < containerTop) {
                                container.scrollTo({ top: top - 50, behavior: 'smooth' });
                            } else if (top + height > containerBottom) {
                                container.scrollTo({ top: (top + height) - container.clientHeight + 50, behavior: 'smooth' });
                            }"""

js = js.replace(auto_scroll_logic, '')

# 2. Extract the terminal toggle logic to the root scope
old_terminal_setup = """        function enableInteractiveTerminal() {
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

new_terminal_setup = """        
        // Extract toggle logic to root so it binds immediately
        document.addEventListener('DOMContentLoaded', () => {
            const toggleBtn = document.getElementById('terminal-toggle-btn');
            const terminalWindow = document.getElementById('floating-terminal-window');
            const closeBtn = document.getElementById('close-terminal-btn');
            const header = document.getElementById('floating-terminal-header');
            const inputField = document.getElementById('mini-input');
            
            if (toggleBtn && terminalWindow) {
                function toggleTerminal() {
                    terminalWindow.classList.toggle('hidden');
                    if (!terminalWindow.classList.contains('hidden') && inputField) {
                        setTimeout(() => inputField.focus(), 100);
                    }
                }
                
                toggleBtn.addEventListener('click', toggleTerminal);
                closeBtn.addEventListener('click', toggleTerminal);
                header.addEventListener('click', (e) => {
                    if(e.target !== closeBtn) toggleTerminal();
                });
            }
        });

        function enableInteractiveTerminal() {
            // Bind to the floating terminal execution logic
            outputEl = document.getElementById('mini-output');
            terminalBody = document.getElementById('interactive-terminal');
            
            const inputField = document.getElementById('mini-input');
            
            if(!inputField) return;
            
            // Ensure we don't bind multiple times if called again
            if (!inputField.dataset.bound) {
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
                
                inputField.dataset.bound = "true";
            }
        }"""

js = js.replace(old_terminal_setup, new_terminal_setup)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed minimap auto-scroll jumping and floating terminal toggle binding.")
