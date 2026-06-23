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

# 1. Throttle playTypingSound in script.js
old_js_sound = """        function playTypingSound() {
            if (!isMuted && audioInitialized) {
                typingSynth.triggerAttackRelease("C3", "32n");
            }
        }"""
new_js_sound = """        let lastTypeTime = 0;
        function playTypingSound() {
            if (!isMuted && audioInitialized) {
                const now = performance.now();
                if (now - lastTypeTime > 40) {
                    typingSynth.triggerAttackRelease("C3", "64n", Tone.now(), 0.5);
                    lastTypeTime = now;
                }
            }
        }"""

# 2. Fix certificates maxHeight on mobile in script.js (there are two places: updateLayout and resize listener)
old_js_maxh1 = """certificatesContainer.style.maxHeight = isPC ? '850px' : '640px';"""
new_js_maxh1 = """certificatesContainer.style.maxHeight = isPC ? '850px' : '504px';"""
old_js_maxh2 = """certsContainer.style.maxHeight = isPC ? '850px' : '640px';"""
new_js_maxh2 = """certsContainer.style.maxHeight = isPC ? '850px' : '504px';"""

# 3. Speed up mobile nav scrolling
old_js_scroll = """lenis.scrollTo(`#${sectionId}`, { offset: -80 });"""
new_js_scroll = """lenis.scrollTo(`#${sectionId}`, { offset: -80, duration: 0.8 });"""

update_file('script.js', [
    (old_js_sound, new_js_sound),
    (old_js_maxh1, new_js_maxh1),
    (old_js_maxh2, new_js_maxh2),
    (old_js_scroll, new_js_scroll)
])

# 4. Fix style.css mobile overrides
old_css = """            /* --- Certificates --- */
            #certificates-container {
                max-height: none !important;
                padding-bottom: 1rem !important;
            }
            #cert-fade, #toggle-certs-wrapper {
                display: none !important;
            }"""
new_css = """            /* --- Certificates --- */
            #certificates-container {
                padding-bottom: 1rem !important;
            }"""

update_file('style.css', [
    (old_css, new_css)
])

# 5. Fix index.html mobile index layout
old_html_ul = """<ul id="mobile-nav-list" class="h-[75vh] flex flex-col justify-evenly text-center font-mono tracking-widest text-gray-400 w-full mt-12">"""
new_html_ul = """<ul id="mobile-nav-list" class="h-[75vh] flex flex-col justify-center space-y-6 text-center font-mono tracking-widest text-gray-400 w-full mt-12">"""

update_file('index.html', [
    (old_html_ul, new_html_ul)
])

import time
html = open('index.html', encoding='utf-8').read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)
open('index.html', 'w', encoding='utf-8').write(html)
print("Finished!")
