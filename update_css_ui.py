import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Replace the old certificates CSS with a unified expandable container CSS
target_css = r"""        #certificates-container \{
            max-height: 800px; /\* Adjust based on 2 rows of cards \*/
            overflow: hidden;
            position: relative;
            transition: max-height 0\.7s ease-in-out;
        \}
        #certificates-container\.expanded \{
            max-height: 8000px; /\* Needs to be larger to accommodate all cards without clipping \*/
        \}
        \.certificates-fade \{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: linear-gradient\(to top, #0d1117, transparent\);
            pointer-events: auto; /\* Block hover on partially hidden bottom cards \*/
            transition: opacity 0\.5s ease, pointer-events 0\.5s ease;
            z-index: 5;
        \}
         #certificates-container\.expanded \+ \.certificates-fade \{
            opacity: 0;
            pointer-events: none; /\* Allow interaction when expanded \*/
        \}
        #toggle-certs-wrapper \{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            padding-bottom: 2rem;
            z-index: 6;
        \}"""

new_css = """        .expandable-container {
            overflow: hidden;
            position: relative;
            transition: max-height 0.7s ease-in-out;
        }
        #certificates-container { max-height: 800px; }
        #projects-container { max-height: 800px; }
        #skills-container { max-height: 150px; } /* ~2 rows of skill tags */
        
        .expandable-container.expanded {
            max-height: 8000px !important;
        }
        
        .expand-fade {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: linear-gradient(to top, #0d1117, transparent);
            pointer-events: auto;
            transition: opacity 0.5s ease, pointer-events 0.5s ease;
            z-index: 5;
        }
        #skills-container + .expand-fade { height: 100px; } /* Smaller fade for skills */
        
        .expandable-container.expanded + .expand-fade {
            opacity: 0;
            pointer-events: none;
        }
        
        .terminal-btn {
            position: relative;
            overflow: hidden;
        }
        .terminal-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.2), transparent);
            transition: left 0.5s ease;
        }
        .terminal-btn:hover::before {
            left: 100%;
        }"""

css = re.sub(target_css, new_css, css)

# 2. Add Mobile Typography adjustments
mobile_typography = """
        /* Mobile Typography & Readability Optimization */
        @media (max-width: 768px) {
            html { font-size: 14px; } /* Base font size reduction */
            body { line-height: 1.5; }
            h1.glitch-title { font-size: 2.5rem !important; }
            h2.glitch-title { font-size: 1.75rem !important; margin-bottom: 1rem !important; }
            h3 { font-size: 1.25rem !important; }
            p { font-size: 0.95rem; line-height: 1.6; }
            .experience-card, .project-card, .certificate-card {
                padding: 1.25rem !important;
            }
            #skills-container { max-height: 180px; } /* Adjust for mobile wrapping */
            #projects-container { max-height: 1100px; } /* Mobile cards stack, so we need more height for 2 cards */
            #certificates-container { max-height: 700px; } /* 2 cards stacked */
        }
"""

if "/* Mobile Typography & Readability Optimization */" not in css:
    # Insert it right before the existing Mobile Responsiveness block
    css = css.replace("/* Mobile Responsiveness */", mobile_typography + "\n        /* Mobile Responsiveness */")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated CSS for expandable containers and typography.")
