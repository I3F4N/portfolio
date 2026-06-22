import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Pioneer Ceilings URL to "#"
js = js.replace('{ title: "Pioneer Ceilings", url: "https://pioneerceilings.com"', '{ title: "Pioneer Ceilings", url: "#"')

# 2. Add new project
new_project = """            { title: "Custom Enterprise Invoicing Software", url: "#", role: "Implementation & Deployment Lead", description: "Deployed and customized a scalable, self-hosted invoicing and billing solution for multiple enterprise clients. Integrated automated payment workflows, recurring billing, and branded client portals. This enabled businesses to streamline financial operations and maintain complete data sovereignty while eliminating recurring SaaS overhead.", tech: ["Self-Hosted", "PHP", "MySQL", "Docker", "Billing Automation"] },
            { title: "Self-Hosted Enterprise Automation (CtrlWeb)", url: "#", role: "Founder", description: "The Architecture: Deployed n8n automation servers strictly on hardened, self-hosted Linux environments to maintain data sovereignty for SME clients. The Security: Configured secure, webhook-driven workflows for encrypted cross-platform transactions, ensuring zero external exposure of core business system endpoints.", tech: ["n8n", "Linux", "Webhooks", "Docker"] },"""
js = js.replace('            { title: "Self-Hosted Enterprise Automation (CtrlWeb)", url: "#", role: "Founder", description: "The Architecture: Deployed n8n automation servers strictly on hardened, self-hosted Linux environments to maintain data sovereignty for SME clients. The Security: Configured secure, webhook-driven workflows for encrypted cross-platform transactions, ensuring zero external exposure of core business system endpoints.", tech: ["n8n", "Linux", "Webhooks", "Docker"] },', new_project)

# 3. Fix Parallax Scroll Lag
old_parallax = """        function handleParallax() {
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

new_parallax = """        function handleParallax() {
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
        }"""

js = js.replace(old_parallax, new_parallax)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.js with projects and parallax fix.")
