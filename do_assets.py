import os
import urllib.request
from PIL import Image, ImageSequence

# 1. Download and reverse the Assassin's Creed GIF
gif_url = 'https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif'
print("Downloading GIF...")
urllib.request.urlretrieve(gif_url, 'temp_assassins.gif')

print("Reversing GIF...")
im = Image.open('temp_assassins.gif')
frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
frames.reverse()
frames[0].save('assets/assassins_reversed.gif', save_all=True, append_images=frames[1:], loop=0, duration=im.info.get('duration', 100))
os.remove('temp_assassins.gif')

# 2. Generate animated_line.svg
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="4" preserveAspectRatio="none">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="50%" stop-color="#818cf8">
        <animate attributeName="stop-color" values="#818cf8;#c084fc;#38bdf8;#818cf8" dur="3s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>
  </defs>
  <rect width="100%" height="4" fill="url(#grad)" rx="2"/>
</svg>"""

with open('assets/animated_line.svg', 'w') as f:
    f.write(svg_content)

print("Done!")
