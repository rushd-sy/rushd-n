import httpx
import pytest
from fetching_user_repos import fetch_repositories

def test_fetch_repositories_valid_user(respx_mock):

    fetch_url = "https://api.github.com/search/repositories"

    params = {
        "q": f"user:octocat",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    respx_mock.get(fetch_url, params=params).mock(
        return_value=httpx.Response(
            200, 
            json={
                "items": [
                    {
                        "name": "Hello-World",
                        "language": "Python",
                        "stargazers_count": 42,
                        "html_url": "https://github.com/octocat/Hello-World"
                    }
                ]
            }
            )
    )
    repos = fetch_repositories("octocat")
    assert isinstance(repos, list)
    assert len(repos) > 0
    for repo in repos:
        assert hasattr(repo, 'name')
        assert hasattr(repo, 'language')
        assert hasattr(repo, 'stars')
        assert hasattr(repo, 'url')

def test_fetch_repositories_invalid_user(respx_mock):

    params = {
        "q": f"user:djfahlsieuhcvsaol",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    respx_mock.get("https://api.github.com/search/repositories", params=params).mock(return_value=httpx.Response(422))
    with pytest.raises(SystemExit, match="User 'djfahlsieuhcvsaol' not found"):
        fetch_repositories("djfahlsieuhcvsaol")
