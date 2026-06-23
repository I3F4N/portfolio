import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Speed up boot sequence delays
old_commands = """        const commands = [
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

new_commands = """        const commands = [
            { cmd: 'Booting Antigravity OS v9.4.2...', isCommand: false, delay: 30 },
            { cmd: '[ OK ] Reached target Basic System.', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: '[ OK ] Started Hardware RNG Entropy Gatherer Daemon.', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: 'Mounting /dev/nvme0n1p2 on /root... ', isCommand: false, delay: 50 },
            { cmd: 'SUCCESS', isCommand: false, color: 'text-green-400', append: true, delay: 20 },
            { cmd: 'Starting Secure Shell server...', isCommand: false, delay: 30 },
            { cmd: '[ OK ] Listening on 0.0.0.0:22', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: 'Decrypting local user vault... ', isCommand: false, delay: 80 },
            { cmd: 'ACCESS GRANTED', isCommand: false, color: 'text-green-400', append: true, delay: 40 },
            { cmd: 'Loading holographic interface modules... done.', isCommand: false, delay: 30 },
            { cmd: 'Welcome to the network.', isCommand: false, color: 'text-blue-400', delay: 100 },
            { cmd: '', isCommand: false, delay: 100 },
            { cmd: './start-portfolio.sh', isCommand: true, delay: 150 },
        ];"""

js = js.replace(old_commands, new_commands)

# Speed up typing character by character
js = js.replace('bootSequenceTimeout = setTimeout(type, 5 + Math.random() * 5);', 'bootSequenceTimeout = setTimeout(type, 2 + Math.random() * 3);')

# 2. Fix the HUD box jumpiness
# Add a flag at the top of the minimap logic
js = js.replace(
    '// --- Text Minimap & Frame Tracker ---',
    '// --- Text Minimap & Frame Tracker ---\n        let isNavigating = false;\n        let navTimeout = null;'
)

# Update the click binding to set the flag and manually update the frame
old_bind_clicks = """                // Bind Clicks
                document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetId = link.getAttribute('data-target');
                        lenis.scrollTo('#' + targetId, { offset: -50 });
                    });
                });"""

new_bind_clicks = """                // Bind Clicks
                document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetId = link.getAttribute('data-target');
                        
                        // Set navigation flag so scroll event doesn't hijack the HUD
                        isNavigating = true;
                        clearTimeout(navTimeout);
                        navTimeout = setTimeout(() => { isNavigating = false; }, 1200); // 1.2s is lenis default duration
                        
                        // Immediately snap the HUD to the target item
                        const li = link.parentElement;
                        navFrame.style.top = li.offsetTop + 'px';
                        navFrame.style.height = li.offsetHeight + 'px';
                        navFrame.style.opacity = '1';
                        
                        document.querySelectorAll('#nav-list .nav-link').forEach(l => {
                            l.classList.remove('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                        });
                        link.classList.add('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                        
                        lenis.scrollTo('#' + targetId, { offset: -50 });
                    });
                });"""

js = js.replace(old_bind_clicks, new_bind_clicks)

# Update the scroll tracker to respect the flag
old_scroll_tracker = """                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    let activeId = '';"""

new_scroll_tracker = """                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    if (isNavigating) return; // Don't update HUD during automated scroll jumps
                    let activeId = '';"""

js = js.replace(old_scroll_tracker, new_scroll_tracker)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixes applied.")
