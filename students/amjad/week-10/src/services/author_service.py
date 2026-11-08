from fastapi import HTTPException, Path, Query
from typing import Annotated

from datetime import datetime
from models import Author, AuthorCreate, AuthorOut, Page
from storage import load_authors, save_authors
from dependency import CommonsDepForPagination, CurrentUserDep


class AuthorService:

    async def create_author(
        self, author: AuthorCreate, user_id: CurrentUserDep
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        authors = await load_authors()
        created_at = datetime.now().isoformat()
        new_author = Author(
            author_id=max(
                [stored_author.author_id for stored_author in authors], default=0
            )
            + 1,
            name=author.name,
            birth_year=author.birth_year,
            created_at=created_at,
        )
        authors.append(new_author)
        await save_authors(authors)
        return AuthorOut(**new_author.model_dump())

    async def get_authors(
        self,
        commons: CommonsDepForPagination,
        author: str | None = Query(default=None, description="Filter authors by name"),
    ) -> Page[AuthorOut]:
        authors = await load_authors()
        authors_out = []
        for a in authors:
            if author and a.name != author:
                continue
            authors_out.append(AuthorOut(**a.model_dump()))

        total = len(authors_out)
        offset = commons.offset
        limit = commons.limit
        authors_out = authors_out[offset : offset + limit]
        return Page[AuthorOut](
            items=authors_out, total=total, offset=offset, limit=limit
        )

    async def get_author(self, author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
        authors = await load_authors()
        for author in authors:
            if author.author_id == author_id:
                return AuthorOut(**author.model_dump())
        raise HTTPException(status_code=404, detail="Author not found")

    async def update_author(
        self,
        author_id: Annotated[int, Path(gt=0)],
        author: AuthorCreate,
        user_id: CurrentUserDep,
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        authors = await load_authors()
        for i, a in enumerate(authors):
            if a.author_id == author_id:
                updated_author = Author(
                    author_id=author_id,
                    name=author.name,
                    birth_year=author.birth_year,
                    created_at=a.created_at,
                )
                authors[i] = updated_author
                await save_authors(authors)
                return AuthorOut(**authors[i].model_dump())
        raise HTTPException(status_code=404, detail="Author not found")

    async def delete_author(
        self, author_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        authors = await load_authors()
        for i, author in enumerate(authors):
            if author.author_id == author_id:
                deleted_author = AuthorOut(**authors[i].model_dump())
                authors.pop(i)
                await save_authors(authors)
                return deleted_author
        raise HTTPException(status_code=404, detail="Author not found")
