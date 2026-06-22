import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change title in CtrlWeb to Founder
html = html.replace('<h3 class="text-2xl font-bold text-blue-400">Co-Founder & CTO</h3>', '<h3 class="text-2xl font-bold text-blue-400">Founder</h3>')

# Add og:image tags
og_tags = """    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Irfan Ahmad - Cybersecurity Portfolio">
    <meta property="og:description" content="Portfolio of Irfan Ahmad, specializing in Cyber Security, Full-Stack Dev, and IT Infrastructure.">
    <meta property="og:image" content="og_preview.png">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Irfan Ahmad - Cybersecurity Portfolio">
    <meta name="twitter:description" content="Portfolio of Irfan Ahmad, specializing in Cyber Security, Full-Stack Dev, and IT Infrastructure.">
    <meta name="twitter:image" content="og_preview.png">"""

# Replace existing tags
html = re.sub(r'    <!-- Open Graph / Facebook -->.*?    <meta name="twitter:description".*?>', og_tags, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change role in CtrlWeb to Founder
js = js.replace('role: "Infrastructure Lead"', 'role: "Founder"')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Update style.css for mobile friendliness
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

mobile_styles = """
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            #side-nav-container {
                display: none !important; /* Hide side nav on small screens */
            }
            .modal-content {
                padding: 1.5rem; /* Reduce padding on modal */
            }
            .close-button {
                right: 15px;
                top: 10px;
            }
        }
"""

if "/* Mobile Responsiveness */" not in css:
    css += mobile_styles

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updates applied successfully.")
