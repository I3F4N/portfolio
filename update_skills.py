import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to replace the skillsData object block.
# Let's find the start and end of skillsData
start_str = "        const skillsData = {"
start_idx = js.find(start_str)

if start_idx != -1:
    end_idx = js.find("};", start_idx)
    if end_idx != -1:
        new_skills_data = """        const skillsData = {
            'AI & Prompt Engineering': { title: 'AI & Prompt Engineering', description: 'Extensive experience leveraging LLMs (ChatGPT, Claude, Gemini) and AI coding assistants for rapid development, architecture planning, and debugging. Proficient in prompt engineering to automate workflows and optimize code generation.' },
            'AI-Assisted Development': { title: 'AI-Assisted Development', description: 'Utilizing AI tools to accelerate the software development lifecycle, from generating boilerplate code and writing unit tests to exploring complex algorithmic solutions and diagnosing network security issues.' },
            'Operating Systems': { title: 'Operating Systems', description: 'Experienced in the installation and configuration of several different operating systems across different platforms, and familiar with the file systems of both windows and linux.'},
            'Security & Pentesting': { title: 'Security & Pentesting', description: 'Proficient in threat analysis and mitigation with tools like Microsoft Certified Cybersecurity Analyst suite and Wazuh IDS. Hands-on experience from PortSwigger Web Security Core Labs (SQLi, XSS, CSRF), DDoS Mitigation, and implementing Role-Based Access Control (RBAC) and IdAM.'},
            'Networking & Infrastructure': { title: 'Networking & Infrastructure', description: 'Cisco CCNA certified with strong skills in Linux System Administration, TCP/IP, VLAN, DHCP, DNS, and VPN Setup & Troubleshooting. Experienced in server setup and security hardening.'},
            'Enterprise CCTV Networks': { title: 'Enterprise CCTV Networks', description: 'Expertise in the complete deployment of large-scale, enterprise-grade IP CCTV networks, including physical fiber-optic backbones and server room architecture.' },
            'Network Architecture': { title: 'Network Architecture', description: 'Skilled in auditing vulnerable network topologies and re-architecting them into highly resilient, scalable models with strict subnet isolation and VLAN tagging.' },
            'Incident Response': { title: 'Incident Response', description: 'Capable of rapid response and threat neutralization for catastrophic network failures, including Layer 2 broadcast storms, STP failures, and edge loops.' },
            'System Configuration': { title: 'System Configuration', description: 'Experience in configuring complex IT systems, including servers, networking equipment, and end-user devices for seamless enterprise operations.' },
            'DevOps & Automation': { title: 'DevOps & Automation', description: 'Skilled in using Docker for containerization, building and managing CI/CD Pipelines, and creating complex workflows with n8n. Proficient in Bash Scripting, and Sendmail/Mail Server Configuration.'},
            'Programming & Frameworks': { title: 'Programming & Frameworks', description: 'Fluent in Python, JavaScript, C++, and more, enabling the creation of complete, end-to-end applications and solutions.'},
            'Server Management': { title: 'Server Management', description: 'Expertise in setting up, configuring, and maintaining web servers (like Apache/Nginx), including VPS management, domain configuration, DNS, and ensuring high availability and performance.' },
            'Full-Stack Dev': { title: 'Full-Stack Development', description: 'Proficient in both front-end (HTML, CSS, JavaScript) and back-end development, enabling the creation of complete, end-to-end web applications.' },
            'Git/VCS': { title: 'Git / Version Control', description: 'Adept at using Git for version control, including branching, merging, and collaborating with teams on complex codebases. Essential for maintaining code integrity and managing project history.' },
            'eCommerce': { title: 'eCommerce Solutions', description: 'Broad experience with various e-commerce platforms like Bagisto and Wix, focusing on creating seamless online shopping experiences and custom sales funnels.' },
            'POS Systems': { title: 'Point-of-Sale (POS) Systems', description: 'Experience in developing and customizing POS software for retail and restaurants, including features like multi-outlet support, inventory management, and receipt/KOT printing.' },
            'Automation (n8n)': { title: 'Automation (n8n)', description: 'Using tools like n8n to create automated workflows that connect different apps and services, improving efficiency and reducing manual work for businesses.' },
            'Docker': { title: 'Docker', description: 'Utilizing Docker to containerize applications, ensuring consistent development and deployment environments, and simplifying the process of scaling applications.' },
            'Technical Support': { title: 'Technical Support', description: 'Proficient in diagnosing and resolving a wide range of hardware and software issues for users. Skilled in providing clear, friendly, and effective technical assistance to ensure smooth and reliable system operation.' },
            'PC Building': { title: 'PC Building', description: 'Experienced in custom PC building, from component selection and compatibility checking to assembly and performance tuning. Passionate about creating high-performance machines tailored for specific needs like gaming or development.' },
            'Polyglot / Languages': { title: 'Polyglot / Languages', description: 'Fluent in over 8 languages. Completely fluent in English, Hindi, Malayalam, Kannada, Urdu, Tamil, and Jeseri. Able to speak and understand Japanese, possess basic conversational Arabic, and currently holding a B2 level in French.' }"""
        
        js = js[:start_idx] + new_skills_data + js[end_idx:]
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Successfully updated skillsData in script.js!")
else:
    print("Warning: start_str not found in script.js!")

# Cache bust
import time
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={time.time()}', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Cache busted index.html")
