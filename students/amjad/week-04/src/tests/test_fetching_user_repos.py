import pytest

from fetching_user_repos import fetch_repositories

def test_fetch_repositories_valid_user():
    repos = fetch_repositories("octocat")
    assert isinstance(repos, list)
    assert len(repos) > 0
    for repo in repos:
        assert hasattr(repo, 'name')
        assert hasattr(repo, 'language')
        assert hasattr(repo, 'stars')
        assert hasattr(repo, 'url')

def test_fetch_repositories_invalid_user():
    with pytest.raises(SystemExit, match="User 'djfahlsieuhcvsaol' not found"):
        fetch_repositories("djfahlsieuhcvsaol")
