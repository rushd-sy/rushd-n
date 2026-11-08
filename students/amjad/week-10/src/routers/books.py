from fastapi import Depends, Path, APIRouter, BackgroundTasks
from typing import Annotated

from models import BookCreate, BookOut, Page
from dependency import CommonsDepForPagination, CurrentUserDep
from services.book_service import BookService

router = APIRouter()


# `async def` because they perform I/O operations
@router.get("/", response_model=Page[BookOut])
async def get_books(
    commons: CommonsDepForPagination,
    author: str | None = None,
    genre: str | None = None,
    min_year: int | None = None,
    service: BookService = Depends(BookService),
) -> Page[BookOut]:
    """
    Retrieve a list of books with optional filters.
    - **author**: Filter books by author name.
    - **genre**: Filter books by genre.
    - **min_year**: Filter books published after a certain year.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    return await service.list(commons, author, genre, min_year)


# `async def` because it performs an I/O operation such as reading from storage
@router.get("/{book_id}", response_model=BookOut)
async def get_book(
    book_id: Annotated[int, Path(gt=0)], service: BookService = Depends(BookService)
) -> BookOut:
    """
    Retrieve a book by its ID.
    - **book_id**: The ID of the book to retrieve and must be a positive integer.
    - Returns the book details if found, otherwise raises a 404 error.
    """
    return await service.get_by_id(book_id)


# `async def` because they perform I/O operations
@router.post("/", response_model=BookOut)
async def create_book(
    book: BookCreate,
    user_id: CurrentUserDep,
    background_tasks: BackgroundTasks,
    service: BookService = Depends(BookService),
) -> BookOut:
    """
    Create a new book.
    - **book**: The details of the book to create.
    - **user_id**: The ID of the user creating the book.
    - **background_tasks**: The background tasks to run after creating the book.
    - Returns the created book details.
    """
    return await service.create(book, user_id, background_tasks)


# `async def` because they perform I/O operations
@router.put("/{book_id}", response_model=BookOut)
async def update_book(
    book_id: Annotated[int, Path(gt=0)],
    book: BookCreate,
    user_id: CurrentUserDep,
    service: BookService = Depends(BookService),
) -> BookOut:
    """
    Update an existing book.
    - **book_id**: The ID of the book to update and must be a positive integer.
    - **book**: The updated details of the book.
    - **user_id**: The ID of the user updating the book.
    - Returns the updated book details if found, otherwise raises a 404 error.
    """
    return await service.update(book_id, book, user_id)


# `async def` because they perform I/O operations
@router.delete("/{book_id}", response_model=BookOut)
async def delete_book(
    book_id: Annotated[int, Path(gt=0)],
    user_id: CurrentUserDep,
    service: BookService = Depends(BookService),
) -> BookOut:
    """
    Delete a book by its ID.
    - **book_id**: The ID of the book to delete and must be a positive integer.
    - **user_id**: The ID of the user deleting the book.
    - Returns the deleted book details if found, otherwise raises a 404 error.
    """
    return await service.delete(book_id, user_id)
