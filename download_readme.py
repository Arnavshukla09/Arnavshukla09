import urllib.request
try:
    html = urllib.request.urlopen('https://raw.githubusercontent.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/main/README.md').read().decode('utf-8')
    with open('cool_gifs_readme.md', 'w', encoding='utf-8') as f:
        f.write(html)
except Exception as e:
    print(e)
