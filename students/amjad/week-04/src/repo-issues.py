from datetime import date, timedelta

import httpx

url = input("Enter the URL of a GitHub repository: ")
api_url = url.replace("github.com", "api.github.com/repos")
date = date.today() - timedelta(days=30)
params = {
    "per_page": 10,
    "since": date.isoformat()
}

response = httpx.get(f"{api_url}/issues", params=params)
response.raise_for_status()

for issue in response.json():
    print(f"Issue #{issue['number']}: {issue['title'] } (created at {issue['created_at']})")