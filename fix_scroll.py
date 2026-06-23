import re

# ============================================================
# SCROLL PERFORMANCE & FEEL OPTIMIZATION
# ============================================================

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# === 1. OPTIMIZE LENIS CONFIG ===
# Default Lenis has no custom config. Add buttery smooth settings.
js = js.replace(
    "        const lenis = new Lenis();",
    """        const lenis = new Lenis({
            lerp: 0.07,
            smoothWheel: true,
            wheelMultiplier: 0.8,
            touchMultiplier: 1.5,
            infinite: false,
        });"""
)

# === 2. THROTTLE PARALLAX ===
# handleParallax fires on EVERY scroll frame. Use rAF to batch it.
js = js.replace(
    """        // --- Parallax Effect for Certificates ---
        let certCards = [];
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        function handleParallax() {
            if (prefersReducedMotion.matches) return;
            if (certCards.length === 0) certCards = document.querySelectorAll('.certificate-card .card-bg');
            
            const innerHeight = window.innerHeight;
            
            // Batch reads to avoid layout thrashing
            const updates = [];
            certCards.forEach(card => {
                const rect = card.parentElement.getBoundingClientRect();
                if (rect.top < innerHeight + 200 && rect.bottom > -200) {
                    updates.push({ card, rectTop: rect.top });
                }
            });
            
            // Batch writes
            updates.forEach(({ card, rectTop }) => {
                const speed = 0.2;
                const movement = -(rectTop - innerHeight / 2) * speed;
                const clampedMovement = Math.max(-50, Math.min(50, movement));
                card.style.transform = `translateY(${clampedMovement}px)`;
            });
        }""",
    """        // --- Parallax Effect for Certificates ---
        let certCards = [];
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        let parallaxTicking = false;
        function handleParallax() {
            if (prefersReducedMotion.matches || parallaxTicking) return;
            parallaxTicking = true;
            requestAnimationFrame(() => {
                if (certCards.length === 0) certCards = document.querySelectorAll('.certificate-card .card-bg');
                const innerHeight = window.innerHeight;
                for (let i = 0; i < certCards.length; i++) {
                    const card = certCards[i];
                    const rect = card.parentElement.getBoundingClientRect();
                    if (rect.top < innerHeight + 200 && rect.bottom > -200) {
                        const movement = -(rect.top - innerHeight / 2) * 0.2;
                        card.style.transform = `translateY(${Math.max(-50, Math.min(50, movement))}px)`;
                    }
                }
                parallaxTicking = false;
            });
        }"""
)

# === 3. THROTTLE MATRIX RAIN DURING SCROLL ===
# Reduce matrix FPS while user is actively scrolling to free up GPU.
js = js.replace(
    """        let lastTime = 0;
        function animateMatrix(time) {
            if (isTabActive) {
                if (time - lastTime > 33) { // ~30fps
                    drawMatrix();
                    lastTime = time;
                }
            }
            requestAnimationFrame(animateMatrix);
        }
        requestAnimationFrame(animateMatrix);""",
    """        let lastTime = 0;
        let isScrolling = false;
        let scrollTimeout = null;
        function animateMatrix(time) {
            if (isTabActive) {
                const interval = isScrolling ? 80 : 33; // ~12fps while scrolling, ~30fps idle
                if (time - lastTime > interval) {
                    drawMatrix();
                    lastTime = time;
                }
            }
            requestAnimationFrame(animateMatrix);
        }
        requestAnimationFrame(animateMatrix);"""
)

# Hook into Lenis scroll to set isScrolling flag
js = js.replace(
    "        lenis.on('scroll', handleParallax);",
    """        lenis.on('scroll', () => {
            handleParallax();
            isScrolling = true;
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => { isScrolling = false; }, 150);
        });"""
)

# === 4. PASSIVE EVENT LISTENERS ===
# The mousemove spotlight should be passive
js = js.replace(
    """        document.body.addEventListener('mousemove', e => {
            document.documentElement.style.setProperty('--x', e.clientX + 'px');
            document.documentElement.style.setProperty('--y', e.clientY + 'px');
        });""",
    """        document.body.addEventListener('mousemove', e => {
            document.documentElement.style.setProperty('--x', e.clientX + 'px');
            document.documentElement.style.setProperty('--y', e.clientY + 'px');
        }, { passive: true });"""
)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed script.js")

# === 5. CSS PERFORMANCE HINTS ===
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add GPU acceleration hints for animated elements
css = css.replace(
    """        .reveal {
            opacity: 0;
            transform: translateY(40px);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        }
        .reveal.visible {
            opacity: 1;
            transform: translateY(0);
        }""",
    """        .reveal {
            opacity: 0;
            transform: translateY(40px);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
            will-change: opacity, transform;
        }
        .reveal.visible {
            opacity: 1;
            transform: translateY(0);
            will-change: auto;
        }"""
)

# GPU-promote the certificate card backgrounds for smooth parallax
css = css.replace(
    """        .certificate-card .card-bg {
            width: 100%;
            height: 150%; /* Taller to allow for movement */
            background-size: cover;
            background-position: center;
            position: absolute;
            top: -25%; /* Start in the middle */
            left: 0;
            transition: transform 0.1s linear;
        }""",
    """        .certificate-card .card-bg {
            width: 100%;
            height: 150%; /* Taller to allow for movement */
            background-size: cover;
            background-position: center;
            position: absolute;
            top: -25%; /* Start in the middle */
            left: 0;
            will-change: transform;
            transform: translateZ(0); /* GPU layer promotion */
        }"""
)

# GPU-promote the matrix canvas
css = css.replace(
    """        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.15;
        }""",
    """        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.15;
            will-change: contents;
            transform: translateZ(0);
        }"""
)

# Promote interactive cards to their own layers so hover transforms don't repaint siblings
css = css.replace(
    """        .clickable-tag, .project-card, .certificate-card, .experience-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #30363d;
        }""",
    """        .clickable-tag, .project-card, .certificate-card, .experience-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #30363d;
            transform: translateZ(0);
            backface-visibility: hidden;
        }"""
)

# Optimize education logos - constrain height to prevent layout shift
css += """
/* Performance: contain layout for cards */
.experience-card, .project-card {
    contain: layout style;
}

/* Optimize logo images */
.experience-card img {
    aspect-ratio: auto;
    object-fit: contain;
}

/* Smooth transitions on all interactive elements */
a, button, .clickable-tag {
    -webkit-tap-highlight-color: transparent;
}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed style.css")
print("\nAll scroll optimizations applied.")
