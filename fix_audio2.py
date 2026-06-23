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

old_js_sound = """        function playTypingSound() {
            if (!isMuted && audioInitialized) {
                const pitch = ['C3', 'C#3', 'D3', 'D#3'][Math.floor(Math.random() * 4)];
                typingSynth.triggerAttackRelease(pitch, '32n', Tone.now());
                typingNoise.triggerAttack(Tone.now());
            }
        }"""

new_js_sound = """        let lastTypeTime = 0;
        function playTypingSound() {
            if (!isMuted && audioInitialized) {
                const now = performance.now();
                if (now - lastTypeTime > 50) {
                    const pitch = ['C3', 'C#3', 'D3', 'D#3'][Math.floor(Math.random() * 4)];
                    typingSynth.triggerAttackRelease(pitch, '64n', Tone.now(), 0.5);
                    typingNoise.triggerAttackRelease("64n", Tone.now(), 0.5);
                    lastTypeTime = now;
                }
            }
        }"""

update_file('script.js', [
    (old_js_sound, new_js_sound)
])

# Also cache bust
import time
html = open('index.html', encoding='utf-8').read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
open('index.html', 'w', encoding='utf-8').write(html)
print("Finished fixing audio!")
