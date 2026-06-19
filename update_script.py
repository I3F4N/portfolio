import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update updateInteractiveElements to use event delegation or just clear old listeners
# Actually event delegation is easier to just rewrite the whole setup.
# Let's replace the updateInteractiveElements block
interactive_block_old = """        function updateInteractiveElements() {
            if (isTouchDevice) return;
            const interactiveElements = document.querySelectorAll('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
            interactiveElements.forEach(el => {
                el.addEventListener('mouseenter', () => { cursor.classList.add('hover'); playHoverSound(); });
                el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
                el.addEventListener('click', playClickSound);
            });
        }"""
interactive_block_new = """        function updateInteractiveElements() {
            if (isTouchDevice) return;
            // Using event delegation on document body to avoid duplicate listeners and improve performance
            document.body.addEventListener('mouseover', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target && !target._hovered) {
                    cursor.classList.add('hover');
                    playHoverSound();
                    target._hovered = true;
                }
            });
            document.body.addEventListener('mouseout', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target) {
                    cursor.classList.remove('hover');
                    target._hovered = false;
                }
            });
            document.body.addEventListener('click', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target) {
                    playClickSound();
                }
            });
        }"""
content = content.replace(interactive_block_old, interactive_block_new)

# 2. Update Matrix Animation
matrix_old = """        // --- Matrix Rain Animation ---
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const alphabet = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const rainDrops = Array.from({ length: columns }).fill(1);
        const drawMatrix = () => {
            ctx.fillStyle = 'rgba(13, 17, 23, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        };
        setInterval(drawMatrix, 33);"""

matrix_new = """        // --- Matrix Rain Animation ---
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        const alphabet = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const fontSize = 16;
        let columns = Math.floor(width / fontSize);
        let rainDrops = Array.from({ length: columns }).fill(1);
        
        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            columns = Math.floor(width / fontSize);
            rainDrops = Array.from({ length: columns }).fill(1);
        });

        let lastTime = 0;
        let mouseX = -1000;
        let mouseY = -1000;

        document.body.addEventListener('mousemove', e => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        const drawMatrix = (time) => {
            if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                if (time - lastTime > 33) {
                    ctx.fillStyle = 'rgba(13, 17, 23, 0.05)';
                    ctx.fillRect(0, 0, width, height);
                    ctx.fillStyle = '#0f0';
                    ctx.font = fontSize + 'px monospace';
                    for (let i = 0; i < rainDrops.length; i++) {
                        const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                        
                        // Mouse interaction: push drops away from mouse
                        let dropX = i * fontSize;
                        let dropY = rainDrops[i] * fontSize;
                        let dist = Math.hypot(mouseX - dropX, mouseY - dropY);
                        
                        if (dist < 100) {
                            ctx.fillStyle = '#fff'; // Glow white near mouse
                        } else {
                            ctx.fillStyle = '#0f0';
                        }
                        
                        ctx.fillText(text, dropX, dropY);
                        if (dropY > height && Math.random() > 0.975) {
                            rainDrops[i] = 0;
                        }
                        rainDrops[i]++;
                    }
                    lastTime = time;
                }
                requestAnimationFrame(drawMatrix);
            }
        };
        requestAnimationFrame(drawMatrix);"""

content = content.replace(matrix_old, matrix_new)


# 3. Interactive Terminal Logic
terminal_typing_old = """        // --- Terminal Typing Effect ---
        const outputEl = document.getElementById('output');
        const commandInputEl = document.getElementById('command-input');
        const mainContentEl = document.getElementById('main-content');
        const terminalBody = document.getElementById('terminal-body');
        const commands = [
            { cmd: 'booting system...', delay: 50, prompt: false },
            { cmd: 'loading kernel modules...', delay: 100, prompt: false },
            { cmd: 'initializing security protocols...', delay: 80, prompt: false },
            { cmd: 'connection established.', delay: 200, prompt: false, color: 'text-green-400' },
            { cmd: '', delay: 300, prompt: false },
            { cmd: 'Welcome, Irfan Ahmad.', delay: 50, prompt: true },
            { cmd: 'Type `help` to see available commands.', delay: 50, prompt: true },
            { cmd: './start-portfolio.sh', delay: 100, prompt: true, isCommand: true },
        ];
        let commandIndex = 0, charIndex = 0;
        function type() {
            if (commandIndex >= commands.length) return;
            const current = commands[commandIndex];
            const text = current.cmd;
            if (charIndex < text.length) {
                playTypingSound();
                if (current.isCommand) commandInputEl.innerHTML += text.charAt(charIndex);
                else {
                    let line = outputEl.lastElementChild;
                    if (!line || current.prompt) {
                        line = document.createElement('div');
                        if (current.prompt) line.classList.add('prompt');
                        if (current.color) line.classList.add(current.color);
                        outputEl.appendChild(line);
                    }
                    line.innerHTML += text.charAt(charIndex);
                }
                charIndex++;
                setTimeout(type, 20 + Math.random() * 20);
            } else {
                if (current.isCommand) {
                    const newLine = document.createElement('div');
                    newLine.classList.add('prompt');
                    newLine.innerHTML = commandInputEl.innerHTML;
                    outputEl.appendChild(newLine);
                    commandInputEl.innerHTML = '';
                    executeCommand(current.cmd);
                }
                commandIndex++;
                charIndex = 0;
                setTimeout(type, current.delay);
            }
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }
        function executeCommand(command) {
            const outputLine = document.createElement('div');
            outputLine.classList.add('text-gray-400', 'my-2');
            if (command === './start-portfolio.sh') {
                outputLine.innerHTML = 'Initializing portfolio interface... Success.';
                outputEl.appendChild(outputLine);
                setTimeout(() => {
                    document.getElementById('main-content').classList.remove('hidden');
                    document.getElementById('side-nav-container').classList.remove('hidden');
                    populateNav();
                    initializeScrollspy();
                    initializeAllAnimations();
                    updateInteractiveElements(); // IMPORTANT: Update listeners after nav is created
                }, 500);
            } else {
                 outputLine.innerHTML = `command not found: ${command}`;
                 outputEl.appendChild(outputLine);
            }
 
        }"""

terminal_typing_new = """        // --- Terminal Typing Effect ---
        const outputEl = document.getElementById('output');
        const commandInputEl = document.getElementById('command-input');
        const mainContentEl = document.getElementById('main-content');
        const terminalBody = document.getElementById('terminal-body');
        const commands = [
            { cmd: 'booting system...', delay: 50, prompt: false },
            { cmd: 'loading kernel modules...', delay: 100, prompt: false },
            { cmd: 'initializing security protocols...', delay: 80, prompt: false },
            { cmd: 'connection established.', delay: 200, prompt: false, color: 'text-green-400' },
            { cmd: '', delay: 300, prompt: false },
            { cmd: 'Welcome, Irfan Ahmad.', delay: 50, prompt: true },
            { cmd: 'Type `help` to see available commands.', delay: 50, prompt: true },
            { cmd: './start-portfolio.sh', delay: 100, prompt: true, isCommand: true },
        ];
        let commandIndex = 0, charIndex = 0;
        let bootSequenceTimeout;
        let isBooting = true;
        
        function skipBootSequence() {
            if (!isBooting) return;
            isBooting = false;
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
        }

        // Add event listener to skip boot sequence
        document.addEventListener('keydown', (e) => {
            if (isBooting && (e.key === 'Enter' || e.key === 'Escape')) {
                skipBootSequence();
            }
        });

        function type() {
            if (!isBooting) return;
            if (commandIndex >= commands.length) return;
            const current = commands[commandIndex];
            const text = current.cmd;
            if (charIndex < text.length) {
                playTypingSound();
                if (current.isCommand) commandInputEl.innerHTML += text.charAt(charIndex);
                else {
                    let line = outputEl.lastElementChild;
                    if (!line || current.prompt) {
                        line = document.createElement('div');
                        if (current.prompt) line.classList.add('prompt');
                        if (current.color) line.classList.add(current.color);
                        outputEl.appendChild(line);
                    }
                    line.innerHTML += text.charAt(charIndex);
                }
                charIndex++;
                bootSequenceTimeout = setTimeout(type, 20 + Math.random() * 20);
            } else {
                if (current.isCommand) {
                    const newLine = document.createElement('div');
                    newLine.classList.add('prompt');
                    newLine.innerHTML = commandInputEl.innerHTML;
                    outputEl.appendChild(newLine);
                    commandInputEl.innerHTML = '';
                    executeCommand(current.cmd);
                }
                commandIndex++;
                charIndex = 0;
                bootSequenceTimeout = setTimeout(type, current.delay);
            }
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        function executeCommand(command) {
            const outputLine = document.createElement('div');
            outputLine.classList.add('text-gray-400', 'my-2');
            
            const cmdLower = command.trim().toLowerCase();
            
            if (cmdLower === './start-portfolio.sh') {
                outputLine.innerHTML = 'Initializing portfolio interface... Success.';
                outputEl.appendChild(outputLine);
                isBooting = false;
                setTimeout(() => {
                    document.getElementById('main-content').classList.remove('hidden');
                    document.getElementById('side-nav-container').classList.remove('hidden');
                    populateNav();
                    initializeScrollspy();
                    initializeAllAnimations();
                    // updateInteractiveElements(); // Replaced by event delegation
                    enableInteractiveTerminal();
                }, 500);
            } else if (cmdLower === 'help') {
                outputLine.innerHTML = `Available commands:<br/>
                <span class="text-green-400">help</span> - Show this message<br/>
                <span class="text-green-400">whoami</span> - Display current user info<br/>
                <span class="text-green-400">clear</span> - Clear the terminal output<br/>
                <span class="text-green-400">contact</span> - Show contact details<br/>
                <span class="text-green-400">cat resume.txt</span> - View quick resume summary`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'whoami') {
                outputLine.innerHTML = `guest_user@irfan-network<br/>Access Level: Visitor`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'clear') {
                outputEl.innerHTML = '';
            } else if (cmdLower === 'contact') {
                outputLine.innerHTML = `Email: <a href="mailto:irfu026@gmail.com" class="text-blue-400 hover:underline">irfu026@gmail.com</a><br/>
                LinkedIn: <a href="https://linkedin.com/in/irfanahmadblr" target="_blank" class="text-blue-400 hover:underline">irfanahmadblr</a><br/>
                GitHub: <a href="https://github.com/i3f4n" target="_blank" class="text-blue-400 hover:underline">i3f4n</a>`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'cat resume.txt') {
                outputLine.innerHTML = `Irfan Ahmad - 4th Year CS Engineer<br/>
                Specialization: Cyber Security<br/>
                Experience: Co-Founder & CTO @ CtrlWeb, DevOps & IT Lead @ E&P International<br/>
                Skills: Python, Linux Admin, Pentesting, Docker, AWS`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === '') {
                // Do nothing on empty command
            } else {
                 outputLine.innerHTML = `command not found: ${command}. Type 'help' for available commands.`;
                 outputEl.appendChild(outputLine);
            }
            
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        function enableInteractiveTerminal() {
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

content = content.replace(terminal_typing_old, terminal_typing_new)

# 4. Random Glitches logic
# Just append this logic to the end of the script before the DOMContentLoaded block

random_glitch_script = """
        // --- Random Glitch Effects ---
        function triggerRandomGlitches() {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            const glitchTitles = document.querySelectorAll('.glitch-title.visible');
            if (glitchTitles.length > 0) {
                const randomElement = glitchTitles[Math.floor(Math.random() * glitchTitles.length)];
                randomElement.classList.remove('visible');
                void randomElement.offsetWidth; // trigger reflow
                randomElement.classList.add('visible');
            }
            setTimeout(triggerRandomGlitches, 2000 + Math.random() * 5000);
        }
        triggerRandomGlitches();
"""
content = content.replace('// --- Initial Load ---', random_glitch_script + '\n        // --- Initial Load ---')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js")
