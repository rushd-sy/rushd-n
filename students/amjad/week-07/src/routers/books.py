from fastapi import HTTPException, Path, Query, APIRouter
from typing import Annotated

from datetime import datetime
from models import BookCreate, Book, BookOut, BookOut, Page
from storage import load_books, save_books

router = APIRouter()


@router.get("/", response_model=Page[BookOut])
async def get_books(
    author: str | None = None,
    genre: str | None = None,
    min_year: int | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10
) -> Page[BookOut]:
    """
    Retrieve a list of books with optional filters.
    - **author**: Filter books by author name.
    - **genre**: Filter books by genre.
    - **min_year**: Filter books published after a certain year.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    books = load_books()
    books_out = []
    for book in books:
        if author and book["author"] != author:
            continue
        if genre and book["genre"] != genre:
            continue
        if min_year and book["year"] < min_year:
            continue
        books_out.append(BookOut(**book))
    
    total = len(books_out)
    books_out = books_out[offset:offset + limit]
    return Page[BookOut](items=books_out, total=total, offset=offset, limit=limit)

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: Annotated[int, Path(gt=0)]) -> BookOut:
    """
    Retrieve a book by its ID.
    - **book_id**: The ID of the book to retrieve and must be a positive integer.
    - Returns the book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return BookOut(**book)
    raise HTTPException(status_code=404, detail="Book not found")



@router.post("/", response_model=BookOut)
async def create_book(book: BookCreate) -> BookOut:
    """
    Create a new book.
    - **book**: The details of the book to create.
    - Returns the created book details.
    """
    books = load_books()    
    created_at = datetime.now().isoformat()
    new_book = Book(book_id=max([stored_book["book_id"] for stored_book in books], default=0) + 1, **book.model_dump(), created_at=created_at)
    books.append(new_book.model_dump())
    save_books(books)
    return BookOut(**new_book.model_dump())

@router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: Annotated[int, Path(gt=0)], book: BookCreate) -> BookOut:
    """
    Update an existing book.
    - **book_id**: The ID of the book to update and must be a positive integer.
    - **book**: The updated details of the book.
    - Returns the updated book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for i, b in enumerate(books):
        if b["book_id"] == book_id:
            updated_book = Book(book_id=book_id, **book.model_dump(), created_at=b["created_at"])
            books[i] = updated_book.model_dump()
            save_books(books)
            return BookOut(**books[i])
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/{book_id}", response_model=BookOut)
async def delete_book(book_id: Annotated[int, Path(gt=0)]) -> BookOut:
    """
    Delete a book by its ID.
    - **book_id**: The ID of the book to delete and must be a positive integer.
    - Returns the deleted book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for i, book in enumerate(books):
        if book["book_id"] == book_id:
            deleted_book = BookOut(**books[i])
            books.pop(i)
            save_books(books)
            return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")