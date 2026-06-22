import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Speed up Boot Sequence
# Replace delay values in the commands array
commands_str_old = """        const commands = [
            { cmd: 'booting system...', delay: 50, prompt: false },
            { cmd: 'loading kernel modules...', delay: 100, prompt: false },
            { cmd: 'initializing security protocols...', delay: 80, prompt: false },
            { cmd: 'connection established.', delay: 200, prompt: false, color: 'text-green-400' },
            { cmd: '', delay: 300, prompt: false },
            { cmd: 'Welcome, Irfan Ahmad.', delay: 50, prompt: true },
            { cmd: 'Type `help` to see available commands.', delay: 50, prompt: true },
            { cmd: './start-portfolio.sh', delay: 100, prompt: true, isCommand: true },
        ];"""

commands_str_new = """        const commands = [
            { cmd: 'booting system...', delay: 10, prompt: false },
            { cmd: 'loading kernel modules...', delay: 20, prompt: false },
            { cmd: 'initializing security protocols...', delay: 20, prompt: false },
            { cmd: 'connection established.', delay: 50, prompt: false, color: 'text-green-400' },
            { cmd: '', delay: 50, prompt: false },
            { cmd: 'Welcome, Irfan Ahmad.', delay: 10, prompt: true },
            { cmd: 'Type `help` to see available commands.', delay: 10, prompt: true },
            { cmd: './start-portfolio.sh', delay: 20, prompt: true, isCommand: true },
        ];"""
js = js.replace(commands_str_old, commands_str_new)

# Make typing speed much faster
js = js.replace('bootSequenceTimeout = setTimeout(type, 20 + Math.random() * 20);', 'bootSequenceTimeout = setTimeout(type, 5 + Math.random() * 5);')
js = js.replace('setTimeout(() => {\n                    document.getElementById(\'main-content\')', 'setTimeout(() => {\n                    document.getElementById(\'layout-wrapper\')')


# 2. Re-write Minimap logic
# Find where buildMinimapNav is defined and replace the whole block up to initializeAllAnimations()
regex_minimap = r'// --- Minimap Sidebar Navigation ---.*?function initMinimapScrollspy\(\) \{.*?\n        \}'
new_minimap = """        // --- Visual Minimap Engine ---
        function buildVisualMinimap() {
            const container = document.getElementById('minimap-container');
            if (!container) return;
            container.innerHTML = '';
            
            const mainContent = document.getElementById('main-content');
            
            // Allow DOM to settle before calculating heights
            setTimeout(() => {
                const totalHeight = mainContent.scrollHeight;
                if(totalHeight === 0) return; // Guard
                
                // 1. Draw structural blocks
                const elements = document.querySelectorAll('#main-content section, #main-content .project-card, #main-content .experience-card, #main-content .skill-tag');
                
                elements.forEach(el => {
                    // Skip hidden or tiny elements to keep it clean
                    if(el.offsetHeight < 10) return;
                    
                    const topPercent = (el.offsetTop / totalHeight) * 100;
                    const heightPercent = (el.offsetHeight / totalHeight) * 100;
                    
                    const block = document.createElement('div');
                    block.className = 'absolute right-0 pointer-events-none rounded-[1px]';
                    
                    // Styling logic based on element type
                    if (el.tagName.toLowerCase() === 'section') {
                        block.classList.add('bg-green-500/20', 'w-full');
                    } else if (el.classList.contains('project-card') || el.classList.contains('experience-card')) {
                        block.classList.add('bg-gray-800/80', 'w-3/4');
                    } else if (el.classList.contains('skill-tag')) {
                        block.classList.add('bg-gray-700/50', 'w-1/2');
                    } else {
                        block.classList.add('bg-gray-900', 'w-1/2');
                    }
                    
                    block.style.top = topPercent + '%';
                    block.style.height = Math.max(heightPercent, 0.2) + '%'; 
                    
                    container.appendChild(block);
                });
                
                // 2. Viewport indicator
                const viewportBox = document.createElement('div');
                viewportBox.id = 'minimap-viewport';
                viewportBox.className = 'absolute right-0 w-full bg-green-500/10 border-y border-green-500/50 pointer-events-none';
                container.appendChild(viewportBox);
                
                // 3. Update viewport on scroll
                lenis.on('scroll', () => {
                    const scrollY = window.scrollY;
                    const viewportHeight = window.innerHeight;
                    const docHeight = document.documentElement.scrollHeight;
                    
                    const topPercent = (scrollY / docHeight) * 100;
                    const heightPercent = (viewportHeight / docHeight) * 100;
                    
                    const box = document.getElementById('minimap-viewport');
                    if(box) {
                        box.style.top = topPercent + '%';
                        box.style.height = heightPercent + '%';
                    }
                });
                
                // 4. Click to scroll functionality
                container.addEventListener('click', (e) => {
                    const rect = container.getBoundingClientRect();
                    const clickY = e.clientY - rect.top;
                    const clickPercent = clickY / rect.height;
                    const targetScroll = clickPercent * document.documentElement.scrollHeight;
                    
                    // Scroll so the clicked area ends up roughly in the middle of the screen
                    lenis.scrollTo(targetScroll - (window.innerHeight / 2), { duration: 1.2 });
                });
            }, 1000); // 1s delay to let animations/renders settle
        }"""
        
js = re.sub(regex_minimap, new_minimap, js, flags=re.DOTALL)

# Update the call in the executeCommand sequence
js = js.replace('buildMinimapNav(); initMinimapScrollspy(); initializeAllAnimations();', 'buildVisualMinimap(); initializeAllAnimations();')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js with visual minimap and boot speed.")
