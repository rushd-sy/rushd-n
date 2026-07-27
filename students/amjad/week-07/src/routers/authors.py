from fastapi import HTTPException, Path, Query, APIRouter
from typing import Annotated

from datetime import datetime
from models import Author, AuthorCreate, AuthorOut, BookCreate, Book, BookOut, LoanCreate, LoanOut, Loan, Page
from storage import load_authors, load_books, load_loans, save_authors, save_books, save_loans

router = APIRouter()

@router.post("/", response_model=AuthorOut)
async def create_author(author: AuthorCreate) -> AuthorOut:
    """
    Create a new author.
    - **author**: The details of the author to create.
    - Returns the created author details.
    """
    authors = load_authors()
    created_at = datetime.now().isoformat()
    new_author = Author(author_id=max([stored_author["author_id"] for stored_author in authors], default=0) + 1, **author.model_dump(), books=[], created_at=created_at)
    authors.append(new_author.model_dump())
    save_authors(authors)
    return AuthorOut(**new_author.model_dump())

@router.get("/", response_model=Page[AuthorOut])
async def get_authors() -> Page[AuthorOut]:
    """
    Retrieve all authors.
    - Returns a list of all authors.
    """
    authors = load_authors()
    return Page[AuthorOut](items=[AuthorOut(**author) for author in authors], total=len(authors))

@router.get("/{author_id}", response_model=AuthorOut)
async def get_author(author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
    """
    Retrieve an author by their ID.
    - **author_id**: The ID of the author to retrieve and must be a positive integer.
    - Returns the author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorOut(**author)
    raise HTTPException(status_code=404, detail="Author not found")

@router.put("/{author_id}", response_model=AuthorOut)
async def update_author(author_id: Annotated[int, Path(gt=0)], author: AuthorCreate) -> AuthorOut:
    """
    Update an existing author.
    - **author_id**: The ID of the author to update and must be a positive integer.
    - **author**: The updated details of the author.
    - Returns the updated author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for i, a in enumerate(authors):
        if a["author_id"] == author_id:
            updated_author = Author(author_id=author_id, **author.model_dump(), created_at=a["created_at"])
            authors[i] = updated_author.model_dump()
            save_authors(authors)
            return AuthorOut(**authors[i])
    raise HTTPException(status_code=404, detail="Author not found")

@router.delete("/{author_id}", response_model=AuthorOut)
async def delete_author(author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
    """
    Delete an author by their ID.
    - **author_id**: The ID of the author to delete and must be a positive integer.
    - Returns the deleted author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for i, author in enumerate(authors):
        if author["author_id"] == author_id:
            deleted_author = AuthorOut(**authors[i])
            authors.pop(i)
            save_authors(authors)
            return deleted_author
    raise HTTPException(status_code=404, detail="Author not found")