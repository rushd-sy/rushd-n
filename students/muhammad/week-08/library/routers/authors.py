from fastapi import APIRouter, Path, Depends
from typing import Annotated

from models.authors import AuthorResponse, AuthorCreate
from models.page import Page
from dependencies import get_pagination_params, get_current_user
from services.author_services import AuthorServices

router = APIRouter(prefix="/authors")


@router.get("/")
async def get_authors(
    author_services: Annotated[AuthorServices, Depends(AuthorServices)],
    pagination_params: Annotated[dict, Depends(get_pagination_params)],
    name: str | None = None,
    min_birth_year: int | None = None,
    max_birth_year: int | None = None,
) -> Page[AuthorResponse]:

    return await author_services.get_authors(
        name=name,
        min_birth_year=min_birth_year,
        max_birth_year=max_birth_year,
        offset=pagination_params["offset"],
        limit=pagination_params["limit"]
    )


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_services: Annotated[AuthorServices, Depends(AuthorServices)],
    author_id: Annotated[int, Path(gt=0)],
):
    return await author_services.get_author_by_id(author_id)


@router.post("/", response_model=AuthorResponse)
async def create_author(
        author_services: Annotated[AuthorServices, Depends(AuthorServices)],
        request_author: AuthorCreate,
        user_id: Annotated[str, Depends(get_current_user)],
    ):
    return await author_services.create_author(request_author)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
        author_services: Annotated[AuthorServices, Depends(AuthorServices)],
        author_id: Annotated[int, Path(gt=0)],
        request_author: AuthorCreate,
        user_id: Annotated[str, Depends(get_current_user)],
    ):
    return await author_services.update_author(
        author_id,
        request_author
    )


@router.delete("/{author_id}")
async def delete_author(
    author_services: Annotated[AuthorServices, Depends(AuthorServices)],
    author_id: Annotated[int, Path(gt=0)],
    user_id: Annotated[str, Depends(get_current_user)]
) -> AuthorResponse:

    return await author_services.delete_author(author_id)
