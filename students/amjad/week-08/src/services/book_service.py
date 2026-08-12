import asyncio

from fastapi import Depends, HTTPException, BackgroundTasks

from datetime import datetime
from models import BookCreate, Book, BookOut, Page
from storage import load_books, save_books
from dependency import CommonsDepForPagination, CurrentUserDep
from exceptions import BookNotFoundError
import logging

class BookService:
    
    async def send_email_task(self, book: BookOut) -> None:
        await asyncio.sleep(2) 
        logging.info(f"Sending email for book: {book.title}")

    async def get_by_id(self, book_id: int) -> BookOut:
        books = await load_books()
        for book in books:
            if book["book_id"] == book_id:
                return BookOut(**book)
        raise BookNotFoundError(book_id=book_id)

    async def list(
        self, 
        common: CommonsDepForPagination,
        author: str | None = None, 
        genre: str | None = None, 
        min_year: int | None = None, 
    ) -> Page[BookOut]:
        books = await load_books()
        books_out = []
        for book in books:
            if author and book["author"] != author:
                continue
            if genre and book["genre"] != genre:
                continue
            if min_year and book["year"] < min_year:
                continue
            books_out.append(BookOut(**book))
        
        total = len(books_out)
        offset = common["offset"]
        limit = common["limit"]
        books_out = books_out[offset:offset + limit]
        return Page[BookOut](items=books_out, total=total, offset=offset, limit=limit)

    async def create(self, book: BookCreate, user_id: CurrentUserDep, background_tasks: BackgroundTasks) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        books = await load_books()    
        created_at = datetime.now().isoformat()
        new_book = Book(book_id=max([stored_book["book_id"] for stored_book in books], default=0) + 1, **book.model_dump(), created_at=created_at)
        books.append(new_book.model_dump())
        await save_books(books)
        background_tasks.add_task(self.send_email_task, BookOut(**new_book.model_dump()))
        return BookOut(**new_book.model_dump())

    async def update(self, book_id: int, book: BookCreate, user_id: CurrentUserDep) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        books = await load_books()
        for i, b in enumerate(books):
            if b["book_id"] == book_id:
                updated_book = Book(book_id=book_id, **book.model_dump(), created_at=b["created_at"])
                books[i] = updated_book.model_dump()
                await save_books(books)
                return BookOut(**books[i])
        raise BookNotFoundError(book_id=book_id)

    async def delete(self, book_id: int, user_id: CurrentUserDep) -> BookOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        books = await load_books()
        for i, book in enumerate(books):
            if book["book_id"] == book_id:
                deleted_book = BookOut(**books[i])
                books.pop(i)
                await save_books(books)
                return deleted_book
        raise BookNotFoundError(book_id=book_id)