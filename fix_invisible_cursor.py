import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the cursor setup logic
old_cursor_logic = """        // --- Custom Cursor ---
        const cursor = document.getElementById('custom-cursor');
        const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

        if (isTouchDevice) {
            cursor.style.display = 'none';
        } else {
            document.head.insertAdjacentHTML("beforeend", "<style>*:not(input, textarea) { cursor: none; }</style>");
            document.addEventListener('mousemove', e => {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });
        }"""

new_cursor_logic = """        // --- Custom Cursor ---
        const cursor = document.getElementById('custom-cursor');
        const cursorDot = document.getElementById('cursor-dot');
        const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

        if (isTouchDevice) {
            cursor.style.display = 'none';
            if (cursorDot) cursorDot.style.display = 'none';
        } else {
            document.head.insertAdjacentHTML("beforeend", "<style>*:not(input, textarea) { cursor: none; }</style>");
            
            let cursorRevealed = false;
            document.addEventListener('mousemove', e => {
                if (!cursorRevealed) {
                    cursor.style.opacity = '1';
                    if (cursorDot) cursorDot.style.opacity = '1';
                    cursorRevealed = true;
                }
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
                if (cursorDot) {
                    cursorDot.style.left = e.clientX + 'px';
                    cursorDot.style.top = e.clientY + 'px';
                }
            });
        }"""

js = js.replace(old_cursor_logic, new_cursor_logic)

# Also update the hover state to hide the dot
old_hover_add = "cursor.classList.add('hover');"
new_hover_add = "cursor.classList.add('hover');\n                    if(cursorDot) cursorDot.classList.add('hover');"
js = js.replace(old_hover_add, new_hover_add)

old_hover_remove = "cursor.classList.remove('hover');"
new_hover_remove = "cursor.classList.remove('hover');\n                    if(cursorDot) cursorDot.classList.remove('hover');"
js = js.replace(old_hover_remove, new_hover_remove)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed invisible cursor and added cursorDot logic.")
