import json
import aiofiles
from models import Book, Author, Loan


async def load_books() -> list[Book]:
    try:
        async with aiofiles.open("books.json", "r", encoding="utf-8") as f:
            books = json.loads(await f.read())
    except FileNotFoundError:
        books = []

        async with aiofiles.open("books.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(books, indent=4))

    return [Book(**b) for b in books]


async def save_books(books: list[Book]) -> None:
    async with aiofiles.open("books.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps([book.model_dump() for book in books], indent=4))


async def load_loans() -> list[Loan]:
    try:
        async with aiofiles.open("loans.json", "r", encoding="utf-8") as f:
            loans = json.loads(await f.read())
    except FileNotFoundError:
        loans = []

        async with aiofiles.open("loans.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(loans, indent=4))

    return [Loan(**loan) for loan in loans]


async def save_loans(loans: list[Loan]) -> None:
    async with aiofiles.open("loans.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps([loan.model_dump() for loan in loans], indent=4))


async def load_authors() -> list[Author]:
    try:
        async with aiofiles.open("authors.json", "r", encoding="utf-8") as f:
            authors = json.loads(await f.read())
    except FileNotFoundError:
        authors = []

        async with aiofiles.open("authors.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(authors, indent=4))

    return [Author(**a) for a in authors]


async def save_authors(authors: list[Author]) -> None:
    async with aiofiles.open("authors.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps([author.model_dump() for author in authors], indent=4))
