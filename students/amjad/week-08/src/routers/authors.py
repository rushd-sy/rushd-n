from fastapi import Depends, Path, Query, APIRouter
from typing import Annotated

from models import AuthorCreate, AuthorOut, Page
from dependency import CommonsDepForPagination, CurrentUserDep
from services.author_service import AuthorService

router = APIRouter()


# `async def` because they perform I/O operations
@router.post("/", response_model=AuthorOut)
async def create_author(
    author: AuthorCreate,
    user_id: CurrentUserDep,
    service: AuthorService = Depends(AuthorService),
) -> AuthorOut:
    """
    Create a new author.
    - **author**: The details of the author to create.
    - **user_id**: The ID of the user creating the author.
    - Returns the created author details.
    """
    return await service.create_author(author, user_id)


# `async def` because they perform I/O operations
@router.get("/", response_model=Page[AuthorOut])
async def get_authors(
    commons: CommonsDepForPagination,
    author: str | None = Query(default=None, description="Filter authors by name"),
    service: AuthorService = Depends(AuthorService),
) -> Page[AuthorOut]:
    """
    Retrieve a list of authors with optional filters.
    - **author**: Filter authors by name.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    return await service.get_authors(commons, author)


# `async def` because they perform I/O operations
@router.get("/{author_id}", response_model=AuthorOut)
async def get_author(
    author_id: Annotated[int, Path(gt=0)],
    service: AuthorService = Depends(AuthorService),
) -> AuthorOut:
    """
    Retrieve an author by their ID.
    - **author_id**: The ID of the author to retrieve and must be a positive integer.
    - Returns the author details if found, otherwise raises a 404 error.
    """
    return await service.get_author(author_id)


# `async def` because they perform I/O operations
@router.put("/{author_id}", response_model=AuthorOut)
async def update_author(
    author_id: Annotated[int, Path(gt=0)],
    author: AuthorCreate,
    user_id: CurrentUserDep,
    service: AuthorService = Depends(AuthorService),
) -> AuthorOut:
    """
    Update an existing author.
    - **author_id**: The ID of the author to update and must be a positive integer.
    - **author**: The updated details of the author.
    - **user_id**: The ID of the user updating the author.
    - Returns the updated author details if found, otherwise raises a 404 error.
    """
    return await service.update_author(author_id, author, user_id)


# `async def` because they perform I/O operations
@router.delete("/{author_id}", response_model=AuthorOut)
async def delete_author(
    author_id: Annotated[int, Path(gt=0)],
    user_id: CurrentUserDep,
    service: AuthorService = Depends(AuthorService),
) -> AuthorOut:
    """
    Delete an author by their ID.
    - **author_id**: The ID of the author to delete and must be a positive integer.
    - **user_id**: The ID of the user deleting the author.
    - Returns the deleted author details if found, otherwise raises a 404 error.
    """
    return await service.delete_author(author_id, user_id)
