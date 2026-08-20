import os

directory = 'c:/Users/atila/OneDrive/Masaüstü/ev-sporu-app'

replacements = {
    'Evde Spor': 'Evde Sporr',
    'evdespor': 'evdesporr',
    'EVDE SPOR': 'EVDE SPORR',
    'text-accent\">SPOR<': 'text-accent\">SPORR<'
}

for root, dirs, files in os.walk(directory):
    if 'venv' in root or '.git' in root or '__pycache__' in root or 'instance' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.py')):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
                
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {filepath}')
