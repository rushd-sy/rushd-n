import time
import httpx
import asyncio

async def get_url(client: httpx.AsyncClient, url: str) -> httpx.Response:
    response = await client.get(url)
    response.raise_for_status()
    return response

async def fetch_data(urls: list[str]) -> float:
    async with httpx.AsyncClient() as client:
        time_before = time.perf_counter()
        tasks = [get_url(client, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        time_after = time.perf_counter()
    return time_after - time_before

def fetch_data_sync(urls: list[str]) -> float:
    with httpx.Client() as client:
        time_before = time.perf_counter()
        for url in urls:
            response = client.get(url)
            response.raise_for_status()
        time_after = time.perf_counter()
    return time_after - time_before

if __name__ == "__main__":
    fetch_url = "https://api.github.com/repos/python/cpython"
    urls = [fetch_url] * 10
    sync_time = fetch_data_sync(urls)
    async_time = asyncio.run(fetch_data(urls))
    print(f"time saved: {sync_time - async_time:.2f} seconds")