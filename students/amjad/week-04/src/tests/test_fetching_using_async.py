from fetching_using_async import fetch_data, fetch_data_sync
import asyncio

def test_fetch_data():
    fetch_url = "https://api.github.com/repos/python/cpython"
    urls = [fetch_url] * 10
    sync_time = fetch_data_sync(urls)
    async_time = asyncio.run(fetch_data(urls))
    assert async_time < sync_time