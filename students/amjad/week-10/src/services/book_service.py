import asyncio

from fastapi import HTTPException, BackgroundTasks

from datetime import datetime
from models import BookCreate, BookOut, Page
from db.db_models import Book as DBBook
from dependency import CommonsDepForPagination, CurrentUserDep, CommonsDepForDB
from exceptions import BookNotFoundError
from sqlalchemy import select, func
import logging 

class BookService:
    def __init__(self, db: CommonsDepForDB) -> None:
        self.db = db

    async def send_email_task(self, book: BookOut) -> None:
        await asyncio.sleep(2)
        logging.info(f"Sending email for book: {book.title}")

    async def get_by_id(self, book_id: int) -> BookOut:
        query = select(DBBook).where(DBBook.book_id == book_id)
        result = await self.db.execute(query)
        db_book = result.scalar_one_or_none()

        if not db_book:
            raise BookNotFoundError(book_id=book_id) 

        return BookOut.model_validate(db_book)

    async def list(
        self,
        common: CommonsDepForPagination,
        author_id: int | None = None,
        genre: str | None = None,
        min_year: int | None = None,
    ) -> Page[BookOut]:
        offset = common.offset
        limit = common.limit
        query = select(DBBook)
        if author_id is not None:
            query = query.where(DBBook.author_id == author_id)
        if genre is not None:
            query = query.where(DBBook.genre == genre)
        if min_year is not None:
            query = query.where(DBBook.year >= min_year)
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()
        result = await self.db.execute(query.order_by(DBBook.book_id).offset(offset).limit(limit))
        db_books = result.scalars().all()
        books_out = [BookOut.model_validate(book) for book in db_books]
        return Page[BookOut](items=books_out, total=total, offset=offset, limit=limit)

    async def create(
        self,
        book: BookCreate,
        user_id: CurrentUserDep,
        background_tasks: BackgroundTasks,
    ) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        new_book = DBBook(
            title=book.title,
            author_id=book.author_id,
            genre=book.genre,
            year=book.year,
            created_at=datetime.now(),
        )
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        background_tasks.add_task(self.send_email_task, BookOut.model_validate(new_book))
        return BookOut.model_validate(new_book)

    async def update(
        self, book_id: int, book: BookCreate, user_id: CurrentUserDep
    ) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBBook).where(DBBook.book_id == book_id)
        result = await self.db.execute(query)
        db_book = result.scalar_one_or_none()
        if not db_book:
            raise BookNotFoundError(book_id=book_id)
        db_book.title = book.title
        db_book.author_id = book.author_id
        db_book.genre = book.genre
        db_book.year = book.year
        await self.db.commit()
        await self.db.refresh(db_book)
        return BookOut.model_validate(db_book)

    async def delete(self, book_id: int, user_id: CurrentUserDep) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBBook).where(DBBook.book_id == book_id)
        result = await self.db.execute(query)
        db_book = result.scalar_one_or_none()
        if not db_book:
            raise BookNotFoundError(book_id=book_id)
        book_out = BookOut.model_validate(db_book)
        await self.db.delete(db_book)
        await self.db.commit()
        return book_out
