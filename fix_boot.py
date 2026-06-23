import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update commands array for a cooler server boot sequence
old_commands = """        const commands = [
            { cmd: 'Initializing kernel...', isCommand: false, prompt: true, delay: 100 },
            { cmd: 'Loading network modules... OK', isCommand: false, prompt: true, delay: 80 },
            { cmd: 'Mounting secure filesystem... OK', isCommand: false, prompt: true, delay: 80 },
            { cmd: 'Starting firewall daemon... OK', isCommand: false, prompt: true, delay: 80 },
            { cmd: 'Checking system integrity... PASSED', isCommand: false, prompt: true, delay: 100 },
            { cmd: 'Establishing encrypted connection... OK', isCommand: false, prompt: true, delay: 150 },
            { cmd: '', isCommand: false, delay: 200 },
            { cmd: './start-portfolio.sh', isCommand: true, delay: 300 },
        ];"""

new_commands = """        const commands = [
            { cmd: 'Booting Antigravity OS v9.4.2...', isCommand: false, delay: 50 },
            { cmd: '[ OK ] Reached target Basic System.', isCommand: false, color: 'text-green-400', delay: 40 },
            { cmd: '[ OK ] Started Hardware RNG Entropy Gatherer Daemon.', isCommand: false, color: 'text-green-400', delay: 40 },
            { cmd: 'Mounting /dev/nvme0n1p2 on /root... ', isCommand: false, delay: 100 },
            { cmd: 'SUCCESS', isCommand: false, color: 'text-green-400', append: true, delay: 40 },
            { cmd: 'Starting Secure Shell server...', isCommand: false, delay: 60 },
            { cmd: '[ OK ] Listening on 0.0.0.0:22', isCommand: false, color: 'text-green-400', delay: 50 },
            { cmd: 'Decrypting local user vault... ', isCommand: false, delay: 150 },
            { cmd: 'ACCESS GRANTED', isCommand: false, color: 'text-green-400', append: true, delay: 80 },
            { cmd: 'Loading holographic interface modules... done.', isCommand: false, delay: 60 },
            { cmd: 'Welcome to the network.', isCommand: false, color: 'text-blue-400', delay: 200 },
            { cmd: '', isCommand: false, delay: 200 },
            { cmd: './start-portfolio.sh', isCommand: true, delay: 300 },
        ];"""

js = js.replace(old_commands, new_commands)

# 2. Fix the type() function so it doesn't create a new div for every character
old_type_logic = """                    let line = outputEl.lastElementChild;
                    if (!line || current.prompt) {
                        line = document.createElement('div');
                        if (current.prompt) line.classList.add('prompt');
                        if (current.color) line.classList.add(current.color);
                        outputEl.appendChild(line);
                    }
                    line.innerHTML += text.charAt(charIndex);"""

new_type_logic = """                    let line = outputEl.lastElementChild;
                    if (!line || (charIndex === 0 && !current.append)) {
                        line = document.createElement('div');
                        if (current.prompt) line.classList.add('prompt');
                        if (current.color) line.classList.add(current.color);
                        outputEl.appendChild(line);
                    }
                    line.innerHTML += text.charAt(charIndex);"""

js = js.replace(old_type_logic, new_type_logic)

# 3. Increase font size of desktop index
old_index_main = 'class="nav-link block text-sm font-bold text-gray-400 hover:text-green-400 tracking-widest px-3 py-2 transition-colors"'
new_index_main = 'class="nav-link block text-base font-bold text-gray-400 hover:text-green-400 tracking-widest px-3 py-2 transition-colors"'

old_index_sub = 'class="nav-link block text-[10px] text-gray-600 hover:text-gray-300 px-3 py-1 transition-colors whitespace-nowrap overflow-hidden text-ellipsis"'
new_index_sub = 'class="nav-link block text-xs text-gray-500 hover:text-gray-300 px-3 py-1 transition-colors whitespace-nowrap overflow-hidden text-ellipsis"'

js = js.replace(old_index_main, new_index_main)
js = js.replace(old_index_sub, new_index_sub)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixes applied.")
