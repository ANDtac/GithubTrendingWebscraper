import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

def fetch_trending_repositories():
    url = "https://github.com/trending"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    repo_list = soup.select(".Box-row")

    trending_repos = []

    for repo in repo_list[:10]:
        repo_name = repo.select_one(".lh-condensed a").text.strip().replace('\n', ' ')
        repo_url = "https://github.com" + repo.select_one(".lh-condensed a")["href"]
        repo_description = repo.select_one(".pr-4")
        if repo_description:
            repo_description = repo_description.text.strip()
        else:
            repo_description = "No description provided."

        stars = repo.select_one(".d-inline-block.float-sm-right").text.strip()

        trending_repos.append({
            "name": repo_name,
            "url": repo_url,
            "description": repo_description,
            "stars": stars
        })

    return trending_repos


def save_to_csv(repos, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'url', 'description', 'stars']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for repo in repos:
            writer.writerow(repo)

def main():
    trending_repos = fetch_trending_repositories()

    file_path = input("Enter the output file path (e.g., output.csv): ").strip()
    save_to_csv(trending_repos, file_path)

    print(f"Top 10 trending repositories on GitHub have been saved to '{Path(file_path).name}'.")

if __name__ == "__main__":
    main()
