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


# 1. Update index.html
html_old = """                <div class="flex items-center mt-2">
                    <span class="prompt"></span>
                    <span id="command-input" class="flex-1 text-green-400 ml-2"></span>
                    <span class="cursor animate-pulse">_</span>
                </div>
            </div>
            
            <!-- Matrix Rain Toggle -->"""

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
            
            <!-- Matrix Rain Toggle -->"""

update_file('index.html', [(html_old, html_new)])

# 2. Update script.js
# First, update type()
js_old_type = """                charIndex++;
                bootSequenceTimeout = setTimeout(type, 2 + Math.random() * 3);
            } else {
                if (current.isCommand) {"""

js_new_type = """                charIndex++;
                
                // Update boot progress bar
                const progressContainer = document.getElementById('boot-progress-container');
                const progressBar = document.getElementById('boot-progress-bar');
                const progressText = document.getElementById('boot-progress-text');
                if (progressContainer && progressBar && progressText) {
                    const totalChars = commands.reduce((acc, cmd) => acc + cmd.cmd.length, 0);
                    let charsTypedSoFar = 0;
                    for (let i = 0; i < commandIndex; i++) charsTypedSoFar += commands[i].cmd.length;
                    charsTypedSoFar += charIndex;
                    
                    const percent = Math.min(100, Math.floor((charsTypedSoFar / totalChars) * 100));
                    progressBar.style.width = percent + '%';
                    progressText.textContent = percent + '%';
                }
                
                bootSequenceTimeout = setTimeout(type, 2 + Math.random() * 3);
            } else {
                if (current.isCommand) {"""


# Second, hide progress bar in executeCommand (end of boot sequence)
js_old_execute = """            if (cmdLower === './start-portfolio.sh') {
                outputLine.innerHTML = 'Initializing portfolio interface... Success.';
                outputEl.appendChild(outputLine);
                isBooting = false; const hint = document.getElementById('skip-hint'); if(hint) hint.style.opacity = '0';
                setTimeout(() => {"""

js_new_execute = """            if (cmdLower === './start-portfolio.sh') {
                outputLine.innerHTML = 'Initializing portfolio interface... Success.';
                outputEl.appendChild(outputLine);
                isBooting = false; const hint = document.getElementById('skip-hint'); if(hint) hint.style.opacity = '0';
                const progressContainer = document.getElementById('boot-progress-container');
                if (progressContainer) progressContainer.style.opacity = '0';
                setTimeout(() => {"""

# Third, hide progress bar in skipBootSequence
js_old_skip = """            clearTimeout(bootSequenceTimeout);
            const hint = document.getElementById('skip-hint');
            if (hint) hint.style.opacity = '0';"""

js_new_skip = """            clearTimeout(bootSequenceTimeout);
            const hint = document.getElementById('skip-hint');
            if (hint) hint.style.opacity = '0';
            const progressContainer = document.getElementById('boot-progress-container');
            if (progressContainer) progressContainer.style.opacity = '0';"""

update_file('script.js', [
    (js_old_type, js_new_type),
    (js_old_execute, js_new_execute),
    (js_old_skip, js_new_skip)
])

print("Boot progress bar added.")
