import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add AI skills to skillsData
skills_target = """        const skillsData = {"""
skills_replacement = """        const skillsData = {
            'AI & Prompt Engineering': { title: 'AI & Prompt Engineering', description: 'Extensive experience leveraging LLMs (ChatGPT, Claude, Gemini) and AI coding assistants for rapid development, architecture planning, and debugging. Proficient in prompt engineering to automate workflows and optimize code generation.' },
            'AI-Assisted Development': { title: 'AI-Assisted Development', description: 'Utilizing AI tools to accelerate the software development lifecycle, from generating boilerplate code and writing unit tests to exploring complex algorithmic solutions and diagnosing network security issues.' },"""
js = js.replace(skills_target, skills_replacement)

# 2. Fix the freeze by adding visibilitychange logic
# I need to find the Lenis raf loop and Matrix drawMatrix loop.
lenis_raf_target = """        // --- Lenis Smooth Scroll ---
        const lenis = new Lenis();
        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        lenis.on('scroll', handleParallax);
        requestAnimationFrame(raf);"""

lenis_raf_replacement = """        // --- Lenis Smooth Scroll & Visibility Fix ---
        let isTabActive = true;
        document.addEventListener("visibilitychange", () => {
            isTabActive = !document.hidden;
            if (isTabActive) {
                lastTime = performance.now(); // Prevent massive time jumps when returning
            }
        });

        const lenis = new Lenis();
        function raf(time) {
            if (isTabActive) {
                lenis.raf(time);
            }
            requestAnimationFrame(raf);
        }
        lenis.on('scroll', handleParallax);
        requestAnimationFrame(raf);"""

js = js.replace(lenis_raf_target, lenis_raf_replacement)

# Let's also wrap the Matrix loop with isTabActive
matrix_target = """        const drawMatrix = (time) => {
            if (!prefersReducedMotion.matches) {
                if (time - lastTime > 33) {"""

matrix_replacement = """        const drawMatrix = (time) => {
            if (isTabActive && !prefersReducedMotion.matches) {
                if (time - lastTime > 33) {"""

js = js.replace(matrix_target, matrix_replacement)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js successfully")
