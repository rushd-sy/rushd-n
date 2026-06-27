import httpx
import asyncio
import time


def fetch_sync(url="https://httpbin.org/delay/1"):
    URLS = [url] * 10
    start = time.time()
    with httpx.Client() as client:
        for url in URLS:
            client.get(url)
    return time.time() - start

async def fetch_async(url="https://httpbin.org/delay/1"):
    URLS = [url] * 10
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in URLS]
        await asyncio.gather(*tasks)
    return time.time() - start

async def main():
    sync_time = fetch_sync()
    print(f"Sequential: {sync_time:.2f}s")

    async_time = await fetch_async()
    print(f"Async: {async_time:.2f}s")
    
    print(f"Async was {sync_time/async_time:.1f}x faster")

if __name__ == "__main__":
    asyncio.run(main())