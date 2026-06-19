import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<div id="nav-trigger"></div>', '<div id="nav-trigger"><span class="nav-trigger-text">[ NAV ]</span></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_css_trigger = """        #nav-trigger {
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 100px;
            background-color: rgba(88, 166, 255, 0.2);
            border: 1px solid rgba(88, 166, 255, 0.4);
            border-left: none;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            cursor: none;
            pointer-events: all;
            transition: all 0.3s ease;
        }
        #side-nav-container:hover #nav-trigger {
            background-color: rgba(88, 166, 255, 0.4);
        }"""

new_css_trigger = """        #nav-trigger {
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 35px;
            height: 120px;
            background-color: rgba(88, 166, 255, 0.15);
            border: 1px solid rgba(88, 166, 255, 0.4);
            border-left: none;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            cursor: pointer;
            pointer-events: all;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #58a6ff;
            font-weight: bold;
            font-size: 0.85rem;
            letter-spacing: 2px;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.2);
            animation: nav-pulse 3s infinite alternate;
        }
        .nav-trigger-text {
            transform: rotate(-90deg);
            white-space: nowrap;
            text-shadow: 0 0 5px rgba(88, 166, 255, 0.5);
        }
        @keyframes nav-pulse {
            0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.1); background-color: rgba(88, 166, 255, 0.1); }
            100% { box-shadow: 0 0 15px rgba(88, 166, 255, 0.5); background-color: rgba(88, 166, 255, 0.25); }
        }
        #side-nav-container:hover #nav-trigger {
            background-color: rgba(88, 166, 255, 0.4);
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.6);
            animation: none;
        }"""

css = css.replace(old_css_trigger, new_css_trigger)

# Let's also make sure we disable the animation if reduced motion is enabled
reduced_motion_css_old = """            .scanlines {
                display: none !important;
            }"""
reduced_motion_css_new = """            .scanlines {
                display: none !important;
            }
            #nav-trigger {
                animation: none !important;
            }"""

css = css.replace(reduced_motion_css_old, reduced_motion_css_new)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Nav trigger updated successfully.")
