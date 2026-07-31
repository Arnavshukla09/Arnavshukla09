import os

headers = [
    ("about", "About Me"),
    ("tech", "Tech Stack"),
    ("projects", "Featured Projects"),
    ("analytics", "GitHub Analytics"),
    ("achievements", "Achievements"),
    ("focus", "Current Focus"),
    ("connect", "Let's Connect")
]

svg_template = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="40" viewBox="0 0 800 40">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#{color1}">
        <animate attributeName="stop-color" values="#{color1};#{color2};#{color3};#{color1}" dur="3s" repeatCount="indefinite" />
      </stop>
      <stop offset="50%" stop-color="#{color2}">
        <animate attributeName="stop-color" values="#{color2};#{color3};#{color1};#{color2}" dur="3s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#{color3}">
        <animate attributeName="stop-color" values="#{color3};#{color1};#{color2};#{color3}" dur="3s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700&amp;display=swap');
      .title {{
        font-family: 'Outfit', sans-serif;
        font-size: 26px;
        font-weight: 700;
        fill: url(#gradient);
      }}
    </style>
  </defs>
  <text x="0" y="30" class="title">{text}</text>
</svg>"""

colors = [
    ("38bdf8", "818cf8", "c084fc"),
    ("10b981", "3b82f6", "8b5cf6"),
    ("f59e0b", "ef4444", "ec4899"),
    ("3b82f6", "8b5cf6", "ec4899"),
    ("f59e0b", "84cc16", "10b981"),
    ("ef4444", "f59e0b", "eab308"),
    ("8b5cf6", "d946ef", "f43f5e")
]

os.makedirs("assets", exist_ok=True)

for (name, text), color in zip(headers, colors):
    svg_content = svg_template.format(
        text=text,
        color1=color[0],
        color2=color[1],
        color3=color[2]
    )
    with open(f"assets/header_{name}.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
