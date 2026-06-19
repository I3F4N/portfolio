import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the Academic Foundations text overflow by renaming the id and data-text
html = html.replace('<section id="academic_foundations"', '<section id="education"')
html = html.replace('data-text="./academic_foundations.sh">./academic_foundations.sh</h2>', 'data-text="./education.sh">./education.sh</h2>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Fix Parallax lag
parallax_old = """        // --- Parallax Effect for Certificates ---
        function handleParallax() {
            const cards = document.querySelectorAll('.certificate-card .card-bg');
            cards.forEach(card => {
                const rect = card.parentElement.getBoundingClientRect();
                const speed = 0.2;
                const movement = -(rect.top - window.innerHeight / 2) * speed;
                 // Clamp the movement to prevent the background from moving too far
                const clampedMovement = Math.max(-50, Math.min(50, movement));
                card.style.transform = `translateY(${clampedMovement}px)`;
            });
        }"""

parallax_new = """        // --- Parallax Effect for Certificates ---
        let certCards = [];
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        function handleParallax() {
            if (prefersReducedMotion.matches) return;
            if (certCards.length === 0) certCards = document.querySelectorAll('.certificate-card .card-bg');
            
            const innerHeight = window.innerHeight;
            certCards.forEach(card => {
                const rect = card.parentElement.getBoundingClientRect();
                // Only calculate if the card is in or near the viewport
                if (rect.top < innerHeight + 200 && rect.bottom > -200) {
                    const speed = 0.2;
                    const movement = -(rect.top - innerHeight / 2) * speed;
                    const clampedMovement = Math.max(-50, Math.min(50, movement));
                    card.style.transform = `translateY(${clampedMovement}px)`;
                }
            });
        }"""

js = js.replace(parallax_old, parallax_new)

# Remove handleParallax from raf loop
raf_old = """        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
            handleParallax();
        }"""
raf_new = """        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        lenis.on('scroll', handleParallax);"""
js = js.replace(raf_old, raf_new)

# 2. Optimize Matrix Rain matchMedia
matrix_old = """        const drawMatrix = (time) => {
            if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {"""
matrix_new = """        const drawMatrix = (time) => {
            if (!prefersReducedMotion.matches) {"""
js = js.replace(matrix_old, matrix_new)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Lag fixed and text updated.")
