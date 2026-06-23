import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_create_card = """            const createCard = (cert) => {
                const card = document.createElement('div');
                card.className = 'certificate-card h-48 md:h-64 bg-[#161b22]/70 rounded-lg flex flex-col justify-end reveal';
                card.innerHTML = `
                    <div class="card-bg" style="background-image: url('${cert.imageUrl}')"></div>
                    <div class="card-content p-4">
                        <h3 class="text-lg font-bold text-gray-100">${cert.title}</h3>
                        <p class="text-sm text-gray-400">${cert.issuer}</p>
                    </div>
                `;
                card.addEventListener('click', () => openDetailModal(cert));
                return card;
            };"""

new_create_card = """            const createCard = (cert) => {
                const card = document.createElement('div');
                card.className = 'certificate-card h-40 sm:h-48 md:h-64 bg-[#161b22]/70 rounded-lg flex flex-col justify-end reveal cursor-pointer relative overflow-hidden border border-green-500/20 hover:border-green-500/60 transition-all duration-300';
                card.innerHTML = `
                    <div class="card-bg absolute inset-0 bg-cover bg-center z-0" style="background-image: url('${cert.imageUrl}')"></div>
                    <div class="relative z-10 w-full pt-10 pb-2 px-2 sm:p-4" style="background: linear-gradient(to top, rgba(22, 27, 34, 1) 10%, rgba(22, 27, 34, 0.85) 60%, transparent 100%);">
                        <h3 class="text-[0.7rem] sm:text-lg font-bold text-gray-100 leading-tight mb-1">${cert.title}</h3>
                        <p class="text-[0.6rem] sm:text-sm text-green-400 font-mono tracking-wider leading-none">${cert.issuer}</p>
                    </div>
                `;
                card.addEventListener('click', () => openDetailModal(cert));
                return card;
            };"""

if old_create_card in js:
    js = js.replace(old_create_card, new_create_card)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed createCard in script.js")
else:
    print("Warning: old_create_card not found in script.js!")

# Now let's remove the conflicting CSS from style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the mobile overrides for certificate font sizes
css = re.sub(r'\.certificate-card \.card-content h3 \{[^}]*\}', '', css)
css = re.sub(r'\.certificate-card \.card-content p \{[^}]*\}', '', css)
css = re.sub(r'\.certificate-card \.card-content \{[^}]*\}', '', css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Cleaned up style.css")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
