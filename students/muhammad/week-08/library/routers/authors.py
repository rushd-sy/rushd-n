from fastapi import APIRouter, Path, HTTPException, Depends
from typing import Annotated
from models.authors import AuthorModel, AuthorResponse, AuthorCreate
from datetime import datetime

from models.page import Page
from utils.storage import load_authors, save_authors
from dependencies import get_pagination_params, get_current_user

router = APIRouter(prefix="/authors")



@router.get("/")
async def get_authors(
        pagination_params: Annotated[dict, Depends(get_pagination_params)],
        name: str | None = None,
        min_birth_year: int | None = None,
        max_birth_year: int | None = None,
    ) -> Page[AuthorResponse]:
    authors = load_authors()
    authors_out = []
    offset = pagination_params['offset']
    limit = pagination_params['limit']
    
    for dict_author in authors:
        author = AuthorResponse(**dict_author)
        if name and author.name != name:
            continue
        if min_birth_year and author.birth_year < min_birth_year:
            continue
        if max_birth_year and author.birth_year > max_birth_year:
            continue
        authors_out.append(author)
    
    total = len(authors_out)
    authors_out = authors_out[offset:offset + limit]
    
    return Page[AuthorResponse](
        items=authors_out,
        total=total,
        offset=offset,
        limit=limit
    )

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
        author_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[str, Depends(get_current_user)]
    ):

    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorResponse(**author)
    raise HTTPException(status_code=404, detail=f"author with id {author_id} doesn't exist")

@router.post("/", response_model=AuthorResponse)
async def create_author(request_author: AuthorCreate):
    authors = load_authors()

    created_author = AuthorModel(
        author_id=max([author["author_id"] for author in authors], default=0) + 1,
        **request_author.model_dump(),
        added_at=datetime.now().isoformat(),
    )
    authors.append(created_author.model_dump())
    save_authors(authors)

    return AuthorResponse(
        **created_author.model_dump(),
    )
    
    
    
@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: Annotated[int, Path(gt=0)],
    request_author: AuthorCreate
    ):
    authors = load_authors()
    
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            existing = AuthorModel(**author)
            updated_author = AuthorModel(
                author_id=author_id,
                **request_author.model_dump(),
                added_at=existing.added_at, 
            )
            
            authors[index] = updated_author.model_dump()
            save_authors(authors)
            
            return AuthorResponse(
                **updated_author.model_dump()
            )
    
    raise HTTPException(status_code=404, detail=f"author with id {author_id} doesn't exist")


@router.delete("/{author_id}")
async def delete_author(author_id: Annotated[int, Path(gt=0)]) -> None:
    authors = load_authors()
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            del authors[index]
            save_authors(authors)
            return
    
    raise HTTPException(status_code=404, detail=f"author with id {author_id} doesn't exist")
