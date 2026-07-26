from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Path
from models import Page, BookCreate, BookModel, BookResponse, AuthorCreate, AuthorModel, AuthorResponse, LoanCreate, LoanModel, LoanResponse
from storage import load_books, save_books, load_authors, save_authors, load_loans, save_loans

app = FastAPI()


@app.get("/books")
async def get_books(
        author : str | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
        offset : Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=20)] = 10,
    ) -> Page[BookResponse]:
    """
        A cool docstring
    """
    
    books = load_books()
    books_out = []
    for dict_book in books:
        book = BookResponse(**dict_book) 
        if author and book.author != author:
            continue
        if genre and book.genre != genre:
            continue
        if min_publish_year and book.publish_year < min_publish_year:
            continue
        books_out.append(book)
    
    total = len(books_out)
    books_out = books_out[offset:offset + limit]
    
    return Page[BookResponse](
        items=books_out,
        total=total,
        offset=offset,
        limit=limit
    )

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: Annotated[int, Path(gt=0)]) -> BookResponse:
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return BookResponse( **book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=BookResponse)
async def create_book(request_book: BookCreate) -> BookResponse:
    books = load_books()

    created_book = BookModel(
        book_id=max([book["book_id"] for book in books], default=0) + 1,
        **request_book.model_dump(),
        creation_date=datetime.now().isoformat(),
    )
    books.append(created_book.model_dump())
    save_books(books)

    respond = BookResponse(
        **created_book.model_dump(),
    )

    return respond

@app.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: Annotated[int, Path(gt=0)], request_book: BookCreate) -> BookResponse:
    books = load_books()
    
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            existing = BookModel(**book)
            UpdatedBook = BookModel (
                book_id=book_id,
                **request_book.model_dump(),
                creation_date=existing.creation_date,
            )
            
            books[index] = UpdatedBook.model_dump()
            save_books(books)
            
            return BookResponse(
                **UpdatedBook.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: Annotated[int, Path(gt=0)]) -> None:
    books = load_books()
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            del books[index]
            save_books(books)
            return
    
    raise HTTPException(status_code=404, detail="Book not found")




@app.get("/authors")
async def get_authors(
        name: str | None = None,
        min_birth_year: int | None = None,
        max_birth_year: int | None = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=20)] = 10,
    ) -> Page[AuthorResponse]:
    authors = load_authors()
    authors_out = []
    
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

@app.get("/authors/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: Annotated[int, Path(gt=0)]):
    """
    Get a specific author by ID.
    
    - **author_id**: ID of the author (must be greater than 0)
    """
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorResponse(**author)
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/authors", response_model=AuthorResponse)
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
    
    
    
@app.put("/authors/{author_id}", response_model=AuthorResponse)
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
    
    raise HTTPException(status_code=404, detail="Author not found")


@app.delete("/authors/{author_id}")
async def delete_author(author_id: Annotated[int, Path(gt=0)]) -> None:
    authors = load_authors()
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            del authors[index]
            save_authors(authors)
            return
    
    raise HTTPException(status_code=404, detail="Author not found")

@app.get("/loans")
async def get_loans(
    name: str | None = None,
    date: str | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10,
    ) -> Page[LoanResponse]:
    loans = load_loans()
    loans_out = []
    
    for dict_loan in loans:
        loan = LoanResponse(**dict_loan)
        if name and loan.name != name:
            continue
        if date and loan.date != date:
            continue
        if min_date and loan.date < min_date:
            continue
        if max_date and loan.date > max_date:
            continue
        loans_out.append(loan)
    
    total = len(loans_out)
    loans_out = loans_out[offset:offset + limit]
    
    return Page[LoanResponse](
        items=loans_out,
        total=total,
        offset=offset,
        limit=limit
    )


@app.get("/loans/{loan_id}", response_model=LoanResponse)
async def get_loan(loan_id: Annotated[int, Path(gt=0)]):
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanResponse(**loan)
    raise HTTPException(status_code=404, detail="Loan not found")


@app.post("/loans", response_model=LoanResponse)
async def create_loan(request_loan: LoanCreate):
    loans = load_loans()

    created_loan = LoanModel(
        loan_id=max([loan["loan_id"] for loan in loans], default=0) + 1,
        **request_loan.model_dump(),
        added_at=datetime.now().isoformat(),
    )
    loans.append(created_loan.model_dump())
    save_loans(loans)

    return LoanResponse(
        **created_loan.model_dump(),
    )


@app.put("/loans/{loan_id}", response_model=LoanResponse)
async def update_loan(
    loan_id: Annotated[int, Path(gt=0)],
    request_loan: LoanCreate
    ):
    loans = load_loans()
    
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            existing = LoanModel(**loan)
            updated_loan = LoanModel(
                loan_id=loan_id,
                **request_loan.model_dump(),
                added_at=existing.added_at,
            )
            
            loans[index] = updated_loan.model_dump()
            save_loans(loans)
            
            return LoanResponse(
                **updated_loan.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Loan not found")


@app.delete("/loans/{loan_id}")
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]) -> None:
    loans = load_loans()
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            del loans[index]
            save_loans(loans)
            return
    
    raise HTTPException(status_code=404, detail="Loan not found")
