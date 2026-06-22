import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove expandable container classes
css = re.sub(r'\.expandable-container\s*\{.*?(?=\.expandable-container\.expanded)', '', css, flags=re.DOTALL)
css = re.sub(r'\.expandable-container\.expanded\s*\{.*?(?=\.expand-fade)', '', css, flags=re.DOTALL)
css = re.sub(r'\.expand-fade\s*\{.*?(?=\.expandable-container\.expanded \.expand-fade)', '', css, flags=re.DOTALL)
css = re.sub(r'\.expandable-container\.expanded \.expand-fade\s*\{.*?(?=#certificates-container)', '', css, flags=re.DOTALL)
css = re.sub(r'#certificates-container\s*\{.*?(?=#projects-container)', '', css, flags=re.DOTALL)
css = re.sub(r'#projects-container\s*\{.*?(?=#skills-container)', '', css, flags=re.DOTALL)
css = re.sub(r'#skills-container\s*\{.*?\n', '', css, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Removed CSS max-height expandable container rules.")
