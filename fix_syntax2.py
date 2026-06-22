import re

with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's cleanly remove lines 773 to 784 (which are indices 772 to 783)
# Actually, since line numbers might shift slightly, let's find the exact block and delete it.
js = "".join(lines)

orphan_block = """
                    } else {
                        visibleCerts += 6;
                        if (visibleCerts >= certificatesData.length) {
                            toggleCertsBtn.textContent = 'Show Less';
                        } else {
                            toggleCertsBtn.textContent = 'Show More Certificates';
                        }
                    }
                    populateCertificates();
                });
            }
        }
"""
js = js.replace(orphan_block, "")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Removed orphaned syntax block.")
