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
        limit : Annotated[int, Query(ge=1)] = 10,
    ) -> Page[BookResponse]:
    """
        A cool docstring
    """
    
    books = load_books()
    books_out = []
    for book in books: 
        if author and book["author"] != author:
            continue
        if genre and book["genre"] != genre:
            continue
        if min_publish_year and book["publish_year"] < min_publish_year:
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
async def get_book(book_id: Annotated[int, Path(gt=1)]) -> BookResponse:
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return BookResponse(
                book_id=book["book_id"],
                title=book["title"],   
                author=book["author"],
                genre=book["genre"],
                publish_year=book["publish_year"],
            )
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
async def update_book(book_id: int, request_book: BookCreate) -> BookResponse:
    books = load_books()
    
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            UpdatedBook = BookModel ( # I have a question about this part
                book_id=book_id,
                **request_book.model_dump(),
                creation_date=book["creation_date"],
            )
            
            books[index] = UpdatedBook.model_dump()
            save_books(books)
            
            return BookResponse(
                **UpdatedBook.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    books = load_books()
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            del books[index]
            save_books(books)
            return {"message": "Book deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Book not found")




@app.get("/authors")
async def get_authors(
        name: str | None = None,
        min_birth_year: int | None = None,
        max_birth_year: int | None = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1)] = 10,
    ) -> Page[AuthorResponse]:
    authors = load_authors()
    authors_out = []
    
    for author in authors:
        if name and author["name"] != name:
            continue
        if min_birth_year and author["birth_year"] < min_birth_year:
            continue
        if max_birth_year and author["birth_year"] > max_birth_year:
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
async def get_author(author_id: Annotated[int, Path(gt=0)]) -> AuthorResponse:
    """
    Get a specific author by ID.
    
    - **author_id**: ID of the author (must be greater than 0)
    """
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorResponse(
                author_id=author["author_id"],
                name=author["name"],
                birth_year=author["birth_year"],
            )
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/authors", response_model=AuthorResponse)
async def create_author(request_author: AuthorCreate) -> AuthorResponse:
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
) -> AuthorResponse:
    authors = load_authors()
    
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            updated_author = AuthorModel(
                author_id=author_id,
                **request_author.model_dump(),
                added_at=author["added_at"], 
            )
            
            authors[index] = updated_author.model_dump()
            save_authors(authors)
            
            return AuthorResponse(
                **updated_author.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Author not found")


@app.delete("/authors/{author_id}")
async def delete_author(author_id: Annotated[int, Path(gt=0)]) -> dict:
    authors = load_authors()
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            del authors[index]
            save_authors(authors)
            return {"message": "Author deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Author not found")

@app.get("/loans")
async def get_loans(
    name: str | None = None,
    date: str | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1)] = 10,
) -> Page[LoanResponse]:
    loans = load_loans()
    loans_out = []
    
    for loan in loans:
        if name and loan["name"] != name:
            continue
        if date and loan["date"] != date:
            continue
        if min_date and loan["date"] < min_date:
            continue
        if max_date and loan["date"] > max_date:
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
async def get_loan(loan_id: Annotated[int, Path(gt=0)]) -> LoanResponse:
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanResponse(
                loan_id=loan["loan_id"],
                date=loan["date"],
            )
    raise HTTPException(status_code=404, detail="Loan not found")


@app.post("/loans", response_model=LoanResponse)
async def create_loan(request_loan: LoanCreate) -> LoanResponse:
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
) -> LoanResponse:
    loans = load_loans()
    
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            updated_loan = LoanModel(
                loan_id=loan_id,
                **request_loan.model_dump(),
                added_at=loan["added_at"],
            )
            
            loans[index] = updated_loan.model_dump()
            save_loans(loans)
            
            return LoanResponse(
                **updated_loan.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Loan not found")


@app.delete("/loans/{loan_id}")
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]) -> dict:
    loans = load_loans()
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            del loans[index]
            save_loans(loans)
            return {"message": "Loan deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Loan not found")
