import os

# 1. Create a better animated line SVG
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 2" width="100%" height="2">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117" stop-opacity="0" />
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="1">
        <animate attributeName="stop-color" values="#38bdf8;#c084fc;#818cf8;#38bdf8" dur="3s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect width="1000" height="2" fill="url(#grad)" rx="1"/>
</svg>"""

with open('assets/animated_line.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

# 2. Update README
with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # Remove old achievements section
    if '🏆 Achievements at a Glance' in line:
        skip = True
        continue
    if skip and '</div>' in line:
        skip = False
        continue
    if skip:
        continue
    
    # Replace dividers
    if 'assets/custom_divider.png' in line:
        new_lines.append('<img src="assets/animated_line.svg" width="100%" height="3">\n')
        continue

    # Compact Featured Projects
    if '<td width="50%" valign="top">' in line:
        new_lines.append(line)
        continue
    if '<h3>' in line:
        title = line.replace('<h3>', '<b>').replace('</h3>', '</b><br/>')
        new_lines.append(title)
        continue
    if '<p><i>' in line:
        subtitle = line.replace('<p>', '').replace('</p>', '<br/><br/>')
        new_lines.append(subtitle)
        continue
    if '<p>' in line and '<code>' in line:
        tech = line.replace('<p>', '').replace('</p>', '')
        new_lines.append(tech)
        continue
    if '✓' in line:
        point = line.replace('<p>', '').replace('</p>', '<br/><br/>')
        new_lines.append(point)
        continue
    if line.strip() == '<p>' or line.strip() == '</p>':
        continue # Drop empty p tags from projects

    new_lines.append(line)

# Add Achievements after About Me (which ends at assassins_reversed.gif)
final_lines = []
for i, line in enumerate(new_lines):
    final_lines.append(line)
    if 'assets/assassins_reversed.gif' in line:
        final_lines.append('\n<img src="assets/animated_line.svg" width="100%" height="3">\n\n')
        final_lines.append('## 🏆 Achievements at a Glance\n\n')
        final_lines.append('<div align="center">\n  <table bordercolor="#161b22">\n    <tr>\n      <td align="left">\n        <ul>\n')
        final_lines.append('          <li>🏅 <b>Honeywell Hackathon:</b> Round 1 Shortlist — Eco-Loop AI</li>\n')
        final_lines.append('          <li>🥈 <b>SIH 2025:</b> Pitched HealthSeva AI at College Round</li>\n')
        final_lines.append('          <li>🤖 <b>IBM Call for Code:</b> Winner — AI Knowledge Challenge</li>\n')
        final_lines.append('          <li>☁️ <b>AWS Certified:</b> Academy Graduate — Cloud Architecting</li>\n')
        final_lines.append('        </ul>\n      </td>\n    </tr>\n  </table>\n</div>\n')

# Add quote at the end
final_lines.append('\n<br/>\n\n<div align="center">\n  <i>"Talk is cheap. Show me the code."</i><br/>— Linus Torvalds\n</div>\n')

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)
