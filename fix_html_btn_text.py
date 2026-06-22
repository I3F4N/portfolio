import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure buttons default to "Show More"
html = html.replace('>Show All Certificates<', '>Show More<')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated HTML default button text.")
