// --- Sound Engine ---
        let isMuted = false;
        let audioInitialized = false;
        const muteButton = document.getElementById('mute-button');
        const speakerIcon = `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>`;
        const mutedIcon = `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" clip-rule="evenodd"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"></path></svg>`;
        muteButton.innerHTML = speakerIcon;

        const synth = new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: 'sine' },
            envelope: { attack: 0.005, decay: 0.1, sustain: 0.3, release: 0.1 },
            volume: -20
        }).toDestination();
        
        const typingSynth = new Tone.MembraneSynth({
            pitchDecay: 0.008,
            octaves: 3,
            oscillator: { type: 'sine' },
            envelope: { attack: 0.001, decay: 0.15, sustain: 0.01, release: 0.05, attackCurve: 'exponential' },
            volume: -18
        }).toDestination();

        const typingNoise = new Tone.NoiseSynth({
            noise: { type: 'brown' },
            envelope: { attack: 0.001, decay: 0.02, sustain: 0, release: 0.02 },
            volume: -30
        }).toDestination();

        function playHoverSound() { if (!isMuted && audioInitialized) synth.triggerAttackRelease('C2', '8n'); }
        function playClickSound() { if (!isMuted && audioInitialized) synth.triggerAttackRelease('C4', '8n'); }
        function playTypingSound() {
            if (!isMuted && audioInitialized) {
                const pitch = ['C3', 'C#3', 'D3', 'D#3'][Math.floor(Math.random() * 4)];
                typingSynth.triggerAttackRelease(pitch, '32n', Tone.now());
                typingNoise.triggerAttack(Tone.now());
            }
        }

        muteButton.addEventListener('click', () => {
            isMuted = !isMuted;
            muteButton.innerHTML = isMuted ? mutedIcon : speakerIcon;
            playClickSound();
        });
        
        // --- Lenis Smooth Scroll & Visibility Fix ---
        let isTabActive = true;
        document.addEventListener("visibilitychange", () => {
            isTabActive = !document.hidden;
            if (isTabActive) {
                lastTime = performance.now(); // Prevent massive time jumps when returning
            }
        });

        const lenis = new Lenis({
            lerp: 0.07,
            smoothWheel: true,
            wheelMultiplier: 0.8,
            touchMultiplier: 1.5,
            infinite: false,
        });
        function raf(time) {
            if (isTabActive) {
                lenis.raf(time);
            }
            requestAnimationFrame(raf);
        }
        lenis.on('scroll', () => {
            handleParallax();
            isScrolling = true;
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => { isScrolling = false; }, 150);
        });
        requestAnimationFrame(raf);

        // --- Mouse Spotlight Effect ---
        document.body.addEventListener('mousemove', e => {
            document.documentElement.style.setProperty('--x', e.clientX + 'px');
            document.documentElement.style.setProperty('--y', e.clientY + 'px');
        }, { passive: true });

        const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
        function updateInteractiveElements() {
            if (isTouchDevice) return;
            // Using event delegation on document body to avoid duplicate listeners and improve performance
            document.body.addEventListener('mouseover', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target && !target._hovered) {
                    
                    playHoverSound();
                    target._hovered = true;
                }
            });
            document.body.addEventListener('mouseout', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target) {
                    
                    target._hovered = false;
                }
            });
            document.body.addEventListener('click', (e) => {
                const target = e.target.closest('a, button, .project-card, .skill-tag, .close-button, .clickable-tag, #mute-button, .certificate-card, .experience-card, .nav-link, #nav-trigger');
                if (target) {
                    playClickSound();
                }
            });
        }

        // --- Matrix Rain Animation ---
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        const alphabet = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const fontSize = 16;
        let columns = Math.floor(width / fontSize);
        let rainDrops = Array.from({ length: columns }).fill(1);

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, width, height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                if (rainDrops[i] * fontSize > height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        }
        let lastTime = 0;
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
        requestAnimationFrame(animateMatrix);

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            columns = Math.floor(width / fontSize);
            rainDrops = Array.from({ length: columns }).fill(1);
        });

        // --- Boot Sequence State ---
        let isBooting = true;
        let commandIndex = 0;
        let charIndex = 0;
        let bootSequenceTimeout = null;
        let outputEl = document.getElementById('output');
        const commandInputEl = document.getElementById('command-input');
        let terminalBody = document.getElementById('terminal-body');

        const commands = [
            { cmd: 'Booting Antigravity OS v9.4.2...', isCommand: false, delay: 30 },
            { cmd: '[ OK ] Reached target Basic System.', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: '[ OK ] Started Hardware RNG Entropy Gatherer Daemon.', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: 'Mounting /dev/nvme0n1p2 on /root... ', isCommand: false, delay: 50 },
            { cmd: 'SUCCESS', isCommand: false, color: 'text-green-400', append: true, delay: 20 },
            { cmd: 'Starting Secure Shell server...', isCommand: false, delay: 30 },
            { cmd: '[ OK ] Listening on 0.0.0.0:22', isCommand: false, color: 'text-green-400', delay: 20 },
            { cmd: 'Decrypting local user vault... ', isCommand: false, delay: 80 },
            { cmd: 'ACCESS GRANTED', isCommand: false, color: 'text-green-400', append: true, delay: 40 },
            { cmd: 'Loading holographic interface modules... done.', isCommand: false, delay: 30 },
            { cmd: 'Welcome to the network.', isCommand: false, color: 'text-blue-400', delay: 100 },
            { cmd: '', isCommand: false, delay: 100 },
            { cmd: './start-portfolio.sh', isCommand: true, delay: 150 },
        ];

        function skipBootSequence() {
            if (!isBooting) return;
            isBooting = false;
            clearTimeout(bootSequenceTimeout);
            const hint = document.getElementById('skip-hint');
            if (hint) hint.style.opacity = '0';
            const progressContainer = document.getElementById('boot-progress-container');
            if (progressContainer) progressContainer.style.opacity = '0';
            const bootOverlay = document.getElementById('boot-overlay');
            if (bootOverlay) {
                bootOverlay.classList.add('opacity-0');
                setTimeout(() => bootOverlay.style.display = 'none', 1000);
            }
            const mainContent = document.getElementById('layout-wrapper');
            if (mainContent) {
                mainContent.classList.remove('hidden');
                setTimeout(() => mainContent.classList.add('opacity-100'), 50);
            }
            buildTextMinimap(); populateMobileNav(); initializeAllAnimations();
            const mobileNavbar = document.getElementById('mobile-navbar');
            if (mobileNavbar) {
                mobileNavbar.classList.remove('-translate-y-full');
            }
            enableInteractiveTerminal();
        }

        // Add event listener to skip boot sequence
        document.addEventListener('keydown', (e) => {
            if (isBooting && (e.key === 'Enter' || e.key === 'Escape')) {
                skipBootSequence();
            }
        });
        let lastTapTime = 0;
        document.addEventListener('touchstart', (e) => {
            if (isBooting) {
                const currentTime = new Date().getTime();
                const tapLength = currentTime - lastTapTime;
                if (tapLength < 500 && tapLength > 0) {
                    skipBootSequence();
                    // Don't prevent default here as it might break normal scrolling/clicks if we aren't careful, but since it's booting it's fine.
                }
                lastTapTime = currentTime;
            }
        });


        function type() {
            if (!isBooting) return;
            if (commandIndex >= commands.length) return;
            const current = commands[commandIndex];
            const text = current.cmd;
            if (charIndex < text.length) {
                playTypingSound();
                if (current.isCommand) commandInputEl.innerHTML += text.charAt(charIndex);
                else {
                    let line = outputEl.lastElementChild;
                    if (!line || (charIndex === 0 && !current.append)) {
                        line = document.createElement('div');
                        if (current.prompt) line.classList.add('prompt');
                        if (current.color) line.classList.add(current.color);
                        outputEl.appendChild(line);
                    }
                    line.innerHTML += text.charAt(charIndex);
                }
                charIndex++;
                
                // Update boot progress bar
                const progressContainer = document.getElementById('boot-progress-container');
                const progressBar = document.getElementById('boot-progress-bar');
                const progressText = document.getElementById('boot-progress-text');
                if (progressContainer && progressBar && progressText) {
                    const totalChars = commands.reduce((acc, cmd) => acc + cmd.cmd.length, 0);
                    let charsTypedSoFar = 0;
                    for (let i = 0; i < commandIndex; i++) charsTypedSoFar += commands[i].cmd.length;
                    charsTypedSoFar += charIndex;
                    
                    const percent = Math.min(100, Math.floor((charsTypedSoFar / totalChars) * 100));
                    progressBar.style.width = percent + '%';
                    progressText.textContent = percent + '%';
                }
                
                bootSequenceTimeout = setTimeout(type, 2 + Math.random() * 3);
            } else {
                if (current.isCommand) {
                    const newLine = document.createElement('div');
                    newLine.classList.add('prompt');
                    newLine.innerHTML = commandInputEl.innerHTML;
                    outputEl.appendChild(newLine);
                    commandInputEl.innerHTML = '';
                    executeCommand(current.cmd);
                }
                commandIndex++;
                charIndex = 0;
                bootSequenceTimeout = setTimeout(type, current.delay);
            }
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        function executeCommand(command) {
            const outputLine = document.createElement('div');
            outputLine.classList.add('text-gray-400', 'my-2');
            
            const cmdLower = command.trim().toLowerCase();
            
            if (cmdLower === './start-portfolio.sh') {
                outputLine.innerHTML = 'Initializing portfolio interface... Success.';
                outputEl.appendChild(outputLine);
                isBooting = false; const hint = document.getElementById('skip-hint'); if(hint) hint.style.opacity = '0';
                const progressContainer = document.getElementById('boot-progress-container');
                if (progressContainer) progressContainer.style.opacity = '0';
                setTimeout(() => {
                    const bootOverlay = document.getElementById('boot-overlay');
                    if (bootOverlay) {
                        bootOverlay.classList.add('opacity-0');
                        setTimeout(() => bootOverlay.style.display = 'none', 1000);
                    }
                    
                    const mainContent = document.getElementById('layout-wrapper');
                    if (mainContent) {
                        mainContent.classList.remove('hidden');
                        setTimeout(() => mainContent.classList.add('opacity-100'), 50);
                    }
                    
                    // Don't call populateNav() because we hand-coded the desktop nav
                    // populateNav();
                    // initializeScrollspy(); // using lenis.on('scroll') now
                    buildTextMinimap(); populateMobileNav(); initializeAllAnimations();
            const mobileNavbar = document.getElementById('mobile-navbar');
            if (mobileNavbar) {
                mobileNavbar.classList.remove('-translate-y-full');
            }

                    
        enableInteractiveTerminal();

                }, 500);
            } else if (cmdLower === 'help') {
                outputLine.innerHTML = `Available commands:<br/>
                <span class="text-green-400">help</span> - Show this message<br/>
                <span class="text-green-400">whoami</span> - Display current user info<br/>
                <span class="text-green-400">clear</span> - Clear the terminal output<br/>
                <span class="text-green-400">contact</span> - Show contact details<br/>
                <span class="text-green-400">cat resume.txt</span> - View quick resume summary`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'whoami') {
                outputLine.innerHTML = `guest_user@irfan-network<br/>Access Level: Visitor`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'clear') {
                outputEl.innerHTML = '';
            } else if (cmdLower === 'contact') {
                outputLine.innerHTML = `Email: <a href="mailto:irfu026@gmail.com" class="text-gray-100 hover:underline">irfu026@gmail.com</a><br/>
                LinkedIn: <a href="https://linkedin.com/in/irfanahmadblr" target="_blank" class="text-gray-100 hover:underline">irfanahmadblr</a><br/>
                GitHub: <a href="https://github.com/i3f4n" target="_blank" class="text-gray-100 hover:underline">i3f4n</a>`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === 'cat resume.txt') {
                outputLine.innerHTML = `Irfan Ahmad - Cybersecurity Professional<br/>
                Specialization: Network Infrastructure & System Deployment<br/>
                Experience: Sonet Integrated Solutions, CtrlWeb, E&P International<br/>
                Focus: Secure, scalable, and resilient IT environments.`;
                outputEl.appendChild(outputLine);
            } else if (cmdLower === '') {
                // Do nothing on empty command
            } else {
                 outputLine.innerHTML = `command not found: ${command}. Type 'help' for available commands.`;
                 outputEl.appendChild(outputLine);
            }
            
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }

        
        // Extract toggle logic to root so it binds immediately
        document.addEventListener('DOMContentLoaded', () => {
            const toggleBtn = document.getElementById('terminal-toggle-btn');
            const terminalWindow = document.getElementById('floating-terminal-window');
            const closeBtn = document.getElementById('close-terminal-btn');
            const header = document.getElementById('floating-terminal-header');
            const inputField = document.getElementById('mini-input');
            
            if (toggleBtn && terminalWindow) {
                function toggleTerminal() {
                    terminalWindow.classList.toggle('hidden');
                    if (!terminalWindow.classList.contains('hidden') && inputField) {
                        setTimeout(() => inputField.focus(), 100);
                    }
                }
                
                toggleBtn.addEventListener('click', toggleTerminal);
                closeBtn.addEventListener('click', toggleTerminal);
                header.addEventListener('click', (e) => {
                    if(e.target !== closeBtn) toggleTerminal();
                });
            }
        });

        function enableInteractiveTerminal() {
            // Bind to the floating terminal execution logic
            outputEl = document.getElementById('mini-output');
            terminalBody = document.getElementById('interactive-terminal');
            
            const inputField = document.getElementById('mini-input');
            
            if(!inputField) return;
            
            // Ensure we don't bind multiple times if called again
            if (!inputField.dataset.bound) {
                inputField.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        const val = this.value;
                        if (val.trim() === '') return;
                        
                        const newLine = document.createElement('div');
                        newLine.classList.add('prompt');
                        newLine.innerHTML = val;
                        outputEl.appendChild(newLine);
                        
                        this.value = '';
                        executeCommand(val);
                    }
                });
                
                // Keep focus when clicking inside terminal body
                terminalBody.addEventListener('click', () => {
                    inputField.focus();
                });
                
                inputField.dataset.bound = "true";
            }
        }
        // --- Text Scramble / Decryption Effect ---
        class TextScramble {
            constructor(el) { this.el = el; this.chars = '!<>-_\\/[]{}—=+*^?#________'; this.update = this.update.bind(this); }
            setText(newText) {
                const oldText = this.el.innerText; const length = Math.max(oldText.length, newText.length);
                const promise = new Promise((resolve) => this.resolve = resolve); this.queue = [];
                for (let i = 0; i < length; i++) { const from = oldText[i] || ''; const to = newText[i] || ''; const start = Math.floor(Math.random() * 40); const end = start + Math.floor(Math.random() * 40); this.queue.push({ from, to, start, end }); }
                cancelAnimationFrame(this.frameRequest); this.frame = 0; this.update(); return promise;
            }
            update() {
                let output = ''; let complete = 0;
                for (let i = 0, n = this.queue.length; i < n; i++) {
                    let { from, to, start, end, char } = this.queue[i];
                    if (this.frame >= end) { complete++; output += to; } 
                    else if (this.frame >= start) { if (!char || Math.random() < 0.28) { char = this.randomChar(); this.queue[i].char = char; } output += `<span class="text-green-500/50">${char}</span>`; } 
                    else { output += from; }
                }
                this.el.innerHTML = output;
                if (complete === this.queue.length) { this.resolve(); } 
                else { this.frameRequest = requestAnimationFrame(this.update); this.frame++; }
            }
            randomChar() { return this.chars[Math.floor(Math.random() * this.chars.length)]; }
        }

        // --- Scroll Reveal & Animation Triggers ---
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    const scrambleEl = entry.target.querySelector('[data-scramble-text]');
                    if (scrambleEl) { const fx = new TextScramble(scrambleEl); fx.setText(scrambleEl.innerText); }
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

                function initializeAllAnimations() {
            const revealElements = document.querySelectorAll('.reveal');
            revealElements.forEach(el => { 
                revealObserver.observe(el);
                // Failsafe: if observer fails to trigger, force visibility after 1s
                setTimeout(() => {
                    if (!el.classList.contains('visible')) {
                        el.classList.add('visible');
                    }
                }, 1000);
            });
        }
        
        // --- Parallax Effect for Certificates ---
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
        }
        
        // --- Data ---
        const certificatesData = [
            // Professional Certificates
            { title: 'Microsoft Cybersecurity Analyst', issuer: 'Microsoft', verifyLink: 'https://coursera.org/verify/professional-cert/7ZVSBE5RAWZ4', imageUrl: 'certificates/MicrosoftCyberSecurityAnalyst.png' },
            { title: 'Google IT Support', issuer: 'Google', verifyLink: 'https://coursera.org/verify/professional-cert/P7J3MD7TD7W8', imageUrl: 'certificates/GoogleITSupport.png' },
            { title: 'Google Project Management', issuer: 'Google', verifyLink: 'https://coursera.org/verify/professional-cert/Y9ZX1ACE2I80', imageUrl: 'certificates/GoogleProjectManagement.png' },
            { title: 'Google UX Design', issuer: 'Google', verifyLink: 'https://coursera.org/verify/professional-cert/CD6IMJEE8JYL', imageUrl: 'certificates/CourseraGoogleUX.png' },
            { title: 'Google IT Automation with Python', issuer: 'Google', verifyLink: 'https://coursera.org/verify/professional-cert/4W0FSRU8PF96', imageUrl: 'certificates/GoogleITAutomationPython.png' },

            // Business & Management
            { title: 'Strategic Management', issuer: 'Copenhagen Business School', verifyLink: 'https://coursera.org/verify/EHYFQ5ZJMM93', imageUrl: 'https://damha.space/certificates/CourseraStrategicManagement.png' },
            { title: 'Protecting Business Innovations via Copyright', issuer: 'HKUST', verifyLink: 'https://coursera.org/verify/9P51UP306ZOV', imageUrl: 'https://damha.space/certificates/CourseraBusinessCopyright.png' },

            // Cybersecurity & Networking
            { title: 'CCNA: Introduction to Networks', issuer: 'Cisco Netacad', verifyLink: 'https://www.credly.com/badges/b2421ee7-7e7b-43ed-96e1-f6a35bd25bf3', imageUrl: 'https://damha.space/certificates/CCNAIntrotoNetworks.png' },
            { title: 'Cybersecurity Essentials', issuer: 'Cisco', imageUrl: 'https://damha.space/certificates/CiscoCyberSecEssentials.png' },
            { title: 'Cyber Threat Hunting', issuer: 'Infosec', verifyLink: 'https://coursera.org/verify/3WWCXD8VPSUZ', imageUrl: 'https://damha.space/certificates/CourseraCyberThreatHunting.png' },
            { title: 'Threat Investigation', issuer: 'Cisco', verifyLink: 'https://coursera.org/verify/GZ1ND2FRVB04', imageUrl: 'https://damha.space/certificates/CourseraThreatInvestigation.png' },
            { title: 'Usable Security', issuer: 'University of Maryland', verifyLink: 'https://coursera.org/verify/0M5ENHBEVJP4', imageUrl: 'https://damha.space/certificates/CourseraUsableSecurity.png' },
            { title: 'Introduction to Cybersecurity', issuer: 'Cisco Netacad', imageUrl: 'https://damha.space/certificates/NetacadIntroToCybersec.png' },
            { title: 'Networking Support & Security', issuer: 'Cisco', imageUrl: 'https://damha.space/certificates/CiscoNetworkSupportSecurity.png' },
            
            // Tech & Development
            { title: 'PCAP: Programming Essentials in Python', issuer: 'Cisco', imageUrl: 'https://damha.space/certificates/CiscoPCAPPython.png' },
            { title: 'NDG Linux Unhatched', issuer: 'Cisco', imageUrl: 'https://damha.space/certificates/CiscoLinux.png' },
            { title: 'Data Mining', issuer: 'Infosys Springboard', imageUrl: 'https://damha.space/certificates/springboardDataMining.png' },
            { title: 'Introduction to Data Warehouse Testing', issuer: 'Infosys Springboard', imageUrl: 'https://damha.space/certificates/springboardDataWarehouseTesting.png' },
            { title: 'Computational Theory', issuer: 'Infosys Springboard', imageUrl: 'https://damha.space/certificates/SpringboardFiniteAutomata.png' },
            { title: 'Big Data Tools and Components', issuer: 'Simplilearn', imageUrl: 'https://damha.space/certificates/SimpliLearnBigDataTools.png' },

            // Additional Coursework
            { title: 'Sustainable Food Systems', issuer: 'University of Illinois', verifyLink: 'https://coursera.org/verify/Y8O3JQBAP9XD', imageUrl: 'https://damha.space/certificates/CourseraCulinaryArts.png' },
            { title: 'Fashion as Design', issuer: 'The Museum of Modern Art', verifyLink: 'https://coursera.org/verify/FFNIQDPLUOZ9', imageUrl: 'https://damha.space/certificates/CourseraFashionDesign.png' },
            { title: 'Sit Less, Get Active', issuer: 'The University of Edinburgh', verifyLink: 'https://coursera.org/verify/BVNUROTBBEKT', imageUrl: 'https://damha.space/certificates/CourseraPhysicalFitness.png' },
            { title: 'Sustainable Tourism', issuer: 'University of Copenhagen', verifyLink: 'https://coursera.org/verify/RE3IZNHZX6U7', imageUrl: 'https://damha.space/certificates/CourseraSustainableTourism.png' }
        ];

        const skillsData = {
            'AI & Prompt Engineering': { title: 'AI & Prompt Engineering', description: 'Extensive experience leveraging LLMs (ChatGPT, Claude, Gemini) and AI coding assistants for rapid development, architecture planning, and debugging. Proficient in prompt engineering to automate workflows and optimize code generation.' },
            'AI-Assisted Development': { title: 'AI-Assisted Development', description: 'Utilizing AI tools to accelerate the software development lifecycle, from generating boilerplate code and writing unit tests to exploring complex algorithmic solutions and diagnosing network security issues.' },
            'Operating Systems': { title: 'Operating Systems', description: 'Experienced in the installation and configuration of several different operating systems across different platforms, and familiar with the file systems of both windows and linux.'},
            'Security & Pentesting': { title: 'Security & Pentesting', description: 'Proficient in threat analysis and mitigation with tools like Microsoft Certified Cybersecurity Analyst suite and Wazuh IDS. Hands-on experience from PortSwigger Web Security Core Labs (SQLi, XSS, CSRF), DDoS Mitigation, and implementing Role-Based Access Control (RBAC) and IdAM.'},
            'Networking & Infrastructure': { title: 'Networking & Infrastructure', description: 'Cisco CCNA certified with strong skills in Linux System Administration, TCP/IP, VLAN, DHCP, DNS, and VPN Setup & Troubleshooting. Experienced in server setup and security hardening.'},
            'DevOps & Automation': { title: 'DevOps & Automation', description: 'Skilled in using Docker for containerization, building and managing CI/CD Pipelines, and creating complex workflows with n8n. Proficient in Bash Scripting, and Sendmail/Mail Server Configuration.'},
            'Programming & Frameworks': { title: 'Programming & Frameworks', description: 'Fluent in Python, JavaScript, PHP, and C++. Experience with backend frameworks including CodeIgniter and Laravel, and front-end libraries like React.'},
            'Web & CMS': { title: 'Web & CMS Development', description: 'Expertise in WordPress, including Advanced Custom Fields (ACF) and WooCommerce for e-commerce. Proficient with Wix Studio and capable of custom plugin development to extend functionality.'},
            'Server Management': { title: 'Server Management', description: 'Expertise in setting up, configuring, and maintaining web servers (like Apache/Nginx), including VPS management, domain configuration, DNS, and ensuring high availability and performance.' },
            'Full-Stack Dev': { title: 'Full-Stack Development', description: 'Proficient in both front-end (HTML, CSS, JavaScript) and back-end (PHP, Laravel, databases) development, enabling the creation of complete, end-to-end web applications.' },
            'Git/VCS': { title: 'Git / Version Control', description: 'Adept at using Git for version control, including branching, merging, and collaborating with teams on complex codebases. Essential for maintaining code integrity and managing project history.' },
            'PHP/JS': { title: 'PHP & JavaScript', description: 'Strong command of PHP for server-side logic and JavaScript for creating dynamic and interactive front-end experiences. The core languages for much of my web development work.' },
            'WordPress': { title: 'WordPress Development', description: 'Skilled in developing and customizing WordPress sites, including theme and plugin development, site optimization, and management for clients.' },
            'WooCommerce': { title: 'WooCommerce', description: 'Experienced in building and managing e-commerce stores using WooCommerce, including product setup, payment gateway integration, and custom checkout flows.' },
            'eCommerce': { title: 'eCommerce Solutions', description: 'Broad experience with various e-commerce platforms like Bagisto and Wix, focusing on creating seamless online shopping experiences and custom sales funnels.' },
            'POS Systems': { title: 'Point-of-Sale (POS) Systems', description: 'Experience in developing and customizing POS software for retail and restaurants, including features like multi-outlet support, inventory management, and receipt/KOT printing.' },
            'Automation (n8n)': { title: 'Automation (n8n)', description: 'Using tools like n8n to create automated workflows that connect different apps and services, improving efficiency and reducing manual work for businesses.' },
            'Docker': { title: 'Docker', description: 'Utilizing Docker to containerize applications, ensuring consistent development and deployment environments, and simplifying the process of scaling applications.' },
            'Laravel': { title: 'Laravel', description: 'Proficient in the Laravel PHP framework for building robust, scalable, and maintainable web applications with an elegant and expressive syntax.' },
            'Android Dev': { title: 'Android Development', description: 'Basic experience in native Android app development using Java/Kotlin, with a focus on creating functional and user-friendly mobile applications.' },
            'Technical Support': { title: 'Technical Support', description: 'Proficient in diagnosing and resolving a wide range of hardware and software issues for users. Skilled in providing clear, friendly, and effective technical assistance to ensure smooth and reliable system operation.' },
            'PC Building': { title: 'PC Building', description: 'Experienced in custom PC building, from component selection and compatibility checking to assembly and performance tuning. Passionate about creating high-performance machines tailored for specific needs like gaming or development.' },
            'Polyglot / Languages': { title: 'Polyglot / Languages', description: 'Fluent in over 8 languages. Completely fluent in English, Hindi, Malayalam, Kannada, Urdu, Tamil, and Jeseri. Able to speak and understand Japanese, possess basic conversational Arabic, and currently holding a B2 level in French.' },
        };

        const interestsData = {
            'Esports': { title: 'Esports', description: 'A passionate and skilled competitive gamer, excelling in high-stakes games like Valorant, Rocket League, and Apex Legends that require sharp reflexes, strategic thinking, and effective teamwork.' },
            'Gym & Powerlifting': { title: 'Gym & Powerlifting', description: 'Dedicated to fitness and strength training, with a focus on powerlifting. This hobby instills discipline, resilience, and a mindset of continuous improvement by pushing physical limits.' },
            'Sneaker Enthusiast': { title: 'Sneaker Enthusiast', description: 'An avid collector of sneakers, appreciating the design, culture, and stories behind iconic and rare footwear. It\'s a hobby that blends style with history.' },
            'Perfume Collecting': { title: 'Perfume Collecting', description: 'Fascinated by the art of fragrance, I enjoy collecting and learning about different perfumes. This hobby involves understanding complex notes, composition, and the craft of perfumery.' },
            'PC Building': { title: 'PC Building', description: 'I enjoy the hands-on process of building custom PCs from scratch. It\'s a hobby that combines my love for high-performance hardware, problem-solving, and creating something powerful and unique.' },
            'Football': { title: 'Football', description: 'A passionate football player and fan, enjoying both the physical demands and the strategic elements of the sport.' },
            'Puzzle Solving': { title: 'Puzzle Solving', description: 'A dedicated puzzle solver with a particular interest in all types of Rubik\'s cubes. I enjoy the mental challenge and pattern recognition required to solve complex puzzles quickly.' },
            'Travelling': { title: 'Travelling', description: 'I love exploring the ocean and mountains. I have travelled extensively throughout India, spending months at a time in places like Lakshadweep.' },
            'Scuba Diving': { title: 'Scuba Diving', description: 'Passionate about exploring the underwater world. My travels to Lakshadweep and other coastal regions have fueled my love for scuba diving and marine environments.' },
        };

        const projects = [
            { title: "Enterprise Security Infrastructure (Sonet)", url: "#", role: "Network Infrastructure Consultant", description: "Engineered a highly resilient Hub-and-Spoke enterprise network for Titan Company Ltd. Directed end-to-end Layer 1 to Layer 3 deployment, including precision fiber-optic (OFC) splicing, secure server room architecture, and a 152-node IP CCTV network. Implemented strict VLAN segmentation to neutralize internal threats, successfully mitigating a severe Layer 2 broadcast storm.", tech: ["Cisco", "OFC", "IP CCTV", "VLANs", "STP"] },
            { title: "Custom Enterprise Invoicing Software", url: "#", role: "Implementation & Deployment Lead", description: "Deployed and customized a scalable, self-hosted invoicing and billing solution for multiple enterprise clients. Integrated automated payment workflows, recurring billing, and branded client portals. This enabled businesses to streamline financial operations and maintain complete data sovereignty while eliminating recurring SaaS overhead.", tech: ["Self-Hosted", "PHP", "MySQL", "Docker", "Billing Automation"] },
            { title: "Self-Hosted Enterprise Automation (CtrlWeb)", url: "#", role: "Founder", description: "The Architecture: Deployed n8n automation servers strictly on hardened, self-hosted Linux environments to maintain data sovereignty for SME clients. The Security: Configured secure, webhook-driven workflows for encrypted cross-platform transactions, ensuring zero external exposure of core business system endpoints.", tech: ["n8n", "Linux", "Webhooks", "Docker"] },
            { title: "Secure Multi-Tenant POS Architecture", url: "#", role: "Full-Stack & Security Engineer", description: "The Problem: High-density commercial campuses require POS systems that can handle concurrent transactions offline while maintaining strict data isolation between vendors. The Architecture: Developed a custom POS ecosystem using PHP/JS and Git. The Security: Implemented strict Role-Based Access Control (RBAC), secure session management, and cross-tenant data isolation.", tech: ["PHP", "JavaScript", "MySQL", "RBAC", "Git"] },
            { title: "Pioneer Ceilings", url: "#", role: "Website Developer & Host Manager", description: "A WordPress site for a ceilings company, utilizing WooCommerce for its product showcase. I handled the complete site setup, theme and plugin configuration, and provide ongoing hosting management.", tech: ["WordPress", "WooCommerce", "Hostinger", "PHP"] },
            { title: "Elephant & Peacock POS", url: "https://eandppos.in", role: "POS Software Developer", description: "A complete, custom-built Point-of-Sale software for a retail client. The system supports multiple outlets, receipt and Kitchen Order Ticket (KOT) printing, and the entire codebase is version-controlled with Git.", tech: ["Custom POS", "PHP", "JavaScript", "Git", "MySQL"] },
            { title: "eandp.in eCommerce", url: "https://eandp.in", role: "eCommerce Developer", description: "Developed and deployed a clothing retail eCommerce website. Managed domain purchasing and hosting, utilizing Wix as the site builder for certain workflows while managing multiple related sites on Hostinger.", tech: ["Wix", "eCommerce", "Hostinger", "Domain Mgmt"] },
            { title: "Bagisto Sales Lead Checkout", url: "#", role: "eCommerce Developer", description: "Customized a Bagisto (Laravel-based) eCommerce platform to bypass the payment gateway. Instead, checkout details are captured and routed directly to the sales team via email and WhatsApp/SMS using a custom 'SalesLeadCheckout' package and Twilio integration.", tech: ["Bagisto", "Laravel", "PHP", "Twilio API"] },
            { title: "NF Solutions Website", url: "#", role: "Frontend & Site Implementer", description: "Designed and deployed a multi-page marketing website for an interior design company in Lucknow. Handled the complete design, content layout, and deployment with a CMS integration.", tech: ["HTML", "CSS", "JavaScript", "CMS"] },
            { title: "Royalwood Furniture eCommerce", url: "https://royalwoodfurniture.com", role: "Full-Stack Developer", description: "Developed a complete eCommerce website for a furniture business from the ground up, featuring a full product catalog, shopping cart, and checkout functionality.", tech: ["WordPress", "WooCommerce", "eCommerce", "PHP"] },
            { title: "OpenSourcePOS Integration", url: "#", role: "POS Integrator", description: "Installed and customized OpenSourcePOS for a restaurant client. The project involved domain setup via GoDaddy, server configuration, and tailoring the POS features to meet specific needs like KOT and receipt formats.", tech: ["OpenSourcePOS", "GoDaddy", "Server Setup", "PHP"] },
            { title: "Self-Hosted ERPNext Setup", url: "#", role: "Systems Engineer", description: "Deployed, configured, and maintain a self-hosted instance of ERPNext on a private server. This involved the complete setup and customization of the open-source ERP for business management.", tech: ["ERPNext", "Linux", "Docker", "Self-Hosting"] }
        ];
        
        // --- Population Functions ---
        const skillsGrid = document.getElementById('skills-grid');
        const interestsGrid = document.getElementById('interests-grid');
        const projectGrid = document.getElementById('project-grid');
        const certificateGrid = document.getElementById('certificate-grid');
        const certificatesContainer = document.getElementById('certificates-container');


        // --- Side Navigation & Scrollspy ---
        function populateNav() {
            const sideNavList = document.querySelector('#side-nav ul');
            if (!sideNavList) return; // Guard clause
            const sections = document.querySelectorAll('main > section');
            sections.forEach(section => {
                const sectionId = section.id;
                const sectionTitle = section.querySelector('h2').getAttribute('data-text');
                const li = document.createElement('li');
                li.innerHTML = `<a href="#${sectionId}" class="nav-link">${sectionTitle}</a>`;
                sideNavList.appendChild(li);
            });
        }
        
        function initializeScrollspy() {
            const navLinks = document.querySelectorAll('.nav-link');
            const sections = document.querySelectorAll('main > section');

            if (navLinks.length === 0) return; // Guard clause

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        navLinks.forEach(link => {
                            link.classList.remove('active');
                            if (link.getAttribute('href') === `#${id}`) {
                                link.classList.add('active');
                            }
                        });
                    }
                });
            }, { rootMargin: '-50% 0px -50% 0px' });

            sections.forEach(section => {
                observer.observe(section);
            });

            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href');
                    lenis.scrollTo(targetId, { offset: -50 });
                });
            });
        }
            
        

        
        
        // --- Mobile Navbar Logic ---
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileNavList = document.getElementById('mobile-nav-list');

        if (mobileMenuBtn && mobileMenu && mobileNavList) {
            mobileMenuBtn.addEventListener('click', () => {
                const isHidden = mobileMenu.classList.contains('hidden');
                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    mobileMenu.classList.add('flex');
                    // Force reflow
                    void mobileMenu.offsetWidth;
                    mobileMenu.classList.remove('opacity-0');
                    mobileMenu.classList.add('opacity-100');
                    // Add staggered cascade class
                    setTimeout(() => mobileNavList.classList.add('mobile-menu-active'), 50);
                    // Animate hamburger to X
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
                    // Populate if empty
                    if (mobileNavList.children.length === 0) {
                        populateMobileNav();
                    }
                } else {
                    mobileNavList.classList.remove('mobile-menu-active');
                    mobileMenu.classList.remove('opacity-100');
                    mobileMenu.classList.add('opacity-0');
                    // Animate X back to hamburger
                    mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    setTimeout(() => {
                        mobileMenu.classList.add('hidden');
                        mobileMenu.classList.remove('flex');
                    }, 300);
                }
            });
        }

        function populateSkills() {
            skillsGrid.innerHTML = '';
            const skillColors = [
                'border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10 hover:border-cyan-500/60 hover:shadow-[0_0_15px_rgba(6,182,212,0.2)]',
                'border-green-500/30 text-green-400 hover:bg-green-500/10 hover:border-green-500/60 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]',
                'border-purple-500/30 text-purple-400 hover:bg-purple-500/10 hover:border-purple-500/60 hover:shadow-[0_0_15px_rgba(168,85,247,0.2)]',
                'border-blue-500/30 text-blue-400 hover:bg-blue-500/10 hover:border-blue-500/60 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)]',
                'border-pink-500/30 text-pink-400 hover:bg-pink-500/10 hover:border-pink-500/60 hover:shadow-[0_0_15px_rgba(236,72,153,0.2)]',
                'border-orange-500/30 text-orange-400 hover:bg-orange-500/10 hover:border-orange-500/60 hover:shadow-[0_0_15px_rgba(249,115,22,0.2)]',
                'border-teal-500/30 text-teal-400 hover:bg-teal-500/10 hover:border-teal-500/60 hover:shadow-[0_0_15px_rgba(20,184,166,0.2)]'
            ];
            Object.keys(skillsData).forEach((skill, index) => {
                const tag = document.createElement('span');
                const colorClass = skillColors[index % skillColors.length];
                tag.className = `skill-tag bg-[#161b22]/50 border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2`;
                tag.innerHTML = `<span class="opacity-50 text-xs font-mono">[]</span> ${skill}`;
                tag.style.setProperty('--delay', `${0.1 + (index % 12) * 0.05}s`);
                tag.addEventListener('click', () => openDetailModal(skillsData[skill]));
                skillsGrid.appendChild(tag);
                revealObserver.observe(tag);
            });
            const toggleBtn = document.getElementById('toggle-skills-btn');
            if (toggleBtn) toggleBtn.parentElement.style.display = 'none';
        }

        function populateInterests() {
            interestsGrid.innerHTML = '';
            const interestColors = {
                'Esports': 'border-red-500/40 text-red-400 bg-red-900/20 hover:bg-red-500/20 hover:shadow-[0_0_15px_rgba(239,68,68,0.2)]',
                'Gym & Powerlifting': 'border-gray-500/40 text-gray-300 bg-gray-800/40 hover:bg-gray-500/20 hover:shadow-[0_0_15px_rgba(156,163,175,0.2)]',
                'Sneaker Enthusiast': 'border-purple-500/40 text-purple-400 bg-purple-900/20 hover:bg-purple-500/20 hover:shadow-[0_0_15px_rgba(168,85,247,0.2)]',
                'Perfume Collecting': 'border-pink-500/40 text-pink-400 bg-pink-900/20 hover:bg-pink-500/20 hover:shadow-[0_0_15px_rgba(236,72,153,0.2)]',
                'PC Building': 'border-blue-500/40 text-blue-400 bg-blue-900/20 hover:bg-blue-500/20 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)]',
                'Football': 'border-orange-500/40 text-orange-400 bg-orange-900/20 hover:bg-orange-500/20 hover:shadow-[0_0_15px_rgba(249,115,22,0.2)]',
                'Puzzle Solving': 'border-teal-500/40 text-teal-400 bg-teal-900/20 hover:bg-teal-500/20 hover:shadow-[0_0_15px_rgba(20,184,166,0.2)]',
                'Travelling': 'border-indigo-500/40 text-indigo-400 bg-indigo-900/20 hover:bg-indigo-500/20 hover:shadow-[0_0_15px_rgba(99,102,241,0.2)]',
                'Scuba Diving': 'border-cyan-500/40 text-cyan-400 bg-cyan-900/20 hover:bg-cyan-500/20 hover:shadow-[0_0_15px_rgba(6,182,212,0.2)]'
            };
            Object.keys(interestsData).forEach((interest, index) => {
                const tag = document.createElement('span');
                const colorClass = interestColors[interest] || 'border-gray-500/40 text-gray-300 bg-gray-800/40 hover:bg-gray-500/20';
                tag.className = `skill-tag border ${colorClass} py-2 px-4 rounded-full reveal reveal-child clickable-tag transition-all duration-300 flex items-center gap-2`;
                tag.innerHTML = `<span class="opacity-50 text-xs font-mono">[]</span> ${interest}`;
                tag.style.setProperty('--delay', `${0.1 + index * 0.1}s`);
                tag.addEventListener('click', () => openDetailModal(interestsData[interest]));
                interestsGrid.appendChild(tag);
                revealObserver.observe(tag);
            });
        }

        let projectsExpanded = false;
        function populateProjects() {
            projectGrid.innerHTML = '';
            projects.forEach((project, index) => {
                const card = document.createElement('div');
                card.id = 'proj-' + index;
                card.className = 'project-card bg-[#161b22]/70 p-6 rounded-lg reveal reveal-child';
                card.style.transitionDelay = `${(index % 4) * 100}ms`;
                card.innerHTML = `<h3 class="text-xl font-bold text-gray-100 mb-2">${project.title}</h3><p class="text-gray-400 mb-4">${project.description.substring(0, 100)}...</p><div class="flex flex-wrap gap-2">${project.tech.map(t => `<span class="bg-gray-800 text-xs text-gray-400 py-1 px-2 rounded">${t}</span>`).join('')}</div>`;
                card.addEventListener('click', () => openDetailModal(project));
                projectGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            const toggleProjectsBtn = document.getElementById('toggle-projects-btn');
            const fadeEl = document.getElementById('proj-fade');
            const projectsContainer = document.getElementById('projects-container');
            
            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleProjectsBtn) toggleProjectsBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projectsContainer.style.maxHeight = isPC ? '900px' : '850px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show More';
                } else {
                    projectsContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleProjectsBtn) toggleProjectsBtn.textContent = 'Show Less';
                }
            };
            
            updateLayout();
            
            if (toggleProjectsBtn && !toggleProjectsBtn.dataset.bound) {
                toggleProjectsBtn.dataset.bound = "true";
                toggleProjectsBtn.addEventListener('click', () => {
                    projectsExpanded = !projectsExpanded;
                    updateLayout();
                });
            }
        }

        let certsExpanded = false;
        function populateCertificates() {
            certificateGrid.innerHTML = '';
            
            const createCard = (cert) => {
                const card = document.createElement('div');
                card.className = 'certificate-card h-48 md:h-64 bg-[#161b22]/70 rounded-lg flex flex-col justify-end reveal';
                card.innerHTML = `
                    <div class="card-bg" style="background-image: url('${cert.imageUrl}')"></div>
                    <div class="card-content p-4">
                        <h3 class="text-lg font-bold text-gray-100">${cert.title}</h3>
                        <p class="text-sm text-gray-400">${cert.issuer}</p>
                    </div>
                `;
                card.addEventListener('click', () => openDetailModal(cert));
                return card;
            };

            certificatesData.forEach((cert) => {
                const card = createCard(cert);
                certificateGrid.appendChild(card);
                revealObserver.observe(card);
            });
            
            let toggleCertsBtn = document.getElementById('toggle-certs-btn');
            const fadeEl = document.getElementById('cert-fade');
            const certificatesContainer = document.getElementById('certificates-container');
            
            const updateLayout = () => {
                const isPC = window.innerWidth >= 768;
                if(toggleCertsBtn) toggleCertsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certificatesContainer.style.maxHeight = isPC ? '850px' : '640px';
                    if(fadeEl) fadeEl.style.opacity = '1';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show More';
                } else {
                    certificatesContainer.style.maxHeight = '4000px';
                    if(fadeEl) fadeEl.style.opacity = '0';
                    if(toggleCertsBtn) toggleCertsBtn.textContent = 'Show Less';
                }
            };
            
            updateLayout();
            
            if (toggleCertsBtn && !toggleCertsBtn.dataset.bound) {
                toggleCertsBtn.dataset.bound = "true";
                toggleCertsBtn.addEventListener('click', () => {
                    certsExpanded = !certsExpanded;
                    if (!certsExpanded) lenis.scrollTo('#certificates', { offset: -100 });
                    updateLayout();
                });
            }
            
        }

        // Resize listener for responsive layouts
        window.addEventListener('resize', () => {
            const isPC = window.innerWidth >= 768;
            
            // Certificates
            const certsContainer = document.getElementById('certificates-container');
            const certsFade = document.getElementById('cert-fade');
            const certsBtn = document.getElementById('toggle-certs-btn');
            if (certsContainer) {
                if (certsBtn) certsBtn.parentElement.style.display = 'flex';
                if (!certsExpanded) {
                    certsContainer.style.maxHeight = isPC ? '850px' : '640px';
                    if (certsFade) certsFade.style.opacity = '1';
                    if (certsBtn) certsBtn.textContent = 'Show More';
                } else {
                    certsContainer.style.maxHeight = '4000px';
                    if (certsFade) certsFade.style.opacity = '0';
                    if (certsBtn) certsBtn.textContent = 'Show Less';
                }
            }
            
            // Projects
            const projContainer = document.getElementById('projects-container');
            const projFade = document.getElementById('proj-fade');
            const projBtn = document.getElementById('toggle-projects-btn');
            if (projContainer) {
                if (projBtn) projBtn.parentElement.style.display = 'flex';
                if (!projectsExpanded) {
                    projContainer.style.maxHeight = isPC ? '900px' : '850px';
                    if (projFade) projFade.style.opacity = '1';
                    if (projBtn) projBtn.textContent = 'Show More';
                } else {
                    projContainer.style.maxHeight = '4000px';
                    if (projFade) projFade.style.opacity = '0';
                    if (projBtn) projBtn.textContent = 'Show Less';
                }
            }
        });

        // --- Modal Logic ---
        const modal = document.getElementById('detail-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalIssuer = document.getElementById('modal-issuer');
        const modalDescription = document.getElementById('modal-description');
        const modalDetails = document.getElementById('modal-details');
        const modalRole = document.getElementById('modal-role');
        const modalTech = document.getElementById('modal-tech');
        const modalLink = document.getElementById('modal-link');
        const modalCertDetails = document.getElementById('modal-certificate-details');
        const modalCertImage = document.getElementById('modal-cert-image');
        const modalVerifyLink = document.getElementById('modal-verify-link');
        const closeButton = document.querySelector('.close-button');

        function openDetailModal(data) {
            modalTitle.textContent = data.title;
            modalDescription.textContent = data.description || '';
            modalDescription.style.display = data.description ? 'block' : 'none';

            if (data.role) { // Project
                modalIssuer.style.display = 'none';
                modalCertDetails.style.display = 'none';
                modalDetails.style.display = 'block';
                modalRole.textContent = data.role;
                modalTech.innerHTML = data.tech.map(t => `<span class="bg-blue-900/50 text-blue-300 text-sm py-1 px-3 rounded-full">${t}</span>`).join('');
                modalLink.style.display = data.url === "#" ? 'none' : 'inline-block';
                modalLink.href = data.url;
            } else if (data.issuer) { // Certificate
                modalDetails.style.display = 'none';
                modalCertDetails.style.display = 'block';
                modalIssuer.style.display = 'block';
                modalIssuer.textContent = `Issued by: ${data.issuer}`;
                modalCertImage.src = data.imageUrl;
                modalVerifyLink.style.display = data.verifyLink ? 'inline-block' : 'none';
                if(data.verifyLink) modalVerifyLink.href = data.verifyLink;
            } else { // Skill or Interest
                modalIssuer.style.display = 'none';
                modalDetails.style.display = 'none';
                modalCertDetails.style.display = 'none';
            }
            modal.style.display = 'flex';
            setTimeout(() => modal.classList.add('active'), 10);
        }

        function closeModal() {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 500);
        }

        closeButton.onclick = closeModal;
        window.onclick = (event) => { if (event.target == modal) { closeModal(); } }
        
        
        // --- Random Glitch Effects ---
        function triggerRandomGlitches() {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            const glitchTitles = document.querySelectorAll('.glitch-title.visible');
            if (glitchTitles.length > 0) {
                const randomElement = glitchTitles[Math.floor(Math.random() * glitchTitles.length)];
                randomElement.classList.remove('visible');
                void randomElement.offsetWidth; // trigger reflow
                randomElement.classList.add('visible');
            }
            setTimeout(triggerRandomGlitches, 2000 + Math.random() * 5000);
        }
        triggerRandomGlitches();

        // --- Initial Load ---
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize audio on the first user interaction
            const startAudio = async () => {
                await Tone.start();
                audioInitialized = true;
                document.body.removeEventListener('click', startAudio);
            };
            document.body.addEventListener('click', startAudio);
            
            type();
            populateSkills();
            populateInterests();
            populateProjects();
            populateCertificates();
            updateInteractiveElements();
        });


                        // --- Text Minimap & Frame Tracker ---
        let isNavigating = false;
        let navTimeout = null;
        function buildTextMinimap() {
            const navList = document.getElementById('nav-list');
            const navFrame = document.getElementById('nav-frame');
            if (!navList || !navFrame) return;
            
            // Allow DOM to settle
            setTimeout(() => {
                navList.innerHTML = '';
                
                const elements = document.querySelectorAll('#main-content > section');
                
                elements.forEach((el, index) => {
                    const li = document.createElement('li');
                    
                    if (el.tagName.toLowerCase() === 'section') {
                        // Ensure section has an ID
                        const titleEl = el.querySelector('h2');
                        const title = titleEl ? titleEl.innerText.replace('./', '').replace('.sh', '').toUpperCase() : 'SECTION';
                        li.className = 'my-2 first:mt-0';
                        li.innerHTML = `<a href="#${el.id}" class="nav-link block text-base font-bold text-gray-400 hover:text-green-400 tracking-widest px-3 py-2 transition-all duration-300" data-target="${el.id}">${title}</a>`;
                    }
 else {
                        // Project or Experience Card
                        const titleEl = el.querySelector('h3');
                        const title = titleEl ? titleEl.innerText : 'Item';
                        
                        // Ensure element has an ID
                        if (!el.id) el.id = 'minimap-item-' + index;
                        
                        li.className = 'my-0';
                        // Shorten title if too long
                        const shortTitle = title.length > 25 ? title.substring(0, 22) + '...' : title;
                        li.innerHTML = `<a href="#${el.id}" class="nav-link block text-xs text-gray-500 hover:text-gray-300 px-3 py-1 transition-all duration-300 whitespace-nowrap overflow-hidden text-ellipsis" data-target="${el.id}">${shortTitle}</a>`;
                    }
                    
                    navList.appendChild(li);
                });
                
                // Bind Clicks
                document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetId = link.getAttribute('data-target');
                        
                        // Set navigation flag so scroll event doesn't hijack the HUD
                        isNavigating = true;
                        clearTimeout(navTimeout);
                        navTimeout = setTimeout(() => { isNavigating = false; }, 1200); // 1.2s is lenis default duration
                        
                        // Immediately snap the HUD to the target item
                        const li = link.parentElement;
                        navFrame.style.top = li.offsetTop + 'px';
                        navFrame.style.height = li.offsetHeight + 'px';
                        navFrame.style.opacity = '1';
                        
                        document.querySelectorAll('#nav-list .nav-link').forEach(l => {
                            l.classList.remove('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                        });
                        link.classList.add('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                        
                        lenis.scrollTo('#' + targetId, { offset: -50 });
                    });
                });
                
                // Scroll Tracker for the Frame
                lenis.on('scroll', () => {
                    if (isNavigating) return; // Don't update HUD during automated scroll jumps
                    let activeId = '';
                    let activeLinkEl = null;
                    
                    // Update mobile scroll progress bar
                    const progressBar = document.getElementById('mobile-progress-bar');
                    if (progressBar && window.innerWidth < 1024) {
                        const scrollPercent = (window.scrollY / (document.body.offsetHeight - window.innerHeight)) * 100;
                        progressBar.style.width = scrollPercent + '%';
                    }

                    // 1. Check if we are at the absolute bottom of the page
                    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50) {
                        if (elements.length > 0) activeId = elements[elements.length - 1].id;
                    } else {
                        // 2. Otherwise find the lowest element that is in the upper half of the screen
                        for (let i = elements.length - 1; i >= 0; i--) {
                            const el = elements[i];
                            const rect = el.getBoundingClientRect();
                            if (rect.top <= window.innerHeight * 0.5) {
                                activeId = el.id;
                                break;
                            }
                        }
                    }
                    
                    // Fallback to first element if at very top
                    if (!activeId && elements.length > 0 && window.scrollY < 100) {
                        activeId = elements[0].id;
                    }
                    
                    if (activeId) {
                        activeLinkEl = document.querySelector(`#nav-list .nav-link[data-target="${activeId}"]`);
                        
                        if (activeLinkEl) {
                            navFrame.style.opacity = '1';
                            
                            // Get exactly where the active <li> is in the scrollable nav list
                            const li = activeLinkEl.parentElement;
                            const top = li.offsetTop;
                            const height = li.offsetHeight;
                            
                            // Size the frame perfectly around the li
                            navFrame.style.top = top + 'px';
                            navFrame.style.height = height + 'px';
                            
                            // Visual pop for active item
                            document.querySelectorAll('#nav-list .nav-link').forEach(link => {
                                link.classList.remove('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');
                            });
                            activeLinkEl.classList.add('text-green-400', 'translate-x-2', 'drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]');

                            // Update mobile section indicator
                            const indicator = document.getElementById('mobile-section-indicator');
                            if (indicator) {
                                const sectionName = activeLinkEl.textContent.trim();
                                indicator.textContent = '/ ' + sectionName.toLowerCase();
                                indicator.classList.remove('hidden');
                                const cursor = document.getElementById('mobile-cursor');
                                if (cursor) cursor.classList.remove('hidden');
                            }
                        }
                    } else {
                        navFrame.style.opacity = '0';
                    }
                });
                
            }, 1000);
        }



        function populateMobileNav() {
            const mobileNavList = document.getElementById('mobile-nav-list');
            if (!mobileNavList) return;
            mobileNavList.innerHTML = '';
            const sections = document.querySelectorAll('main > section');
            
            sections.forEach((section, index) => {
                const sectionId = section.id;
                const h2 = section.querySelector('h2');
                if(!h2) return;
                const sectionTitle = h2.getAttribute('data-text');
                const li = document.createElement('li');
                li.className = 'mobile-nav-item';
                li.style.transitionDelay = `${index * 0.08}s`;
                li.innerHTML = `<a href="#${sectionId}" class="mobile-nav-link block py-4 text-3xl font-bold tracking-[0.1em] text-center uppercase hover:text-green-400 transition-colors" data-target="${sectionId}">
                                    <span class="mr-3 opacity-30 text-xl font-mono block mb-1">0${index + 1}.</span>${sectionTitle.replace('./', '').replace('.sh', '')}
                                </a>`;
                
                // Add click listener so links actually close the menu on mobile!
                li.addEventListener('click', (e) => {
                    e.preventDefault();
                    lenis.scrollTo(`#${sectionId}`, { offset: -80 });
                    
                    const mobileMenu = document.getElementById('mobile-menu');
                    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                    const mobileNavList = document.getElementById('mobile-nav-list');
                    
                    if (mobileNavList) mobileNavList.classList.remove('mobile-menu-active');
                    if (mobileMenu) {
                        mobileMenu.classList.remove('opacity-100');
                        mobileMenu.classList.add('opacity-0');
                    }
                    if (mobileMenuBtn) {
                        mobileMenuBtn.innerHTML = '<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>';
                    }
                    setTimeout(() => {
                        if (mobileMenu) {
                            mobileMenu.classList.add('hidden');
                            mobileMenu.classList.remove('flex');
                        }
                    }, 300);
                });
                
                mobileNavList.appendChild(li);
            });
        }
