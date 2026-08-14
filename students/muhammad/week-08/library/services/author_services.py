from datetime import date

from models.authors import AuthorModel, AuthorCreate, AuthorResponse
from models.page import Page
from utils.storage import load_authors, save_authors
from exceptions import AuthorNotFoundError


class AuthorServices:

    @staticmethod
    async def _load_authors() -> list[AuthorModel]:
        return await load_authors()

    @staticmethod
    async def _save_authors(authors: list[AuthorModel]) -> None:
        await save_authors(authors)

    async def get_authors(
        self,
        name: str | None = None,
        min_birth_year: int | None = None,
        max_birth_year: int | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> Page[AuthorResponse]:
        authors = await AuthorServices._load_authors()
        authors_out = []

        for author_model in authors:
            author = AuthorResponse(**author_model.model_dump())
            
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

    async def get_author_by_id(
        self,
        author_id: int
    ) -> AuthorResponse:
        authors = await AuthorServices._load_authors()
        for author in authors:
            if author.author_id == author_id:
                return AuthorResponse(**author.model_dump())
        raise AuthorNotFoundError(author_id)

    async def create_author(
        self,
        request_author: AuthorCreate
    ) -> AuthorResponse:

        authors = await AuthorServices._load_authors()
        created_author = AuthorModel(
            author_id=max(
                [author.author_id for author in authors],
                default=0
            ) + 1,
            **request_author.model_dump(),
            added_at=date.today()
        )

        authors.append(created_author)
        await AuthorServices._save_authors(authors)
        return AuthorResponse(**created_author.model_dump())

    async def update_author(
        self,
        author_id: int,
        request_author: AuthorCreate
    ) -> AuthorResponse:

        authors = await AuthorServices._load_authors()
        for index, author in enumerate(authors):
            if author.author_id == author_id:
                updated_author = AuthorModel(
                    author_id=author_id,
                    **request_author.model_dump(),
                    added_at=author.added_at
                )
                authors[index] = updated_author
                await AuthorServices._save_authors(authors)
                return AuthorResponse(**updated_author.model_dump())
        raise AuthorNotFoundError(author_id)

    async def delete_author(
        self,
        author_id: int
    ) -> AuthorResponse:

        authors = await AuthorServices._load_authors()
        for index, author in enumerate(authors):
            if author.author_id == author_id:
                del authors[index]
                await AuthorServices._save_authors(authors)
                return AuthorResponse(**author.model_dump())

        raise AuthorNotFoundError(author_id)
