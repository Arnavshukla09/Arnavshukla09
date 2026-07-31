import os

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('assets/animated_line.svg', 'assets/custom_divider.png')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)
