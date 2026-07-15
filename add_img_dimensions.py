import os
import re

def process_html_files(base_dir):
    img_pattern = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)
    
    # Dictionary for aspect ratios
    aspect_ratios = {
        'logo': ('40', '40'),
        'person': ('600', '400'),
        'farmer': ('600', '400'),
        'shop': ('800', '600'),
        'bottle': ('300', '400'),
        'bag': ('300', '400'),
        'soil': ('400', '300'),
        'category': ('400', '300'),
        'pro': ('1920', '600') # Hero banner
    }
    
    updated_files = 0
    
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or 'node_modules' in root or '.git' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                def repl_img(match):
                    attrs = match.group(1)
                    # If width or height already exists, skip
                    if 'width=' in attrs.lower() or 'height=' in attrs.lower():
                        return match.group(0)
                        
                    # Determine width and height
                    w, h = '800', '600' # default 4:3
                    lower_attrs = attrs.lower()
                    
                    if 'logo' in lower_attrs:
                        w, h = '40', '40'
                    elif 'person' in lower_attrs or 'farmer' in lower_attrs:
                        w, h = '600', '400'
                    elif 'shop' in lower_attrs:
                        w, h = '800', '600'
                    elif 'bottle' in lower_attrs or 'bag' in lower_attrs:
                        w, h = '300', '400'
                    elif 'hero-banner' in lower_attrs or 'pro.webp' in lower_attrs:
                        w, h = '1920', '600'
                        
                    return f'<img {attrs} width="{w}" height="{h}">'

                new_content = img_pattern.sub(repl_img, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated images in {file_path}")
                    updated_files += 1
                    
    print(f"Total HTML files updated for images: {updated_files}")

if __name__ == '__main__':
    process_html_files(r'c:\Users\ASUS\Downloads\SRA')
