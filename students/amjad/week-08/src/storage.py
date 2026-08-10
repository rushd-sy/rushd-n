import json
import aiofiles

async def load_books() -> list[dict]:
    try:
        async with aiofiles.open("books.json", "r", encoding="utf-8") as f:
            books = json.loads(await f.read())
    except FileNotFoundError:
        books = []

        async with aiofiles.open("books.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(books, indent=4))

    return books

async def save_books(books: list[dict]) -> None:
    async with aiofiles.open("books.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(books, indent=4))


async def load_loans() -> list[dict]:
    try:
        async with aiofiles.open("loans.json", "r", encoding="utf-8") as f:
            loans = json.loads(await f.read())
    except FileNotFoundError:
        loans = []

        async with aiofiles.open("loans.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(loans, indent=4))

    return loans

async def save_loans(loans: list[dict]) -> None:
    async with aiofiles.open("loans.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(loans, indent=4))


async def load_authors() -> list[dict]:
    try:
        async with aiofiles.open("authors.json", "r", encoding="utf-8") as f:
            authors = json.loads(await f.read())
    except FileNotFoundError:
        authors = []

        async with aiofiles.open("authors.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(authors, indent=4))

    return authors

async def save_authors(authors: list[dict]) -> None:
    async with aiofiles.open("authors.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(authors, indent=4))

