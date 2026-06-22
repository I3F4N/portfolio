import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix executeCommand
old_exec = """                setTimeout(() => {
                    document.getElementById('main-content').classList.remove('hidden');
                    document.getElementById('side-nav-container').classList.remove('hidden');
                    populateNav();
                    initializeScrollspy();
                    initializeAllAnimations();
                    // updateInteractiveElements(); // Replaced by event delegation
                    enableInteractiveTerminal();
                }, 500);"""

new_exec = """                setTimeout(() => {
                    const bootOverlay = document.getElementById('boot-overlay');
                    if (bootOverlay) {
                        bootOverlay.classList.add('opacity-0');
                        setTimeout(() => bootOverlay.style.display = 'none', 1000);
                    }
                    
                    const mainContent = document.getElementById('main-content');
                    if (mainContent) {
                        mainContent.classList.remove('hidden');
                        setTimeout(() => mainContent.classList.add('opacity-100'), 50);
                    }
                    
                    // Don't call populateNav() because we hand-coded the desktop nav
                    // populateNav();
                    // initializeScrollspy(); // using lenis.on('scroll') now
                    initializeAllAnimations();
                    enableInteractiveTerminal();
                }, 500);"""

if "document.getElementById('side-nav-container').classList.remove('hidden');" in js:
    js = js.replace(old_exec, new_exec)
else:
    print("Could not find old executeCommand block")

# Fix skipBootSequence
old_skip = """        function skipBootSequence() {
            if (!isBooting) return;
            isBooting = false; const hint = document.getElementById('skip-hint'); if(hint) hint.style.opacity = '0';
            clearTimeout(bootSequenceTimeout);
            outputEl.innerHTML = '';
            commands.forEach(cmd => {
                if(cmd.isCommand) return;
                const line = document.createElement('div');
                if (cmd.prompt) line.classList.add('prompt');
                if (cmd.color) line.classList.add(cmd.color);
                line.innerHTML = cmd.cmd;
                outputEl.appendChild(line);
            });
            const newLine = document.createElement('div');
            newLine.classList.add('prompt');
            newLine.innerHTML = './start-portfolio.sh';
            outputEl.appendChild(newLine);
            executeCommand('./start-portfolio.sh');
        }"""

new_skip = """        function skipBootSequence() {
            if (!isBooting) return;
            isBooting = false; const hint = document.getElementById('skip-hint'); if(hint) hint.style.opacity = '0';
            clearTimeout(bootSequenceTimeout);
            
            const bootOverlay = document.getElementById('boot-overlay');
            if (bootOverlay) {
                bootOverlay.classList.add('opacity-0');
                setTimeout(() => bootOverlay.style.display = 'none', 1000);
            }
            
            const mainContent = document.getElementById('main-content');
            if (mainContent) {
                mainContent.classList.remove('hidden');
                setTimeout(() => mainContent.classList.add('opacity-100'), 50);
            }
            
            initializeAllAnimations();
            enableInteractiveTerminal();
        }"""

if "executeCommand('./start-portfolio.sh');" in js:
    js = js.replace(old_skip, new_skip)

# Double check if populateNav exists and is crashing anything
# Actually, I removed side-nav-container from HTML, so populateNav will fail if it tries to access it
old_pop = "const sideNav = document.querySelector('#side-nav ul');"
new_pop = "const sideNav = document.querySelector('#side-nav ul');\n            if (!sideNav) return;"
js = js.replace(old_pop, new_pop)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed boot sequence bugs.")
