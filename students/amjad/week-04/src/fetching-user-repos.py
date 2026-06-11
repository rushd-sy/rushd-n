import httpx
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class Repo(BaseModel):
    name: str
    language: str | None = None
    stars: int = Field(alias="stargazers_count")
    url: HttpUrl = Field(alias="html_url")


username = input("Enter a GitHub username to fetch their repositories: ")

params = {
    "q": f"user:{username}",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}

fetch_url = "https://api.github.com/search/repositories"

try:
    response = httpx.get(fetch_url, params=params)
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 422:
        print(f"User '{username}' not found")
    elif e.response.status_code == 429: # 429 i hope
        print("API rate limit exceeded")
    exit(1)
except httpx.RequestError as e:
    print(f"Network error: {e}")
    exit(1)


data = response.json()
repos = []
for item in data["items"]:
    try:
        repo = Repo(**item)
        repos.append(repo)
    except ValidationError as e:
        print(f"Error parsing repository data: {e}")

for repo in repos:
    print(f"Name: {repo.name}")
    print(f"Language: {repo.language}")
    print(f"Stars: {repo.stars}")
    print(f"URL: {repo.url}")
    print("-" * 40)