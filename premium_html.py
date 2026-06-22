import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fonts
html = html.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">'
)

# 2. Body Class
html = html.replace('<body class="antialiased">', '<body class="antialiased font-sans text-gray-300">')

# 3. Card Styling (Experience)
html = html.replace('bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child', 'bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 p-6 sm:p-8 rounded-xl reveal reveal-child hover:border-white/10 transition-colors')

# 4. Text Colors
html = html.replace('text-2xl font-bold text-blue-400', 'text-2xl font-bold text-gray-100')
html = html.replace('text-blue-400', 'text-gray-100') # Any remaining blue
html = html.replace('text-lg italic text-green-400 mb-4', 'text-lg italic text-gray-400 mb-4 border-l-2 border-green-500/50 pl-4')

# 5. Fix skills container background
html = html.replace('bg-[#161b22]/70 p-6 rounded-md border border-gray-700', 'bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 p-6 rounded-xl hover:border-white/10 transition-colors')
html = html.replace('bg-[#161b22]/70 p-8 rounded-md border border-gray-700', 'bg-[#0d1117]/60 backdrop-blur-xl border border-white/5 p-8 rounded-xl hover:border-white/10 transition-colors')

# 6. Contact button
html = html.replace('bg-green-500 text-gray-900 font-bold py-3 px-6 rounded-md hover:bg-green-400', 'bg-green-500/10 text-green-400 font-mono font-bold py-3 px-6 rounded-md border border-green-500/50 hover:bg-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.3)]')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html for premium aesthetics.")
