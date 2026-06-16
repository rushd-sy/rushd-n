import asyncio

from fetching_using_async import fetch_data, fetch_data_sync
import httpx
import pytest
import time

def sleep_sync(request):
    time.sleep(1)
    return httpx.Response(200, json={"status": "ok"})

async def sleep_async(request):
    await asyncio.sleep(1)
    return httpx.Response(200, json={"status": "ok"})

@pytest.mark.asyncio
async def test_fetch_data(respx_mock):
    fetch_url = "https://api.github.com/repos/python/cpython"
    urls = [fetch_url] * 10
    respx_mock.get(fetch_url).mock(side_effect=sleep_sync)
    sync_time = fetch_data_sync(urls)

    respx_mock.clear()

    respx_mock.get(fetch_url).mock(side_effect=sleep_async)
    async_time = await fetch_data(urls)
    assert async_time < sync_time