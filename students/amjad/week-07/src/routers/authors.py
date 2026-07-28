from fastapi import Depends, HTTPException, Path, Query, APIRouter
from typing import Annotated

from datetime import datetime
from models import Author, AuthorCreate, AuthorOut, Page
from storage import load_authors, load_books, load_loans, save_authors, save_books, save_loans
from dependency import CommonsDepForPagination, CurrentUserDep

router = APIRouter()

class AuthorService:

    async def create_author(self, author: AuthorCreate, user_id: CurrentUserDep) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        authors = load_authors()
        created_at = datetime.now().isoformat()
        new_author = Author(author_id=max([stored_author["author_id"] for stored_author in authors], default=0) + 1, **author.model_dump(), books=[], created_at=created_at)
        authors.append(new_author.model_dump())
        save_authors(authors)
        return AuthorOut(**new_author.model_dump())

    async def get_authors(
        self, 
        commons: CommonsDepForPagination,
        author: str | None = Query(default=None, description="Filter authors by name"),
    ) -> Page[AuthorOut]:
        authors = load_authors()
        authors_out = []
        for a in authors:
            if author and a["name"] != author:
                continue
            authors_out.append(AuthorOut(**a))

        total = len(authors_out)
        offset = commons["offset"]
        limit = commons["limit"]
        authors_out = authors_out[offset:offset + limit]
        return Page[AuthorOut](items=authors_out, total=total, offset=offset, limit=limit)

    async def get_author(self, author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
        authors = load_authors()
        for author in authors:
            if author["author_id"] == author_id:
                return AuthorOut(**author)
        raise HTTPException(status_code=404, detail="Author not found")

    async def update_author(self, author_id: Annotated[int, Path(gt=0)], author: AuthorCreate, user_id: CurrentUserDep) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        authors = load_authors()
        for i, a in enumerate(authors):
            if a["author_id"] == author_id:
                updated_author = Author(author_id=author_id, **author.model_dump(), created_at=a["created_at"])
                authors[i] = updated_author.model_dump()
                save_authors(authors)
                return AuthorOut(**authors[i])
        raise HTTPException(status_code=404, detail="Author not found")

    async def delete_author(self, author_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        authors = load_authors()
        for i, author in enumerate(authors):
            if author["author_id"] == author_id:
                deleted_author = AuthorOut(**authors[i])
                authors.pop(i)
                save_authors(authors)
                return deleted_author
        raise HTTPException(status_code=404, detail="Author not found")

@router.post("/", response_model=AuthorOut)
async def create_author(author: AuthorCreate, user_id: CurrentUserDep, service: AuthorService = AuthorService()) -> AuthorOut:
    """
    Create a new author.
    - **author**: The details of the author to create.
    - **user_id**: The ID of the user creating the author.
    - Returns the created author details.
    """
    return await service.create_author(author, user_id)

@router.get("/", response_model=Page[AuthorOut])
async def get_authors(
    commons: CommonsDepForPagination,
    author: str | None = Query(default=None, description="Filter authors by name"),
    service: AuthorService = AuthorService()
) -> Page[AuthorOut]:
    """
    Retrieve a list of authors with optional filters.
    - **author**: Filter authors by name.
    - **genre**: Filter authors by genre.
    - **min_year**: Filter authors who started publishing after a certain year.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    return await service.get_authors(commons, author)

@router.get("/{author_id}", response_model=AuthorOut)
async def get_author(author_id: Annotated[int, Path(gt=0)], service: AuthorService = AuthorService()) -> AuthorOut:
    """
    Retrieve an author by their ID.
    - **author_id**: The ID of the author to retrieve and must be a positive integer.
    - Returns the author details if found, otherwise raises a 404 error.
    """
    return await service.get_author(author_id)

@router.put("/{author_id}", response_model=AuthorOut)
async def update_author(author_id: Annotated[int, Path(gt=0)], author: AuthorCreate, user_id: CurrentUserDep, service: AuthorService = AuthorService()) -> AuthorOut:
    """
    Update an existing author.
    - **author_id**: The ID of the author to update and must be a positive integer.
    - **author**: The updated details of the author.
    - **user_id**: The ID of the user updating the author.
    - Returns the updated author details if found, otherwise raises a 404 error.
    """
    return await service.update_author(author_id, author, user_id)

@router.delete("/{author_id}", response_model=AuthorOut)
async def delete_author(author_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep, service: AuthorService = AuthorService()) -> AuthorOut:
    """
    Delete an author by their ID.
    - **author_id**: The ID of the author to delete and must be a positive integer.
    - **user_id**: The ID of the user deleting the author.
    - Returns the deleted author details if found, otherwise raises a 404 error.
    """
    return await service.delete_author(author_id, user_id)