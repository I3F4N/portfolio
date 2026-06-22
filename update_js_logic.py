import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Replace the old certificates toggle logic
old_toggle = """        const toggleCertsBtn = document.getElementById('toggle-certs-btn');
        const certsContainer = document.getElementById('certificates-container');
        if (toggleCertsBtn && certsContainer) {
            toggleCertsBtn.addEventListener('click', () => {
                certsContainer.classList.toggle('expanded');
                if (certsContainer.classList.contains('expanded')) {
                    toggleCertsBtn.textContent = 'Show Less';
                } else {
                    toggleCertsBtn.textContent = 'Show All Certificates';
                    // Scroll back to top of certificates section
                    lenis.scrollTo('#certificates', { offset: -50, duration: 1 });
                }
            });
        }"""

new_toggle = """        function setupExpandableSection(containerId, buttonId, sectionId, scriptName) {
            const btn = document.getElementById(buttonId);
            const container = document.getElementById(containerId);
            if (btn && container) {
                btn.addEventListener('click', () => {
                    container.classList.toggle('expanded');
                    const commandSpan = btn.querySelector('span'); // The first span
                    if (container.classList.contains('expanded')) {
                        commandSpan.innerHTML = `&gt; ./collapse_${scriptName}.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span>`;
                    } else {
                        commandSpan.innerHTML = `&gt; ./expand_${scriptName}.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span>`;
                        lenis.scrollTo(`#${sectionId}`, { offset: -50, duration: 1 });
                    }
                });
            }
        }
        setupExpandableSection('skills-container', 'toggle-skills-btn', 'skills', 'skills');
        setupExpandableSection('projects-container', 'toggle-projects-btn', 'projects', 'projects');
        setupExpandableSection('certificates-container', 'toggle-certs-btn', 'certificates', 'certs');"""

js = js.replace(old_toggle, new_toggle)

# 2. Add Double-Tap to skip boot logic
double_tap_logic = """
        let lastTapTime = 0;
        document.addEventListener('touchstart', (e) => {
            if (isBooting) {
                const currentTime = new Date().getTime();
                const tapLength = currentTime - lastTapTime;
                if (tapLength < 500 && tapLength > 0) {
                    skipBootSequence();
                    // Don't prevent default here as it might break normal scrolling/clicks if we aren't careful, but since it's booting it's fine.
                }
                lastTapTime = currentTime;
            }
        });
"""

# Find where keydown listener is and insert after it
if "document.addEventListener('keydown', (e) => {" in js:
    keydown_block_end = js.find("});", js.find("document.addEventListener('keydown', (e) => {")) + 3
    js = js[:keydown_block_end] + double_tap_logic + js[keydown_block_end:]
else:
    print("Could not find keydown event listener to insert double tap.")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated JS logic successfully.")
