import json
import aiofiles

BOOKS_FILE = "books.json"
AUTHORS_FILE = "authors.json"
LOANS_FILE = "loans.json"

async def save_books(books: list[dict]) -> None:
    async with aiofiles.open(BOOKS_FILE, "w") as file:
        await file.write(json.dumps(books, indent=4))

async def load_books() -> list[dict]:
    try:
        async with aiofiles.open(BOOKS_FILE, "r") as file:
            content = await file.read()
            books = json.loads(content)
    except FileNotFoundError:
        await save_books([])
        books = []
    return books




async def save_authors(authors: list[dict]) -> None:
    async with aiofiles.open(AUTHORS_FILE, "w") as file:
        await file.write(json.dumps(authors, indent=4))

async def load_authors() -> list[dict]:
    try:
        async with aiofiles.open(AUTHORS_FILE, "r") as file:
            content = await file.read()
            authors = json.loads(content)
    except FileNotFoundError:
        await save_authors([])
        authors = []
    return authors




async def save_loans(loans: list[dict]) -> None:
    async with aiofiles.open(LOANS_FILE, "w") as file:
        await file.write(json.dumps(loans, indent=4))

async def load_loans() -> list[dict]:
    try:
        async with aiofiles.open(LOANS_FILE, "r") as file:
            content = await file.read()
            loans = json.loads(content)
    except FileNotFoundError:
        await save_loans([])
        loans = []
    return loans
