import os
import sys
import httpx

from dotenv import load_dotenv

def get_github_token():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise ValueError("Token not valid")
    
    return token


def fetch_private_repos():
    url = "https://api.github.com/user/repos"
    token = get_github_token()
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "visibility": "private",
    }
    
    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10.0)
        
        # Check authentication
        if response.status_code == 401:
            print("❌ Authentication failed!")
            print("   Your token might be invalid or expired.")
            print("   Check your token at: https://github.com/settings/tokens")
            sys.exit(1)
        
        if response.status_code == 403:
            print("❌ Forbidden!")
            print("   Your token doesn't have the right permissions.")
            print("   Make sure it has 'repo' scope for private repositories.")
            sys.exit(1)
        
        response.raise_for_status()
        
        repos = response.json()
        return repos
    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)

def main():
    repos = fetch_private_repos()
    
    if not repos:
        print("You have no private repositories.")
        return

    print(f"Found {len(repos)} private repositories:")
    
    for repo in repos:
        print(f"Repo's name: {repo['name']}")
        print(f"\tDescription: {repo['description']}")
        print(f"\tLanguage: {repo['language']}")
        print(f"\tStars: {repo['stargazers_count']}")
        print(f"\tURL: {repo['url']}")
        print()



if __name__ == "__main__":
    main()