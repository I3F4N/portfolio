import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Condense Minimap and Fix Text
old_minimap_elements = "const elements = document.querySelectorAll('#main-content section, #main-content .project-card, #main-content .experience-card');"
new_minimap_elements = "const elements = document.querySelectorAll('#main-content > section');"
js = js.replace(old_minimap_elements, new_minimap_elements)

# Ensure sections get larger text
js = js.replace("li.innerHTML = `<a href=\"#${el.id}\" class=\"nav-link block text-xs font-bold text-gray-500", 
                "li.innerHTML = `<a href=\"#${el.id}\" class=\"nav-link block text-sm font-bold text-gray-400")

# The 'else' block for project-card won't even be hit now since we only query > section, but that's fine.

# 2. Setup Interactive Terminal
old_terminal_setup = """        function enableInteractiveTerminal() {
            commandInputEl.innerHTML = '<input type="text" id="terminal-input" class="bg-transparent border-none outline-none text-green-400 w-full" autocomplete="off" spellcheck="false" autofocus />';
            const inputField = document.getElementById('terminal-input');
            inputField.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    const val = this.value;
                    
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
js = js.replace(old_terminal_setup, new_terminal_setup)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("script.js updated.")
