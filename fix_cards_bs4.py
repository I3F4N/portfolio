from bs4 import BeautifulSoup
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

cards = soup.find_all('div', class_=re.compile(r'experience-card'))

for card in cards:
    # Find the flex container inside the card
    flex_container = card.find('div', class_=re.compile(r'flex.*flex-col.*sm:flex-row'))
    if not flex_container:
        continue
        
    # Find img
    img = flex_container.find('img')
    
    # Find the div containing text
    text_div = None
    for child in flex_container.children:
        if child.name == 'div':
            text_div = child
            break
            
    if not img or not text_div:
        continue
        
    # Inside text_div, we have h3, p (date), and then ul or other p's
    h3 = text_div.find('h3')
    
    # The first p is usually the date/company
    p_date = text_div.find('p')
    
    # Collect the rest of the elements (ul, other p's like "Driving Innovation and Growth")
    rest_elements = []
    found_date = False
    for child in text_div.children:
        if child == h3:
            continue
        if child == p_date and not found_date:
            found_date = True
            continue
        if child.name in ['ul', 'p', 'div']:
            rest_elements.append(child)
            
    # Now rebuild the structure
    # 1. Update flex_container classes
    old_classes = flex_container.get('class', [])
    new_classes = 'flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6'.split()
    flex_container['class'] = new_classes
    
    # 2. Update img classes
    img_classes = img.get('class', [])
    # replace w-48 or w-32 with w-24 sm:w-48 or w-16 sm:w-32
    new_img_classes = []
    for cls in img_classes:
        if cls == 'w-48':
            new_img_classes.extend(['w-24', 'sm:w-48'])
        elif cls == 'w-32':
            new_img_classes.extend(['w-16', 'sm:w-32'])
        else:
            new_img_classes.append(cls)
    if 'object-contain' not in new_img_classes:
        new_img_classes.append('object-contain')
    img['class'] = new_img_classes
    
    # 3. Create a new div for h3 and date
    header_text_div = soup.new_tag('div')
    header_text_div['class'] = 'flex-1'.split()
    
    if h3:
        h3['class'] = 'text-lg sm:text-2xl font-bold text-gray-100 leading-tight'.split()
        header_text_div.append(h3.extract())
        
    if p_date:
        p_date['class'] = 'text-xs sm:text-base text-gray-400 mt-1 sm:mt-2'.split()
        header_text_div.append(p_date.extract())
        
    # Clear flex_container and add img and header_text_div
    flex_container.clear()
    flex_container.append(img.extract())
    flex_container.append(header_text_div)
    
    # 4. Add the rest_elements after the flex_container inside the card
    # but since flex_container is already in the card, we just insert them after it
    # We must remove them from text_div first
    for el in rest_elements:
        extracted = el.extract()
        # update classes for ul and p
        if extracted.name == 'ul':
            extracted['class'] = 'list-disc list-inside text-sm sm:text-base text-gray-400 space-y-2'.split()
        elif extracted.name == 'p':
            extracted['class'] = 'text-sm sm:text-lg italic text-gray-400 mb-4 border-l-2 border-green-500/50 pl-4'.split()
        flex_container.insert_after(extracted)
        
    # text_div is now empty (or contains just whitespace), remove it
    text_div.decompose()
    
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Successfully processed index.html with BeautifulSoup.")
