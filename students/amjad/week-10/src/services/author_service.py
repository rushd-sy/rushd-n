from fastapi import HTTPException, Path, Query
from typing import Annotated

from datetime import datetime
from models import AuthorCreate, AuthorOut, Page
from db.db_models.Author import Author as DBAuthor
from dependency import CommonsDepForPagination, CurrentUserDep, CommonsDepForDB
from sqlalchemy import select, func

class AuthorService:
    def __init__(self, db: CommonsDepForDB) -> None:
        self.db = db

    async def create_author(
        self, author: AuthorCreate, user_id: CurrentUserDep
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        new_author = DBAuthor(
            name=author.name,
            birth_year=author.birth_year,
            created_at=datetime.now(),
        )
        self.db.add(new_author)
        await self.db.commit()
        await self.db.refresh(new_author)
        return AuthorOut.model_validate(new_author)

    async def get_authors(
        self,
        commons: CommonsDepForPagination,
        author: str | None = Query(default=None, description="Filter authors by name"),
    ) -> Page[AuthorOut]:
        offset = commons.offset
        limit = commons.limit
        query = select(DBAuthor)
        if author is not None:
            query = query.where(DBAuthor.name == author)
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()
        result = await self.db.execute(query.order_by(DBAuthor.author_id).offset(offset).limit(limit))
        db_authors = result.scalars().all()
        authors_out = [AuthorOut.model_validate(author) for author in db_authors]
        return Page[AuthorOut](
            items=authors_out, total=total, offset=offset, limit=limit
        )

    async def get_author(self, author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
        query = select(DBAuthor).where(DBAuthor.author_id == author_id)
        result = await self.db.execute(query)
        db_author = result.scalar_one_or_none()
        if not db_author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorOut.model_validate(db_author)

    async def update_author(
        self,
        author_id: Annotated[int, Path(gt=0)],
        author: AuthorCreate,
        user_id: CurrentUserDep,
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBAuthor).where(DBAuthor.author_id == author_id)
        result = await self.db.execute(query)
        db_author = result.scalar_one_or_none()
        if not db_author:
            raise HTTPException(status_code=404, detail="Author not found")
        db_author.name = author.name
        db_author.birth_year = author.birth_year
        await self.db.commit()
        await self.db.refresh(db_author)
        return AuthorOut.model_validate(db_author)

    async def delete_author(
        self, author_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep
    ) -> AuthorOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBAuthor).where(DBAuthor.author_id == author_id)
        result = await self.db.execute(query)
        db_author = result.scalar_one_or_none()
        if not db_author:
            raise HTTPException(status_code=404, detail="Author not found")
        author_out = AuthorOut.model_validate(db_author)
        await self.db.delete(db_author)
        await self.db.commit()
        return author_out