import json
import aiofiles

async def save_books(books: list[dict]) -> None:
    async with aiofiles.open("books.json", "w") as file:
        await file.write(json.dumps(books, indent=4))

async def load_books() -> list[dict]:
    try:
        async with aiofiles.open("books.json", "r") as file:
            content = await file.read()
            books = json.loads(content)
    except FileNotFoundError:
        await save_books([])
        books = []
    return books




async def save_authors(authors: list[dict]) -> None:
    async with aiofiles.open("authors.json", "w") as file:
        await file.write(json.dumps(authors, indent=4))

async def load_authors() -> list[dict]:
    try:
        async with aiofiles.open("authors.json", "r") as file:
            content = await file.read()
            authors = json.loads(content)
    except FileNotFoundError:
        await save_authors([])
        authors = []
    return authors




async def save_loans(loans: list[dict]) -> None:
    async with aiofiles.open("loans.json", "w") as file:
        await file.write(json.dumps(loans, indent=4))

async def load_loans() -> list[dict]:
    try:
        async with aiofiles.open("loans.json", "r") as file:
            content = await file.read()
            loans = json.loads(content)
    except FileNotFoundError:
        await save_loans([])
        loans = []
    return loans
