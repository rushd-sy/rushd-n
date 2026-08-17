from datetime import date

from models.books import BookCreate, BookModel, BookResponse
from models.page import Page
from utils.storage import load_books, save_books
from exceptions import BookNotFoundError

class BookServices:

    async def get_books (        
        self,
        author : str | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> Page[BookResponse]:
        
        books = await load_books()
        books_out = []
        
        for book_model in books:
            if author and book_model.author != author:
                continue
            if genre and book_model.genre != genre:
                continue
            if min_publish_year and book_model.publish_year < min_publish_year:
                continue
            
            book = BookResponse(**book_model.model_dump())
            books_out.append(book)
        
        total = len(books_out)
        books_out = books_out[offset:offset + limit]
        
        return Page[BookResponse](
            items=books_out,
            total=total,
            offset=offset,
            limit=limit
        )
    
    async def get_book_by_id (
        self,
        book_id: int
    ) -> BookResponse:
        
        books = await load_books()
        
        for book in books:
            if book.book_id == book_id:
                return BookResponse(**book.model_dump())
        
        raise BookNotFoundError(book_id)
    
    async def create_book (
        self,
        request_book: BookCreate
    ) -> BookResponse:
        
        books = await load_books()
        
        created_book = BookModel(
        book_id=max([book.book_id for book in books], default=0) + 1,
            **request_book.model_dump(),
            creation_date=date.today(),
        )
        books.append(created_book)
        await save_books(books)
        respond = BookResponse(**created_book.model_dump())
        return respond

    async def delete_book(self, book_id: int) -> BookResponse:
        books = await load_books()
        for index, book in enumerate(books):
            if book.book_id == book_id:
                del books[index]
                await save_books(books)
                return BookResponse(**book.model_dump())
        
        raise BookNotFoundError(book_id)
    
    async def update_book(self, book_id: int, request_book: BookCreate) -> BookResponse:
        books = await load_books()
    
        for index, book in enumerate(books):
            if book.book_id == book_id:
                UpdatedBook = BookModel (
                    book_id=book_id,
                    **request_book.model_dump(),
                    creation_date=book.creation_date,
                )
                
                books[index] = UpdatedBook
                await save_books(books)
                return BookResponse(**UpdatedBook.model_dump())
        
        raise BookNotFoundError(book_id)
