import os
import re

def fix_accessibility(base_dir):
    updated_files = 0
    
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or 'node_modules' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 1. Add <main> tag if not present and if there's a <body> tag
                if '<main>' not in content and '<main id="main-content">' not in content:
                    # Find the header or first section
                    if '</header>' in content:
                        content = content.replace('</header>', '</header>\n<main id="main-content">', 1)
                        if '<footer>' in content:
                            content = content.replace('<footer>', '</main>\n<footer>', 1)
                        elif '</body>' in content:
                            content = content.replace('</body>', '</main>\n</body>', 1)
                    elif '<nav ' in content or '<nav>' in content:
                        # Find end of nav
                        nav_end_idx = content.find('</nav>')
                        if nav_end_idx != -1:
                            content = content[:nav_end_idx+6] + '\n<main id="main-content">' + content[nav_end_idx+6:]
                            if '<footer>' in content:
                                content = content.replace('<footer>', '</main>\n<footer>', 1)
                            elif '</body>' in content:
                                content = content.replace('</body>', '</main>\n</body>', 1)
                
                # 2. Add aria-labels to "Explore More" or identical links
                content = re.sub(r'(<a\s+[^>]*href="([^"]+)"[^>]*)>\s*Explore More', r'\1 aria-label="Explore more about \2">\nExplore More', content, flags=re.IGNORECASE)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated accessibility in {file_path}")
                    updated_files += 1

    print(f"Total HTML files updated for a11y: {updated_files}")

if __name__ == '__main__':
    fix_accessibility(r'c:\Users\ASUS\Downloads\SRA')
