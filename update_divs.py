with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == '---':
        new_lines.append('<img src="assets/animated_line.svg" width="100%">\n')
    elif '212284100-561aa473-3905-4a80-b561-0d28506553ee.gif' in line:
        new_lines.append(line.replace('https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif', 'assets/assassins_reversed.gif'))
    else:
        new_lines.append(line)

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
