
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.authors import Author
from database.models.books import Book
from models.authors import AuthorCreate, AuthorResponse
from models.page import Page
from exceptions import AuthorNotFoundError, AuthorHasBookError



class AuthorServices:

    async def get_authors(
        self,
        db: AsyncSession,
        name: str | None = None,
        min_birth_year: int | None = None,
        max_birth_year: int | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> Page[AuthorResponse]:

        conditions = []

        if name is not None:
            conditions.append(Author.name == name)

        if min_birth_year is not None:
            conditions.append(Author.birth_year >= min_birth_year)

        if max_birth_year is not None:
            conditions.append(Author.birth_year <= max_birth_year)

        total = await db.scalar(
            select(func.count(Author.author_id))
            .where(*conditions)
        )

        result = await db.scalars(
            select(Author)
            .where(*conditions)
            .order_by(Author.author_id)
            .offset(offset)
            .limit(limit)
        )

        authors = result.all()

        return Page[AuthorResponse](
            items=[
                AuthorResponse.model_validate(author)
                for author in authors
            ],
            total=total or 0,
            offset=offset,
            limit=limit
        )

    async def get_author_by_id(
        self,
        db: AsyncSession,
        author_id: int
    ) -> AuthorResponse:

        author = await db.get(Author, author_id)

        if author is None:
            raise AuthorNotFoundError(author_id)

        return AuthorResponse.model_validate(author)

    async def create_author(
        self,
        db: AsyncSession,
        request_author: AuthorCreate
    ) -> AuthorResponse:

        new_author = Author(
            name=request_author.name,
            birth_year=request_author.birth_year
        )

        db.add(new_author)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        await db.refresh(new_author)

        return AuthorResponse.model_validate(new_author)

    async def update_author(
        self,
        db: AsyncSession,
        author_id: int,
        request_author: AuthorCreate
    ) -> AuthorResponse:

        author = await db.get(Author, author_id)

        if author is None:
            raise AuthorNotFoundError(author_id)

        author.name = request_author.name
        author.birth_year = request_author.birth_year

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        await db.refresh(author)

        return AuthorResponse.model_validate(author)

    async def delete_author(
        self,
        db: AsyncSession,
        author_id: int
    ) -> AuthorResponse:

        author = await db.get(Author, author_id)

        if author is None:
            raise AuthorNotFoundError(author_id)

        existing_book = await db.scalar(
            select(Book.book_id)
            .where(Book.author_id == author_id)
            .limit(1)
        )

        if existing_book is not None:
            raise AuthorHasBookError(author_id)

        response = AuthorResponse.model_validate(author)

        try:
            await db.delete(author)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return response
