import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_wrapper = '<div id="toggle-certs-wrapper" class="w-full flex justify-center pt-8 pb-4 z-10 px-4">'
new_wrapper = '<div id="toggle-certs-wrapper" class="w-full flex justify-center pt-24 pb-8 -mt-24 relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent">'

html = html.replace(old_wrapper, new_wrapper)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's replace the toggleCertsBtn logic
old_logic = """                    toggleCertsBtn.addEventListener('click', () => {
                        if (certsVisible >= certificatesData.length) {
                            certsVisible = 6;
                            toggleCertsBtn.textContent = 'Show More';
                            lenis.scrollTo('#certificates', { offset: -100 });
                        } else {
                            certsVisible += 6;
                            if (certsVisible >= certificatesData.length) toggleCertsBtn.textContent = 'Show Less';
                        }
                        populateCertificates();
                    });"""

new_logic = """                    toggleCertsBtn.addEventListener('click', () => {
                        const wrapper = toggleCertsBtn.parentElement;
                        if (certsVisible >= certificatesData.length) {
                            certsVisible = 6;
                            toggleCertsBtn.textContent = 'Show More';
                            wrapper.className = 'w-full flex justify-center pt-24 pb-8 -mt-24 relative z-10 px-4 bg-gradient-to-t from-[#050505] via-[#050505]/90 to-transparent';
                            lenis.scrollTo('#certificates', { offset: -100 });
                        } else {
                            certsVisible += 6;
                            if (certsVisible >= certificatesData.length) {
                                toggleCertsBtn.textContent = 'Show Less';
                                wrapper.className = 'w-full flex justify-center pt-8 pb-8 relative z-10 px-4';
                            }
                        }
                        populateCertificates();
                    });"""

js = js.replace(old_logic, new_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated Certificates fade overlay and button logic.")
