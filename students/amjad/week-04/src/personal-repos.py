import os
from dotenv import load_dotenv
import httpx

load_dotenv() 
if "GITHUB_TOKEN" not in os.environ:
    raise ValueError("GITHUB_TOKEN environment variable is not set")
github_token = os.environ.get("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {github_token}"
}
response = httpx.get("https://api.github.com/user/repos", headers=headers)
response.raise_for_status()
repos = response.json()
for repo in repos:
    if repo["private"] == True:
        print(f"Name: {repo['name']}")
        print(f"URL: {repo['html_url']}")
        print("-" * 40)
