import urllib.request, re
try:
    html = urllib.request.urlopen('https://raw.githubusercontent.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/main/README.md').read().decode('utf-8')
    urls = re.findall(r'src="(https://[^"]+\.gif)"', html)
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')
except Exception as e:
    print(e)
