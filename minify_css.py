import re
import os

def minify_css(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    
    # Remove space around delimiters
    css = re.sub(r'\s*([\{\}\:\;\,\>\+\~])\s*', r'\1', css)
    
    # Remove last semicolon in block
    css = re.sub(r';\}', '}', css)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(css.strip())

    print(f"Minified {file_path}")

if __name__ == '__main__':
    styles_path = r'c:\Users\ASUS\Downloads\SRA\static\styles.css'
    staticfiles_path = r'c:\Users\ASUS\Downloads\SRA\staticfiles\styles.css'
    
    if os.path.exists(styles_path):
        minify_css(styles_path)
    
    if os.path.exists(staticfiles_path):
        minify_css(staticfiles_path)
