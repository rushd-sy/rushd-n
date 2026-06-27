import asyncio

import pytest
import httpx
import respx
import os
import time

from unittest.mock import patch

from task_01 import fetch_last_repos    
from task_02 import fetch_issues
from task_03.main import fetch_private_repos
from task_04 import fetch_async, fetch_sync
class Test:

    @respx.mock
    def test_task_one(self):
        mock_response = [ {
                "name": "test-1-repo",
                "stargazers_count": 42,
                "language": "Python",
                "html_url": "https://github.com/testuser/test-1-repo",
                "description": "A test repo"
            }, {
                "name": "test-2-repo",
                "stargazers_count": 10,
                "language": "JavaScript",
                "html_url": "https://github.com/testuser/test-2-repo",
                "description": None
            }
        ]
        
        respx.get("https://api.github.com/users/testuser/repos").mock(return_value=httpx.Response(200, json=mock_response)) 
        result = fetch_last_repos("testuser")
        assert result[0].name == "test-1-repo"
        assert result[0].stars == 42
        
        assert result[1].name == "test-2-repo"
        assert result[1].url == "https://github.com/testuser/test-2-repo"

    @respx.mock
    def test_task_two(self):
        mock_response = [ {
                "number": 1,
                "repository_url": "https://api.github.com/repos/owner/repo",
                "url": "https://api.github.com/repos/owner/repo/issues/1"
            }
        ]
        
        respx.get("https://api.github.com/repos/user/repo/issues").mock(return_value=httpx.Response(200, json=mock_response))
        
        result = fetch_issues(user="user", repo="repo")
        
        assert result == mock_response

    @respx.mock
    def test_task_three(self):
        mock_response = [
            {
                "name": "private-repo-1",
                "description": "First private repo",
                "language": "Python",
                "stargazers_count": 5,
                "url": "https://api.github.com/repos/testuser/private-repo-1"
            }
        ]
        
        respx.get("https://api.github.com/user/repos").mock(
            return_value=httpx.Response(200, json=mock_response)
        )
        
        with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
            result = fetch_private_repos()
        
        assert result == mock_response
        assert len(result) == 1
        assert result[0]["name"] == "private-repo-1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_task_four(self):
        
        
        def sync_slow(request):
            time.sleep(.1)
            return httpx.Response(200)
        
        async def async_slow(request):
            await asyncio.sleep(.1)
            return httpx.Response(200)
        
        respx.get("https://httpbin.org/delay/sync").mock(side_effect=sync_slow)
        respx.get("https://httpbin.org/delay/async").mock(side_effect=async_slow)
        sync_time = fetch_sync("https://httpbin.org/delay/sync")
        async_time = await fetch_async("https://httpbin.org/delay/async")
        
        assert async_time < sync_time