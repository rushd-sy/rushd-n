import asyncio
import time

from services.book_services import BookServices


isbns = [
        "9780140328721",
        "9780451524935",
        "9780743273565",
        "9780061120084",
        "9780261102217",
        "9780439023481",
        "9780307277671",
        "9780544003415",
        "9780316769488",
        "9780131103627",
    ]

def benchmark_sync():
    service = BookServices()
    start = time.perf_counter()

    for isbn in isbns:
        service.sync_get_book_from_ext_api(isbn)

    end = time.perf_counter()

    return end - start


async def benchmark_async():
    service = BookServices()

    start = time.perf_counter()
    await asyncio.gather(
        *(service.async_get_book_from_ext_api(isbn) for isbn in isbns)
    )

    end = time.perf_counter()

    return end - start


async def main():
    print("Test started..")
    sync_time = benchmark_sync()
    async_time = await benchmark_async()

    print(f"Sync time:  {sync_time:.4f} seconds")
    print(f"Async time: {async_time:.4f} seconds")

    if async_time < sync_time:
        improvement = ((sync_time - async_time) / sync_time) * 100
        print(f"Async is {improvement:.2f}% faster")
    else:
        difference = ((async_time - sync_time) / async_time) * 100
        print(f"Sync was {difference:.2f}% faster")


if __name__ == "__main__":
    asyncio.run(main())