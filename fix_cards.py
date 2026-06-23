import re

def update_file(filename, replacements):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find segment in {filename}:\n{old[:50]}...")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Experience Cards Replacements
rep_sonet_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="sonet.png" alt="Sonet Logo" class="w-48 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-gray-100">Network & Security Infrastructure Consultant</h3>
                                <p class="text-gray-400 mb-2">Sonet Integrated Solutions (Titan Company Project) • Jan 2026 – Jun 2026 | Chikkaballapur</p>
                                <ul class="list-disc list-inside text-gray-400 space-y-2 mt-4">
                                    <li><strong class="text-gray-200">Enterprise Deployment:</strong> Engineered the complete Layer 1 to Layer 3 deployment of a 152-node enterprise IP CCTV network. Designed the physical fiber-optic backbone and server room architecture to eliminate physical security risks.</li>
                                    <li><strong class="text-gray-200">Threat Neutralization (Internal DoS):</strong> Acted as the primary incident responder for a catastrophic campus-wide Layer 2 broadcast storm. Diagnosed the spanning tree failure and edge loop, isolated the compromised nodes, and restored 100% network availability with zero data loss.</li>
                                    <li><strong class="text-gray-200">Topology Re-Architecture:</strong> Audited a vulnerable, legacy daisy-chain network topology and completely re-architected it into a highly resilient Hub-and-Spoke model. Enforced strict subnet isolation and VLAN tagging to prevent lateral propagation of edge-device failures and mitigate future STP vulnerabilities.</li>
                                </ul>
                            </div>
                        </div>"""
rep_sonet_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                            <img src="sonet.png" alt="Sonet Logo" class="w-24 sm:w-48 h-auto bg-white p-2 rounded-lg object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">Network & Security Infrastructure Consultant</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">Sonet Integrated Solutions (Titan Company Project) • Jan 2026 – Jun 2026 | Chikkaballapur</p>
                            </div>
                        </div>
                        <ul class="list-disc list-inside text-sm sm:text-base text-gray-400 space-y-2">
                            <li><strong class="text-gray-200">Enterprise Deployment:</strong> Engineered the complete Layer 1 to Layer 3 deployment of a 152-node enterprise IP CCTV network. Designed the physical fiber-optic backbone and server room architecture to eliminate physical security risks.</li>
                            <li><strong class="text-gray-200">Threat Neutralization (Internal DoS):</strong> Acted as the primary incident responder for a catastrophic campus-wide Layer 2 broadcast storm. Diagnosed the spanning tree failure and edge loop, isolated the compromised nodes, and restored 100% network availability with zero data loss.</li>
                            <li><strong class="text-gray-200">Topology Re-Architecture:</strong> Audited a vulnerable, legacy daisy-chain network topology and completely re-architected it into a highly resilient Hub-and-Spoke model. Enforced strict subnet isolation and VLAN tagging to prevent lateral propagation of edge-device failures and mitigate future STP vulnerabilities.</li>
                        </ul>"""

rep_ctrlweb_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="ctrlweb.png" alt="CtrlWeb Logo" class="w-48 h-auto">
                            <div>
                                <h3 class="text-2xl font-bold text-gray-100">Founder</h3>
                                <p class="text-gray-400 mb-2">CtrlWeb • June 2024 - Present</p>
                                <p class="text-lg italic text-gray-400 mb-4 border-l-2 border-green-500/50 pl-4">"Driving Innovation and Growth"</p>
                                <ul class="list-disc list-inside text-gray-400 space-y-2">
                                    <li>Spearheaded the founding and scaling of an end-to-end IT consultancy, delivering a portfolio of web, software and infrastructure solutions.</li>
                                    <li>Engineered a bespoke, multi-outlet Point-of-Sale (POS) system from the ground up using PHP/JS and Git.</li>
                                    <li>Implemented and administered self-hosted n8n automation servers on Linux for multiple clients.</li>
                                </ul>
                            </div>
                        </div>"""
rep_ctrlweb_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                            <img src="ctrlweb.png" alt="CtrlWeb Logo" class="w-24 sm:w-48 h-auto object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">Founder</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">CtrlWeb • June 2024 - Present</p>
                            </div>
                        </div>
                        <p class="text-sm sm:text-lg italic text-gray-400 mb-4 border-l-2 border-green-500/50 pl-4">"Driving Innovation and Growth"</p>
                        <ul class="list-disc list-inside text-sm sm:text-base text-gray-400 space-y-2">
                            <li>Spearheaded the founding and scaling of an end-to-end IT consultancy, delivering a portfolio of web, software and infrastructure solutions.</li>
                            <li>Engineered a bespoke, multi-outlet Point-of-Sale (POS) system from the ground up using PHP/JS and Git.</li>
                            <li>Implemented and administered self-hosted n8n automation servers on Linux for multiple clients.</li>
                        </ul>"""

rep_ep_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                             <img src="e&p.PNG" alt="E&P Logo" class="w-48 h-auto rounded-lg">
                            <div class="flex-1">
                                <div class="mb-6">
                                    <h3 class="text-2xl font-bold text-gray-100">Infrastructure Engineer</h3>
                                    <p class="text-gray-400 mb-4">E&P International Ventures • Nov 2024 – Sep 2025</p>
                                    <ul class="list-disc list-inside text-gray-400 space-y-2">
                                        <li>Architected and deployed the comprehensive IT and network infrastructure for a new 13-outlet commercial campus in Shoolagiri and several distributed franchised outlets.</li>
                                        <li>Evaluated, selected, and integrated the complete technology stack across the campus, including specialized Point-of-Sale (POS) systems.</li>
                                        <li>Led the end-to-end development and deployment of the corporate website and managed ongoing IT initiatives.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>"""
rep_ep_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                             <img src="e&p.PNG" alt="E&P Logo" class="w-24 sm:w-48 h-auto rounded-lg object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">Infrastructure Engineer</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">E&P International Ventures • Nov 2024 – Sep 2025</p>
                            </div>
                        </div>
                        <ul class="list-disc list-inside text-sm sm:text-base text-gray-400 space-y-2">
                            <li>Architected and deployed the comprehensive IT and network infrastructure for a new 13-outlet commercial campus in Shoolagiri and several distributed franchised outlets.</li>
                            <li>Evaluated, selected, and integrated the complete technology stack across the campus, including specialized Point-of-Sale (POS) systems.</li>
                            <li>Led the end-to-end development and deployment of the corporate website and managed ongoing IT initiatives.</li>
                        </ul>"""

rep_basik_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="basik.PNG" alt="Basik Logo" class="w-48 h-auto rounded-lg">
                            <div class="flex-1">
                                <h3 class="text-2xl font-bold text-gray-100">Website & Database Administrator</h3>
                                <p class="text-gray-400 mb-4">Basik Marketing Pvt. Ltd. • Jul 2024 – Oct 2024</p>
                                <ul class="list-disc list-inside text-gray-400 space-y-2">
                                    <li>Redesigned and managed the corporate website, ensuring a high-performance, responsive user experience.</li>
                                    <li>Administered and maintained the company's SQL database infrastructure.</li>
                                    <li>Handled general IT support and troubleshooting for staff operations.</li>
                                </ul>
                            </div>
                        </div>"""
rep_basik_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                            <img src="basik.PNG" alt="Basik Logo" class="w-24 sm:w-48 h-auto rounded-lg object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">Website & Database Administrator</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">Basik Marketing Pvt. Ltd. • Jul 2024 – Oct 2024</p>
                            </div>
                        </div>
                        <ul class="list-disc list-inside text-sm sm:text-base text-gray-400 space-y-2">
                            <li>Redesigned and managed the corporate website, ensuring a high-performance, responsive user experience.</li>
                            <li>Administered and maintained the company's SQL database infrastructure.</li>
                            <li>Handled general IT support and troubleshooting for staff operations.</li>
                        </ul>"""

rep_garden_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="logos/gardencity.png" alt="Garden City University Logo" class="w-32 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-gray-100">BSc Cyber Security</h3>
                                <p class="text-gray-400 mb-2">2022 - 2026</p>
                                <p class="text-gray-400">Successfully completed my degree with a specialization in Cyber Security, deepening my academic knowledge in the field and graduating with First Class Distinction (CGPA: 9.07 / 10.0).</p>
                            </div>
                        </div>"""
rep_garden_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                            <img src="logos/gardencity.png" alt="Garden City University Logo" class="w-16 sm:w-32 h-auto bg-white p-2 rounded-lg object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">BSc Cyber Security</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">2022 - 2026</p>
                            </div>
                        </div>
                        <p class="text-sm sm:text-base text-gray-400">Successfully completed my degree with a specialization in Cyber Security, deepening my academic knowledge in the field and graduating with First Class Distinction (CGPA: 9.07 / 10.0).</p>"""

rep_pres_old = """                        <div class="flex flex-col sm:flex-row items-center gap-8">
                            <img src="logos/presidency.png" alt="Presidency School Logo" class="w-32 h-auto bg-white p-2 rounded-lg">
                            <div>
                                <h3 class="text-2xl font-bold text-gray-100">Science PCMC</h3>
                                <p class="text-gray-400 mb-2">2020 - 2022</p>
                                <p class="text-gray-400">Completed my Pre-University education focusing on Physics, Chemistry, Mathematics, and Computer Science with an overall score of 87%.</p>
                            </div>
                        </div>"""
rep_pres_new = """                        <div class="flex flex-row sm:flex-row items-center sm:items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
                            <img src="logos/presidency.png" alt="Presidency School Logo" class="w-16 sm:w-32 h-auto bg-white p-2 rounded-lg object-contain">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-2xl font-bold text-gray-100 leading-tight">Science PCMC</h3>
                                <p class="text-xs sm:text-base text-gray-400 mt-1 sm:mt-2">2020 - 2022</p>
                            </div>
                        </div>
                        <p class="text-sm sm:text-base text-gray-400">Completed my Pre-University education focusing on Physics, Chemistry, Mathematics, and Computer Science with an overall score of 87%.</p>"""

update_file('index.html', [
    (rep_sonet_old, rep_sonet_new),
    (rep_ctrlweb_old, rep_ctrlweb_new),
    (rep_ep_old, rep_ep_new),
    (rep_basik_old, rep_basik_new),
    (rep_garden_old, rep_garden_new),
    (rep_pres_old, rep_pres_new)
])

print("Finished HTML updates.")
