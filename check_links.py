import urllib.request, json

repos = ['RURAL-HEALTHCARE-PLATFORM', 'Eco_Loop_Building_Agents', 'talentmatch-ai', 'Student-Service-Portal---CampusCart']
for repo in repos:
    try:
        req = urllib.request.Request(f'https://api.github.com/repos/Arnavshukla09/{repo}', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"{repo} homepage: {data.get('homepage')}")
    except Exception as e:
        print(f"{repo} error: {e}")
