import os
import glob

# The working directory will be backend/
files = glob.glob('**/*.py', recursive=True)
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'from app' in content:
        new_content = content.replace('from app', 'from app')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file}")
