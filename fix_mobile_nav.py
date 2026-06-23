import re

# 1. Update index.html for grid layout on mobile nav
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
# Replace the old class and id
html = re.sub(
    r'<ul\s+class="h-\[75vh\].*?"\s+id="mobile-nav-list"\s*>',
    r'<ul id="mobile-nav-list" class="grid grid-cols-2 gap-3 sm:gap-4 h-[75vh] w-full content-center font-mono tracking-widest text-gray-400 mt-8 sm:mt-12 px-4">',
    html
)

# Cache bust
import time
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
html = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={time.time()}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update script.js for populateMobileNav
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find where function starts and ends
start_idx = js.find('function populateMobileNav() {')
if start_idx != -1:
    # Find the matching closing brace for the function
    open_braces = 0
    end_idx = -1
    for i in range(start_idx, len(js)):
        if js[i] == '{':
            open_braces += 1
        elif js[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                end_idx = i + 1
                break
                
    if end_idx != -1:
        new_js = """function populateMobileNav() {
            const mobileNavList = document.getElementById('mobile-nav-list');
            if (!mobileNavList) return;
            mobileNavList.innerHTML = '';
            const sections = document.querySelectorAll('main > section');
            
            const icons = {
                'about': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>',
                'resume': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>',
                'experience': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>',
                'certificates': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path></svg>',
                'education': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path></svg>',
                'skills': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>',
                'projects': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>',
                'interests': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg>',
                'contact': '<svg class="w-6 h-6 sm:w-8 sm:h-8 mb-2 mx-auto stroke-current" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>'
            };
            
            sections.forEach((section, index) => {
                const sectionId = section.id;
                const h2 = section.querySelector('h2');
                if(!h2) return;
                
                let sectionTitle = h2.getAttribute('data-text');
                sectionTitle = sectionTitle.replace('./', '').replace('.sh', '');
                
                const li = document.createElement('li');
                
                // If it's the last item (9th item, index 8), make it col-span-2 so it centers perfectly
                const colSpan = (index === sections.length - 1 && sections.length % 2 !== 0) ? 'col-span-2' : '';
                
                li.className = `transform translate-y-4 opacity-0 transition-all duration-300 ease-out ${colSpan}`;
                li.style.transitionDelay = `${index * 0.05}s`;
                
                const iconSvg = icons[sectionId] || icons['about']; // Fallback
                
                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link flex flex-col justify-center items-center w-full h-full min-h-[90px] sm:min-h-[110px] bg-[#161b22]/70 border border-green-500/20 rounded-xl shadow-lg hover:border-green-400 hover:shadow-[0_0_15px_rgba(34,197,94,0.3)] hover:-translate-y-1 active:translate-y-0 transition-all duration-300 group" data-target="${sectionId}">
                                    ${iconSvg}
                                    <span class="text-[1.8vh] sm:text-sm font-bold tracking-wider text-center uppercase text-gray-300 group-hover:text-green-400 transition-colors">${sectionTitle}</span>
                                </a>`;
                                
                li.addEventListener('click', (e) => {
                    e.preventDefault();
                    lenis.scrollTo(`#${sectionId}`, { offset: -80, duration: 0.8 });
                    
                    const mobileMenu = document.getElementById('mobile-menu');
                    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                    const html = document.documentElement;
                    
                    if (mobileMenu) {
                        mobileMenu.classList.remove('active');
                        mobileMenu.classList.add('pointer-events-none');
                        mobileMenu.classList.replace('opacity-100', 'opacity-0');
                        setTimeout(() => {
                            mobileMenu.style.display = 'none';
                        }, 500);
                    }
                    if (mobileMenuBtn) {
                        mobileMenuBtn.classList.remove('open');
                    }
                    html.classList.remove('overflow-hidden');
                });
                
                mobileNavList.appendChild(li);
            });
        }"""
        
        js = js[:start_idx] + new_js + js[end_idx:]
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Successfully updated script.js!")
else:
    print("Warning: function populateMobileNav() not found in script.js!")
