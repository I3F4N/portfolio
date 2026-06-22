import re

# ============================================================
# COMPREHENSIVE FIX SCRIPT
# After reading every single line of index.html, script.js, and style.css
# ============================================================

# --- FIX index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ISSUE 1: The glitch-title pseudo-elements use `background: #0d1117` but
# the actual page background is #000000/#050505. This means the glitch
# effect's ::before and ::after show a lighter grey stripe behind the text.
# The CSS needs fixing, not HTML. Will fix in CSS section below.

# ISSUE 2: Line 17 in CSS - body has font-family declared TWICE.
# The second declaration overrides the first. Will fix in CSS.

# ISSUE 3: Lines 104-106 sidebar nesting. The structure is actually:
#   <div class="sticky...">        (line 83)
#     <div class="overflow-y-auto"> (line 84)
#       ...
#     </div>                        (line 89)
#   </div>                          (line 91, with blank line 90)
# This is correct but the blank line makes it look sloppy. Clean it up.
html = html.replace(
    '                    </div>\r\n                    \r\n                    </div>',
    '                    </div>\r\n                </div>'
)

# ISSUE 4: The mobile-menu z-index (40) is LOWER than the mobile-navbar (50).
# But the menu also needs to cover the page content. When the menu opens,
# it sits behind the navbar which is correct, but the menu button on the
# navbar needs to still be clickable. This is actually fine.
# However, the mobile-menu has `hidden flex-col` which means `hidden` and
# `flex-col` are both applied. When JS removes `hidden`, the display
# becomes `block` (default), not `flex`. The `flex-col` never takes effect.
# Fix: change to use `flex` explicitly when shown.
html = html.replace(
    'id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-40 hidden flex-col items-center justify-center pt-16 opacity-0 transition-opacity duration-300"',
    'id="mobile-menu" class="fixed inset-0 bg-[#0d1117]/95 backdrop-blur-lg z-40 hidden items-center justify-center pt-16 opacity-0 transition-opacity duration-300"'
)

# ISSUE 5: skills-grid has `pb-24` padding bottom. Since we removed the
# expand button, this leaves a massive empty space at the bottom.
html = html.replace(
    'id="skills-grid" class="flex flex-wrap gap-3 bg-[#050505] border border-green-500/20 shadow-lg p-6 rounded-xl hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500 pb-24"',
    'id="skills-grid" class="flex flex-wrap gap-3 bg-[#050505] border border-green-500/20 shadow-lg p-6 rounded-xl hover:border-green-500/60 hover:-translate-y-2 hover:shadow-[0_0_30px_rgba(34,197,94,0.15)] transition-all duration-500"'
)

# ISSUE 6: toggle-skills-wrapper is still in the HTML even though JS hides it.
# The wrapper has `absolute bottom-0` which means it positions itself
# at the bottom of the `relative` parent. Since the skills grid no longer
# needs it, remove the entire skills toggle wrapper.
skills_toggle_block = """
                     <div id="toggle-skills-wrapper" class="absolute bottom-0 w-full flex justify-center pb-6 z-10 px-4">
                        <button id="toggle-skills-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/30 text-green-400 font-mono text-sm py-3 px-4 rounded hover:bg-green-500/10 transition-all flex items-center justify-between group shadow-[0_0_10px_rgba(34,197,94,0.1)] hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_skills.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>
                    </div>"""
html = html.replace(skills_toggle_block, '')

# Also remove the wrapping <div class="relative"> around skills since it
# served only to position the absolute toggle button.
html = html.replace(
    """                <div class="relative">
                    <div id="skills-container" >""",
    '                    <div id="skills-container" >'
)
# And its closing tags
html = html.replace(
    """                    </div>
                </div>
            </section>

            <section id="projects""",
    """                    </div>
            </section>

            <section id="projects"""
)

# ISSUE 7: Same for projects - remove toggle wrapper.
projects_toggle_block = """
                     <div id="toggle-projects-wrapper" class="w-full flex justify-center pt-8 pb-4 z-10 px-4">
                        <button id="toggle-projects-btn" class="w-full max-w-sm bg-[#0d1117] border border-green-500/30 text-green-400 font-mono text-sm py-3 px-4 rounded hover:bg-green-500/10 transition-all flex items-center justify-between group shadow-[0_0_10px_rgba(34,197,94,0.1)] hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <span class="opacity-70 group-hover:opacity-100 transition-opacity">&gt; ./expand_projects.sh <span class="text-gray-500 text-xs ml-2">[Click to Execute]</span></span>
                            <span class="animate-pulse">_</span>
                        </button>
                    </div>"""
html = html.replace(projects_toggle_block, '')

# Remove project-grid's unnecessary padding
html = html.replace(
    'id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-12 md:pb-32"',
    'id="project-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"'
)

# Remove the relative wrapper around projects too
html = html.replace(
    """                <div class="relative">
                    <div id="projects-container" >""",
    '                    <div id="projects-container" >'
)
html = html.replace(
    """                    </div>
                </div>
            </section>
            
            <section id="interests""",
    """                    </div>
            </section>
            
            <section id="interests"""
)

# ISSUE 8: Line 280-283 closing tag order is wrong.
# Currently: </main> </div> </div> </div>
# The </main> closes the main tag (line 96).
# Then </div> should close lg:col-span-9 (line 94).
# Then </div> should close the grid (line 79).
# Then </div> should close layout-wrapper (line 61).
# Let's verify and fix the nesting.
html = html.replace(
    """        </main>
            </div>
            
        </div>
    </div>""",
    """        </main>
            </div> <!-- end lg:col-span-9 -->
        </div> <!-- end grid -->
    </div> <!-- end layout-wrapper -->"""
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed index.html")

# --- FIX style.css ---
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# ISSUE 9: body has two font-family declarations. The second one
# (Fira Code) overrides the first (Space Grotesk). This means ALL
# body text uses monospace, which hurts readability for long paragraphs.
# Keep Fira Code as primary since the site is terminal-themed.
css = css.replace(
    "font-family: 'Space Grotesk', sans-serif;\n            font-family: 'Fira Code', monospace;",
    "font-family: 'Fira Code', monospace;"
)

# ISSUE 10: Orphaned #custom-cursor CSS rules (lines 117-133).
# The cursor elements were removed from HTML and JS but the CSS remains.
css = css.replace(
    """        #custom-cursor::after {
            content: '';
            position: absolute;
            width: 4px;
            height: 4px;
            background-color: #0f0;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        #custom-cursor.hover {
            width: 40px;
            height: 40px;
            background-color: rgba(0, 255, 0, 0.1);
            border-radius: 10%;
        }""",
    ""
)

# ISSUE 11: The glitch-title ::before/::after use `background: #0d1117`
# but the page sections sit on #000000/#050505. This causes visible
# grey rectangles behind the glitch text. Fix to transparent/inherit.
css = css.replace(
    """            background: #0d1117;
            overflow: hidden;""",
    """            background: inherit;
            overflow: hidden;"""
)

# ISSUE 12: Mobile CSS hides toggle-projects-wrapper but not toggle-skills-wrapper.
# Since we removed both from HTML, clean up the CSS references too.
css = css.replace(
    """            #skills-container + .expand-fade,
            #toggle-projects-wrapper, #projects-container + .expand-fade {
                display: none !important;
            }""",
    ""
)

# ISSUE 13: Add sr-only utility class for accessibility (used by social icons).
css += """
/* Screen reader only - for accessibility */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed style.css")

# --- FIX script.js ---
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# ISSUE 14: Lines 514-517 declare `visibleSkills`, `visibleProjects`,
# `visibleCerts` but they are never used anymore (populateSkills and
# populateProjects show all items, and populateCertificates uses
# `certsExpanded` boolean instead). Remove unused state variables.
js = js.replace(
    """        // --- Pagination State ---
        let visibleSkills = 12;
        let visibleProjects = 4;
        let visibleCerts = 6;""",
    ""
)

# ISSUE 15: Line 107 calls enableInteractiveTerminal() at module level,
# before the DOM is ready. The function tries to find #mini-input which
# doesn't exist yet. It's harmless (returns early) but wasteful.
# It's called again properly inside executeCommand and DOMContentLoaded.
# Remove the premature call.
js = js.replace(
    """        enableInteractiveTerminal();


""",
    ""
)

# ISSUE 16: Lines 463-464 grab toggleCertsBtn and toggleCertsWrapper
# at module level (top of script). But populateCertificates() also does
# `let toggleCertsBtn = document.getElementById('toggle-certs-btn');`
# inside itself (line 636), which shadows the outer variable. The outer
# ones are never used. Remove them.
js = js.replace(
    """        const toggleCertsBtn = document.getElementById('toggle-certs-btn');
        const toggleCertsWrapper = document.getElementById('toggle-certs-wrapper');""",
    ""
)

# ISSUE 17: Line 670 adds a resize listener EVERY time populateCertificates()
# is called. This means after clicking Show More/Show Less, you accumulate
# duplicate resize handlers. Fix by moving the listener outside the function.
js = js.replace(
    """            window.addEventListener('resize', updateLayout);
        }""",
    """        }"""
)

# Add a single resize listener after populateCertificates definition
js = js.replace(
    """        // --- Modal Logic ---""",
    """        // Resize listener for certificates layout (added once)
        let certsResizeHandler = null;
        window.addEventListener('resize', () => {
            const isPC = window.innerWidth >= 768;
            const container = document.getElementById('certificates-container');
            const fadeEl = document.getElementById('cert-fade');
            const btn = document.getElementById('toggle-certs-btn');
            if (!container) return;
            if (!isPC) {
                container.style.maxHeight = 'none';
                if(btn) btn.parentElement.style.display = 'none';
                if(fadeEl) fadeEl.style.opacity = '0';
            } else {
                if(btn) btn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    container.style.maxHeight = '650px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(btn) btn.textContent = 'Show More';
                } else {
                    container.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(btn) btn.textContent = 'Show Less';
                }
            }
        });

        // --- Modal Logic ---"""
)

# ISSUE 18: In the mobile menu click handler (line 526), when the menu
# opens, it sets display to flex via removing 'hidden'. But the element
# has class `hidden` (display:none) and removing it makes it display:block.
# The `flex-col items-center justify-center` classes require display:flex.
# Fix: explicitly add 'flex' class when showing.
js = js.replace(
    """                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');""",
    """                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');"""
)

# And when closing, add back hidden and remove flex
js = js.replace(
    """                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    setTimeout(() => mobileMenu.classList.add('hidden'), 300);
                }
            });
        }""",
    """                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    setTimeout(() => {
                        mobileMenu.classList.add('hidden');
                        mobileMenu.classList.remove('flex');
                    }, 300);
                }
            });
        }"""
)

# Also fix the close-on-click inside the menu items
js = js.replace(
    """                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                setTimeout(() => mobileMenu.classList.add('hidden'), 300);""",
    """                                mobileMenu.classList.remove('opacity-100');
                                mobileMenu.classList.add('opacity-0');
                                setTimeout(() => {
                                    mobileMenu.classList.add('hidden');
                                    mobileMenu.classList.remove('flex');
                                }, 300);"""
)

# ISSUE 19: The `enableInteractiveTerminal()` call on line 200 is inside
# the `executeCommand('./start-portfolio.sh')` handler but at a weird
# indentation level. It should be inside the setTimeout callback.
# Currently: 
#   Line 177: setTimeout(() => {
#   Line 193: buildTextMinimap(); populateMobileNav(); initializeAllAnimations();
#   Line 194-197: mobileNavbar logic
#   Line 200: enableInteractiveTerminal();  <-- this is BEFORE the closing }, 500)
#   Line 202: }, 500);
# This is actually correct - it's inside the setTimeout. Just messy indentation.

# ISSUE 20: The interests data keys don't match. In interestColors (line 577-583),
# the key is 'Sneaker Collecting' and 'Perfume Collecting', but in interestsData
# (line 437-438), the keys are 'Sneaker Enthusiast' and 'Perfume Collecting'.
# 'Sneaker Collecting' won't match 'Sneaker Enthusiast', so it falls back to grey.
js = js.replace(
    "'Sneaker Collecting': 'bg-purple-800/50 text-purple-300',",
    "'Sneaker Enthusiast': 'bg-purple-800/50 text-purple-300',"
)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed script.js")
print("\nAll fixes applied successfully.")
