
import requests
import csv
from datetime import datetime
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise Exception('Por favor, defina a variável de ambiente GITHUB_TOKEN com seu token do GitHub.')
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

repositories = []
for page_number in range(1, 11):
    api_url = f"https://api.github.com/search/repositories?q=language:Java&sort=stars&order=desc&per_page=100&page={page_number}"
    response = requests.get(api_url, headers=headers)
    data = response.json()
    if 'items' in data:
        for repo in data['items']:
            releases_url = repo["releases_url"].replace("{/id}", "")
            releases_resp = requests.get(releases_url, headers=headers)
            releases = releases_resp.json()
            num_releases = len(releases) if isinstance(releases, list) else 0

            created_at = repo["created_at"]
            created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            age_years = (datetime.now() - created_date).days / 365

            repositories.append({
                "name": repo["full_name"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"],
                "clone_url": repo["clone_url"],
                "created_at": created_at,
                "age_years": round(age_years, 2),
                "num_releases": num_releases
            })
    else:
        print(f"A resposta da API não contém 'items' na página {page_number}. Resposta recebida: {data}")

csv_file = open("top_1000_java_repos.csv", "w", newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=["name", "stars", "url", "clone_url", "created_at", "age_years", "num_releases"])
csv_writer.writeheader()
csv_writer.writerows(repositories)
csv_file.close()