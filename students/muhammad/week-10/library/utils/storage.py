import json
import aiofiles

from models.books import BookModel
from models.authors import AuthorModel
from models.loans import LoanModel

BOOKS_FILE = "books.json"
AUTHORS_FILE = "authors.json"
LOANS_FILE = "loans.json"

async def save_books(books_models: list[BookModel]) -> None:
    books = [book.model_dump(mode="json") for book in books_models]
    async with aiofiles.open(BOOKS_FILE, "w") as file:
        await file.write(json.dumps(books, indent=4))

async def load_books() -> list[BookModel]:
    try:
        async with aiofiles.open(BOOKS_FILE, "r") as file:
            content = await file.read()
            books = [BookModel.model_validate(item) for item in json.loads(content)]
    except FileNotFoundError: 
        await save_books([]) 
        books = []
    return books




async def save_authors(authors_models: list[AuthorModel]) -> None:
    authors = [author.model_dump(mode="json") for author in authors_models]
    async with aiofiles.open(AUTHORS_FILE, "w") as file:
        await file.write(json.dumps(authors, indent=4))

async def load_authors() -> list[AuthorModel]:
    try:
        async with aiofiles.open(AUTHORS_FILE, "r") as file:
            content = await file.read()
            authors = [AuthorModel.model_validate(item) for item in json.loads(content)]
    except FileNotFoundError:
        await save_authors([])
        authors = []
    return authors




async def save_loans(loans_models: list[LoanModel]) -> None:
    loans = [loan.model_dump(mode="json") for loan in loans_models]
    async with aiofiles.open(LOANS_FILE, "w") as file:
        await file.write(json.dumps(loans, indent=4))

async def load_loans() -> list[LoanModel]:
    try:
        async with aiofiles.open(LOANS_FILE, "r") as file:
            content = await file.read()
            loans = [LoanModel.model_validate(item) for item in json.loads(content)]
    except FileNotFoundError:
        await save_loans([])
        loans = []
    return loans
