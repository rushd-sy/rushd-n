import httpx
from datetime import datetime, timedelta, timezone

def main():
    user = "Blue-Dots-Economy"
    repo = "bluedots-automation"
    url = f"https://api.github.com/repos/{user}/{repo}/issues"
    
    current_time = datetime.now(timezone.utc)
    oldest_time = current_time - timedelta(days=30)
    since_date_str = oldest_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    
    
    params = {
        "state" : "open",
        "since" : since_date_str,
    }

    response = httpx.get(url, params=params)

    response.raise_for_status()
    if response.status_code == 403 and "rate_limit" in response.text.lower():
        raise RuntimeError("Rate limit exceeded")
    if response.status_code == 404:
        raise ValueError("User not found")

    data = response.json()
    for ind, issue in enumerate(data):
        print(f"Issue {ind}:")
        print(f"\tIssue's number: {issue['number']}")
        print(f"\tIssue's repo url: {issue['repository_url']}")
        print(f"\tIssue's url: {issue['url']}")
        

if __name__ == '__main__':
    main()
