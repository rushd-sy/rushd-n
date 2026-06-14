import httpx
from pydantic import BaseModel

class Repo(BaseModel):
    name: str
    stars: int
    language: str | None
    url: str



def main():
    url = "https://api.github.com/users/mohammedbabelly20/repos"
    params = {
        "sort" : "starts",
        "direction" : "desc",
        "per_page" : 10
    }

    response = httpx.get(url, params=params)
    
    response.raise_for_status()
    if response.status_code == 403 and "rate_limit" in response.text.lower():
        raise RuntimeError("Rate limit exceeded")
    if response.status_code == 404:
        raise ValueError("User not found")

    data = response.json()
    repos: list[Repo] = []

    for repo_data in data:
        repo = Repo( 
            name=repo_data['name'],
            stars=int(repo_data['stargazers_count']),
            language=repo_data['language'],
            url=repo_data['html_url']
        )
        repos.append(repo)
    
    for ind, repo in enumerate(repos):
        print(f"Repo's num: {ind}")
        print(f"\tRepo's name: {repo.name}")
        print(f"\tRepo's stars: {repo.stars}")
        print(f"\tRepo's language: {repo.language}")
        print(f"\tRepo's url: {repo.url}")

if __name__ == '__main__':
    main()
