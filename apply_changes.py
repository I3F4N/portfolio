import re

# 1. UPDATE index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update About section
about_match = re.search(r'(<section id="about" class="mb-16 reveal">.*?</section>)', html, re.DOTALL)
if about_match:
    new_about = """<section id="about" class="mb-16 reveal">
                <h2 class="glitch-title text-3xl font-bold text-green-400 mb-6 border-b-2 border-green-400/30 pb-2" data-text="./about.sh">./about.sh</h2>
                <div class="text-lg leading-relaxed bg-[#161b22]/70 p-6 rounded-md border border-gray-700">
                    <p data-scramble-text>I am a technology professional specializing in cybersecurity, network infrastructure, and system deployment. My background spans both physical network architecture and software development, giving me a comprehensive view of how enterprise systems operate from the physical layer up to the application level.<br><br>I focus on building secure, scalable, and resilient IT environments. Rather than treating security as an afterthought, I integrate it directly into the infrastructure and applications I deploy. My goal is to design technology solutions that solve complex business problems efficiently and securely, without creating unnecessary friction for the end user.</p>
                </div>
            </section>"""
    html = html.replace(about_match.group(1), new_about)

# Update Experience section to include Sonet correctly
exp_match = re.search(r'(<section id="experience" class="mb-16 reveal">.*?</section>)', html, re.DOTALL)
if exp_match:
    # Build the full experience section cleanly
    new_exp = """<section id="experience" class="mb-16 reveal">
                <h2 class="glitch-title text-3xl font-bold text-green-400 mb-6 border-b-2 border-green-400/30 pb-2" data-text="./experience.sh">./experience.sh</h2>
                <div class="space-y-8">
                     <!-- Sonet Role -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.1s;">
                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="sonet.png" alt="Sonet Logo" class="w-48 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-blue-400">Network & Security Infrastructure Consultant</h3>
                                <p class="text-gray-400 mb-2">Sonet Integrated Solutions (Titan Company Project) • Jan 2026 – Jun 2026 | Chikkaballapur</p>
                                <ul class="list-disc list-inside text-gray-400 space-y-2 mt-4">
                                    <li><strong class="text-gray-200">Enterprise Deployment:</strong> Engineered the complete Layer 1 to Layer 3 deployment of a 152-node enterprise IP CCTV network. Designed the physical fiber-optic backbone and server room architecture to eliminate physical security risks.</li>
                                    <li><strong class="text-gray-200">Threat Neutralization (Internal DoS):</strong> Acted as the primary incident responder for a catastrophic campus-wide Layer 2 broadcast storm. Diagnosed the spanning tree failure and edge loop, isolated the compromised nodes, and restored 100% network availability with zero data loss.</li>
                                    <li><strong class="text-gray-200">Topology Re-Architecture:</strong> Audited a vulnerable, legacy daisy-chain network topology and completely re-architected it into a highly resilient Hub-and-Spoke model. Enforced strict subnet isolation and VLAN tagging to prevent lateral propagation of edge-device failures and mitigate future STP vulnerabilities.</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                     <!-- CtrlWeb Role -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.2s;">
                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="ctrlweb.png" alt="CtrlWeb Logo" class="w-48 h-auto">
                            <div>
                                <h3 class="text-2xl font-bold text-blue-400">Co-Founder & CTO</h3>
                                <p class="text-gray-400 mb-2">CtrlWeb • June 2024 - Present</p>
                                <p class="text-lg italic text-green-400 mb-4">"Driving Innovation and Growth"</p>
                                <ul class="list-disc list-inside text-gray-400 space-y-2">
                                    <li>Spearheaded the founding and scaling of an end-to-end IT consultancy, delivering a portfolio of web, software and infrastructure solutions.</li>
                                    <li>Engineered a bespoke, multi-outlet Point-of-Sale (POS) system from the ground up using PHP/JS and Git.</li>
                                    <li>Implemented and administered self-hosted n8n automation servers on Linux for multiple clients.</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!-- E&P Role -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.3s;">
                        <div class="flex flex-col sm:flex-row items-center gap-8">
                             <img src="e&p.PNG" alt="E&P Logo" class="w-48 h-auto rounded-lg">
                            <div class="flex-1">
                                <div class="mb-6">
                                    <h3 class="text-2xl font-bold text-blue-400">Infrastructure Engineer</h3>
                                    <p class="text-gray-400 mb-4">E&P International Ventures • Nov 2024 – Sep 2025</p>
                                    <ul class="list-disc list-inside text-gray-400 space-y-2">
                                        <li>Architected and deployed the comprehensive IT and network infrastructure for a new 13-outlet commercial campus in Shoolagiri and several distributed franchised outlets.</li>
                                        <li>Evaluated, selected, and integrated the complete technology stack across the campus, including specialized Point-of-Sale (POS) systems.</li>
                                        <li>Led the end-to-end development and deployment of the corporate website and managed ongoing IT initiatives.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                     <!-- Basik Marketing Role -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.4s;">
                        <div>
                            <h3 class="text-2xl font-bold text-blue-400">System and Network Security Admin Intern</h3>
                            <p class="text-gray-400 mb-4">Basik Marketing Pvt. Ltd. • Jul 2024 – Oct 2024</p>
                            <ul class="list-disc list-inside text-gray-400 space-y-2">
                                <li>Managed core network infrastructure uptime and performance against threats, actively deploying backup link failover routing during critical power disruptions to eliminate dropped packets on live streams.</li>
                                <li>Documented corporate IT systems and created comprehensive network diagrams to optimize the internal knowledge base.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>"""
    html = html.replace(exp_match.group(1), new_exp)

# Update Academic Foundations section
acad_match = re.search(r'(<section id="(?:journey|academic_foundations)".*?</section>)', html, re.DOTALL)
if acad_match:
    new_acad = """<section id="academic_foundations" class="mb-16 reveal">
                <h2 class="glitch-title text-3xl font-bold text-green-400 mb-6 border-b-2 border-green-400/30 pb-2" data-text="./academic_foundations.sh">./academic_foundations.sh</h2>
                <div class="space-y-8">
                     <!-- Garden City University -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.1s;">
                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="logos/gardencity.png" alt="Garden City University Logo" class="w-32 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-blue-400">Garden City University</h3>
                                <p class="text-gray-400 mb-2">2022 - 2026</p>
                                <p class="text-lg italic text-green-400 mb-4">"Graduated with a B.Tech in Computer Science (IT-Cyber Security)"</p>
                                <p class="text-gray-400">Successfully completed my degree with a specialization in Cyber Security, deepening my academic knowledge in the field and graduating with First Class Distinction (CGPA: 9.07 / 10.0).</p>
                            </div>
                        </div>
                    </div>
                    <!-- Presidency School -->
                    <div class="experience-card bg-[#161b22]/70 p-6 sm:p-8 rounded-md reveal reveal-child" style="--delay: 0.2s;">
                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="logos/presidency.png" alt="Presidency School Logo" class="w-32 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-blue-400">Presidency School (Grades 1 - 12)</h3>
                                <p class="text-gray-400 mb-2">Foundation</p>
                                <p class="text-gray-400">Completed my schooling in the CBSE stream, choosing Science with Computer Science in 11th and 12th grade to build a strong technical foundation.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>"""
    html = html.replace(acad_match.group(1), new_acad)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. UPDATE script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Projects array
projects_match = re.search(r'const projects = \[\s*(\{.*?})\s*\];', js, re.DOTALL)
if projects_match:
    old_projects = projects_match.group(0)
    
    new_projects_data = """const projects = [
            { title: "Enterprise Security Infrastructure (Sonet)", url: "#", role: "Network Infrastructure Consultant", description: "Engineered a highly resilient Hub-and-Spoke enterprise network for Titan Company Ltd. Directed end-to-end Layer 1 to Layer 3 deployment, including precision fiber-optic (OFC) splicing, secure server room architecture, and a 152-node IP CCTV network. Implemented strict VLAN segmentation to neutralize internal threats, successfully mitigating a severe Layer 2 broadcast storm.", tech: ["Cisco", "OFC", "IP CCTV", "VLANs", "STP"] },
            { title: "Self-Hosted Enterprise Automation (CtrlWeb)", url: "#", role: "Infrastructure Lead", description: "The Architecture: Deployed n8n automation servers strictly on hardened, self-hosted Linux environments to maintain data sovereignty for SME clients. The Security: Configured secure, webhook-driven workflows for encrypted cross-platform transactions, ensuring zero external exposure of core business system endpoints.", tech: ["n8n", "Linux", "Webhooks", "Docker"] },
            { title: "Secure Multi-Tenant POS Architecture", url: "#", role: "Full-Stack & Security Engineer", description: "The Problem: High-density commercial campuses require POS systems that can handle concurrent transactions offline while maintaining strict data isolation between vendors. The Architecture: Developed a custom POS ecosystem using PHP/JS and Git. The Security: Implemented strict Role-Based Access Control (RBAC), secure session management, and cross-tenant data isolation.", tech: ["PHP", "JavaScript", "MySQL", "RBAC", "Git"] },
            { title: "Pioneer Ceilings", url: "https://pioneerceilings.com", role: "Website Developer & Host Manager", description: "A WordPress site for a ceilings company, utilizing WooCommerce for its product showcase. I handled the complete site setup, theme and plugin configuration, and provide ongoing hosting management.", tech: ["WordPress", "WooCommerce", "Hostinger", "PHP"] },
            { title: "Elephant & Peacock POS", url: "https://eandppos.in", role: "POS Software Developer", description: "A complete, custom-built Point-of-Sale software for a retail client. The system supports multiple outlets, receipt and Kitchen Order Ticket (KOT) printing, and the entire codebase is version-controlled with Git.", tech: ["Custom POS", "PHP", "JavaScript", "Git", "MySQL"] },
            { title: "eandp.in eCommerce", url: "https://eandp.in", role: "eCommerce Developer", description: "Developed and deployed a clothing retail eCommerce website. Managed domain purchasing and hosting, utilizing Wix as the site builder for certain workflows while managing multiple related sites on Hostinger.", tech: ["Wix", "eCommerce", "Hostinger", "Domain Mgmt"] },
            { title: "Bagisto Sales Lead Checkout", url: "#", role: "eCommerce Developer", description: "Customized a Bagisto (Laravel-based) eCommerce platform to bypass the payment gateway. Instead, checkout details are captured and routed directly to the sales team via email and WhatsApp/SMS using a custom 'SalesLeadCheckout' package and Twilio integration.", tech: ["Bagisto", "Laravel", "PHP", "Twilio API"] },
            { title: "NF Solutions Website", url: "#", role: "Frontend & Site Implementer", description: "Designed and deployed a multi-page marketing website for an interior design company in Lucknow. Handled the complete design, content layout, and deployment with a CMS integration.", tech: ["HTML", "CSS", "JavaScript", "CMS"] },
            { title: "Royalwood Furniture eCommerce", url: "https://royalwoodfurniture.com", role: "Full-Stack Developer", description: "Developed a complete eCommerce website for a furniture business from the ground up, featuring a full product catalog, shopping cart, and checkout functionality.", tech: ["WordPress", "WooCommerce", "eCommerce", "PHP"] },
            { title: "OpenSourcePOS Integration", url: "#", role: "POS Integrator", description: "Installed and customized OpenSourcePOS for a restaurant client. The project involved domain setup via GoDaddy, server configuration, and tailoring the POS features to meet specific needs like KOT and receipt formats.", tech: ["OpenSourcePOS", "GoDaddy", "Server Setup", "PHP"] },
            { title: "Self-Hosted ERPNext Setup", url: "#", role: "Systems Engineer", description: "Deployed, configured, and maintain a self-hosted instance of ERPNext on a private server. This involved the complete setup and customization of the open-source ERP for business management.", tech: ["ERPNext", "Linux", "Docker", "Self-Hosting"] }
        ];"""
    js = js.replace(old_projects, new_projects_data)

# Update terminal cat resume.txt logic
terminal_match = re.search(r"else if \(cmdLower === 'cat resume\.txt'\) \{.*?}", js, re.DOTALL)
if terminal_match:
    new_terminal = """else if (cmdLower === 'cat resume.txt') {
                outputLine.innerHTML = `Irfan Ahmad - Cybersecurity Professional<br/>
                Specialization: Network Infrastructure & System Deployment<br/>
                Experience: Sonet Integrated Solutions, CtrlWeb, E&P International<br/>
                Focus: Secure, scalable, and resilient IT environments.`;
                outputEl.appendChild(outputLine);
            }"""
    js = js.replace(terminal_match.group(0), new_terminal)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("HTML and JS updated successfully.")
