from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.books import Book
from database.models.authors import Author
from database.models.loans import Loan
from models.books import BookCreate, BookResponse
from models.page import Page
from exceptions import AuthorNotFoundError, BookNotFoundError, BookHasLoansError

class BookServices:

    async def get_books (        
        self,
        db: AsyncSession,
        author_id : int | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
        max_publish_year : int | None = None,
        offset: int = 0,
        limit: int = 20
    ) -> Page[BookResponse]:
        
        conditions = []
        
        if author_id is not None:
            conditions.append(Book.author.has(Author.author_id == author_id))
    
        if genre is not None:
            conditions.append(Book.genre == genre)

        if min_publish_year is not None:
            conditions.append(Book.publish_year >= min_publish_year)
            
        if max_publish_year is not None:
            conditions.append(Book.publish_year <= max_publish_year)
            
        
        total = await db.scalar (
            select(func.count(Book.book_id)).select_from(Book).where(*conditions)
        )

        result = await db.scalars (
            select(Book)
            .where(*conditions)
            .order_by(Book.book_id)
            .offset(offset)
            .limit(limit)
        )
        
        books = result.all()

        return Page[BookResponse] (
            items=[
                BookResponse.model_validate(book) for book in books
            ],
            total=total or 0,
            offset=offset,
            limit=limit,
        )

    async def get_book_by_id (
        self,
        db: AsyncSession,
        book_id: int
    ) -> BookResponse:
        
        book = await db.scalar(select(Book).options(selectinload(Book.author)).where(Book.book_id==book_id))
        
        if book is None:
            raise BookNotFoundError(book_id)
        
        return BookResponse.model_validate(book)
    
    async def create_book (
        self,
        db: AsyncSession,
        request_book: BookCreate
    ) -> BookResponse:
        
        author = await db.get(Author, request_book.author_id)
        
        if author is None:
            raise AuthorNotFoundError(request_book.author_id)
    
        new = Book (
            title=request_book.title,
            author_id=request_book.author_id,
            genre=request_book.genre,
            publish_year=request_book.publish_year
        )
        
        db.add(new)
        
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise Exception
        
        await db.refresh(new)
        
        return BookResponse.model_validate(new)

    async def delete_book(
        self,
        db: AsyncSession,
        book_id: int) -> BookResponse:
        
        book = await db.get(Book, book_id)

        if book is None:
            raise BookNotFoundError(book_id)
        
        loan = await db.scalar(
            select(Loan.loan_id)
            .where(Loan.book_id == book_id)
            .limit(1)
        )
        
        if loan is not None:
            raise BookHasLoansError(book_id)
        
        response = BookResponse.model_validate(book)
        
        try:
            await db.delete(book)
            await db.commit()
        except Exception:
            await db.rollback()
            raise 
        
        return response
    
    async def update_book(
        self,
        db: AsyncSession,
        book_id: int,
        request_book: BookCreate
    ) -> BookResponse:

        book = await db.scalar(select(Book).where(Book.book_id == book_id))

        if book is None:
            raise BookNotFoundError(book_id)
        
        author = await db.get(Author, request_book.author_id)
        
        if author is None:
            raise AuthorNotFoundError(book.author_id)
        
        book.title = request_book.title
        book.author_id = request_book.author_id
        book.genre = request_book.genre
        book.publish_year = request_book.publish_year
        
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise 
        
        await db.refresh(book)
        
        return BookResponse.model_validate(book)
