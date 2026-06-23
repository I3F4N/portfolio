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

js_old1 = """            if (toggleProjectsBtn) {
                // Remove old event listener if re-populating
                const newBtn = toggleProjectsBtn.cloneNode(true);
                toggleProjectsBtn.parentNode.replaceChild(newBtn, toggleProjectsBtn);
                newBtn.addEventListener('click', () => {
                    projectsExpanded = !projectsExpanded;
                    updateLayout();
                });
                updateLayout();
            }"""

js_new1 = """            updateLayout();
            
            if (toggleProjectsBtn && !toggleProjectsBtn.dataset.bound) {
                toggleProjectsBtn.dataset.bound = "true";
                toggleProjectsBtn.addEventListener('click', () => {
                    projectsExpanded = !projectsExpanded;
                    updateLayout();
                });
            }"""

js_old2 = """        function populateCertificates() {
            certificateGrid.innerHTML = '';
            
            const createCard = (cert) => {"""

js_new2 = """        function populateCertificates() {
            const certificateGrid = document.getElementById('certificate-grid');
            if(certificateGrid) certificateGrid.innerHTML = '';
            
            const createCard = (cert) => {"""

# And wait, does certificateGrid throw if it's undefined?
# At the top of script.js, certificateGrid is defined globally.
# I just need to make sure the replacement works. Let's do it carefully.

update_file('script.js', [
    (js_old1, js_new1)
])

print("Fixed updateLayout issue.")
