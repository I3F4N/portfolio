import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Increase size of minimap index items
old_link = "li.innerHTML = `<a href=\"#${el.id}\" class=\"nav-link block text-sm font-bold text-gray-400 tracking-widest px-3 py-2 transition-colors\" data-target=\"${el.id}\">${title}</a>`;"
new_link = "li.innerHTML = `<a href=\"#${el.id}\" class=\"nav-link block text-base font-bold text-gray-300 tracking-widest px-5 py-4 transition-colors\" data-target=\"${el.id}\">${title}</a>`;"
js = js.replace(old_link, new_link)

# We also need to change the class for the li to give it more breathing room if needed, but it's currently 'mt-6 mb-2 first:mt-0'.
js = js.replace("li.className = 'mt-6 mb-2 first:mt-0';", "li.className = 'my-2 first:mt-0';")

# 2. Fix the scroll tracker logic
old_tracker = """                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    let activeId = '';
                    let activeLinkEl = null;
                    
                    // Find the lowest element that has passed the top of the viewport (or is near it)
                    for (let i = elements.length - 1; i >= 0; i--) {
                        const el = elements[i];
                        const rect = el.getBoundingClientRect();
                        // If the top of the element is above the middle of the screen
                        if (rect.top <= window.innerHeight * 0.4 && rect.bottom >= window.innerHeight * 0.2) {
                            activeId = el.id;
                            break;
                        }
                    }
                    
                    // Fallback to first element if at very top
                    if (!activeId && elements.length > 0 && window.scrollY < 100) {
                        activeId = elements[0].id;
                    }"""

new_tracker = """                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    let activeId = '';
                    let activeLinkEl = null;
                    
                    // 1. Check if we are at the absolute bottom of the page
                    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50) {
                        if (elements.length > 0) activeId = elements[elements.length - 1].id;
                    } else {
                        // 2. Otherwise find the lowest element that is in the upper half of the screen
                        for (let i = elements.length - 1; i >= 0; i--) {
                            const el = elements[i];
                            const rect = el.getBoundingClientRect();
                            if (rect.top <= window.innerHeight * 0.5) {
                                activeId = el.id;
                                break;
                            }
                        }
                    }
                    
                    // Fallback to first element if at very top
                    if (!activeId && elements.length > 0 && window.scrollY < 100) {
                        activeId = elements[0].id;
                    }"""

js = js.replace(old_tracker, new_tracker)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("script.js updated with larger index and fixed scrollspy.")
