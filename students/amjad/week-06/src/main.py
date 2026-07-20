from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from models import Author, AuthorCreate, AuthorOut, BookCreate, Book, BookOut, LoanCreate, LoanOut, Loan
from storage import load_authors, load_books, load_loans, save_authors, save_books, save_loans

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "running"}

@app.get("/books")
async def get_books(
    author: str | None = None,
    genre: str | None = None,
    min_year: int | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10
):
    """
    Retrieve a list of books with optional filters.
    - **author**: Filter books by author name.
    - **genre**: Filter books by genre.
    - **min_year**: Filter books published after a certain year.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    books = load_books()
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
    books_out = books_out[offset:offset + limit]
    return {"books": books_out, "total": total, "offset": offset, "limit": limit}

@app.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: Annotated[int, Path(gt=0)]) -> BookOut:
    """
    Retrieve a book by its ID.
    - **book_id**: The ID of the book to retrieve and must be a positive integer.
    - Returns the book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return BookOut(**book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=BookOut)
async def create_book(book: BookCreate) -> BookOut:
    """
    Create a new book.
    - **book**: The details of the book to create.
    - Returns the created book details.
    """
    books = load_books()    
    created_at = datetime.now().isoformat()
    new_book = Book(book_id=max([stored_book["book_id"] for stored_book in books], default=0) + 1, **book.model_dump(), created_at=created_at)
    books.append(new_book.model_dump())
    save_books(books)
    return BookOut(**new_book.model_dump())

@app.put("/books/{book_id}", response_model=BookOut)
async def update_book(book_id: Annotated[int, Path(gt=0)], book: BookCreate) -> BookOut:
    """
    Update an existing book.
    - **book_id**: The ID of the book to update and must be a positive integer.
    - **book**: The updated details of the book.
    - Returns the updated book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for i, b in enumerate(books):
        if b["book_id"] == book_id:
            updated_book = Book(book_id=book_id, **book.model_dump(), created_at=b["created_at"])
            books[i] = updated_book.model_dump()
            save_books(books)
            return BookOut(**books[i])
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=BookOut)
async def delete_book(book_id: Annotated[int, Path(gt=0)]) -> BookOut:
    """
    Delete a book by its ID.
    - **book_id**: The ID of the book to delete and must be a positive integer.
    - Returns the deleted book details if found, otherwise raises a 404 error.
    """
    books = load_books()
    for i, book in enumerate(books):
        if book["book_id"] == book_id:
            deleted_book = BookOut(**books[i])
            books.pop(i)
            save_books(books)
            return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/loans", response_model=list[LoanOut])
async def get_loans():
    """
    Retrieve all loans.
    - Returns a list of all loans.
    """
    loans = load_loans()
    return [LoanOut(**loan) for loan in loans]

@app.post("/loans", response_model=LoanOut)
async def create_loan(loan: LoanCreate) -> LoanOut:
    """
    Create a new loan.
    - **loan**: The details of the loan to create.
    - Returns the created loan details.
    """
    loans = load_loans()    
    created_at = datetime.now().isoformat()
    new_loan = Loan(loan_id=max([stored_loan["loan_id"] for stored_loan in loans], default=0) + 1, **loan.model_dump(), loan_date=created_at)
    loans.append(new_loan.model_dump())
    save_loans(loans)
    return LoanOut(**new_loan.model_dump())
    

@app.delete("/loans/{loan_id}", response_model=LoanOut)
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]) -> LoanOut:
    """
    Delete a loan by its ID.
    - **loan_id**: The ID of the loan to delete and must be a positive integer.
    - Returns the deleted loan details if found, otherwise raises a 404 error.
    """
    loans = load_loans()
    for i, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            deleted_loan = LoanOut(**loans[i])
            loans.pop(i)
            save_loans(loans)
            return deleted_loan
    raise HTTPException(status_code=404, detail="Loan not found")

@app.get("/loans/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: Annotated[int, Path(gt=0)]) -> LoanOut:
    """
    Retrieve a loan by its ID.
    - **loan_id**: The ID of the loan to retrieve and must be a positive integer.
    - Returns the loan details if found, otherwise raises a 404 error.
    """
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanOut(**loan)
    raise HTTPException(status_code=404, detail="Loan not found")

@app.put("/loans/{loan_id}", response_model=LoanOut)
async def update_loan(loan_id: Annotated[int, Path(gt=0)], loan: LoanCreate) -> LoanOut:
    """
    Update an existing loan.
    - **loan_id**: The ID of the loan to update and must be a positive integer.
    - **loan**: The updated details of the loan.
    - Returns the updated loan details if found, otherwise raises a 404 error.
    """
    loans = load_loans()
    for i, l in enumerate(loans):
        if l["loan_id"] == loan_id:
            updated_loan = Loan(loan_id=loan_id, **loan.model_dump(), loan_date=l["loan_date"])
            loans[i] = updated_loan.model_dump()
            save_loans(loans)
            return LoanOut(**loans[i])
    raise HTTPException(status_code=404, detail="Loan not found")

@app.post("/authors", response_model=AuthorOut)
async def create_author(author: AuthorCreate) -> AuthorOut:
    """
    Create a new author.
    - **author**: The details of the author to create.
    - Returns the created author details.
    """
    authors = load_authors()
    created_at = datetime.now().isoformat()
    new_author = Author(author_id=max([stored_author["author_id"] for stored_author in authors], default=0) + 1, **author.model_dump(), books=[], created_at=created_at)
    authors.append(new_author.model_dump())
    save_authors(authors)
    return AuthorOut(**new_author.model_dump())

@app.get("/authors", response_model=list[AuthorOut])
async def get_authors():
    """
    Retrieve all authors.
    - Returns a list of all authors.
    """
    authors = load_authors()
    return [AuthorOut(**author) for author in authors]

@app.get("/authors/{author_id}", response_model=AuthorOut)
async def get_author(author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
    """
    Retrieve an author by their ID.
    - **author_id**: The ID of the author to retrieve and must be a positive integer.
    - Returns the author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorOut(**author)
    raise HTTPException(status_code=404, detail="Author not found")

@app.put("/authors/{author_id}", response_model=AuthorOut)
async def update_author(author_id: Annotated[int, Path(gt=0)], author: AuthorCreate) -> AuthorOut:
    """
    Update an existing author.
    - **author_id**: The ID of the author to update and must be a positive integer.
    - **author**: The updated details of the author.
    - Returns the updated author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for i, a in enumerate(authors):
        if a["author_id"] == author_id:
            updated_author = Author(author_id=author_id, **author.model_dump(), created_at=a["created_at"])
            authors[i] = updated_author.model_dump()
            save_authors(authors)
            return AuthorOut(**authors[i])
    raise HTTPException(status_code=404, detail="Author not found")

@app.delete("/authors/{author_id}", response_model=AuthorOut)
async def delete_author(author_id: Annotated[int, Path(gt=0)]) -> AuthorOut:
    """
    Delete an author by their ID.
    - **author_id**: The ID of the author to delete and must be a positive integer.
    - Returns the deleted author details if found, otherwise raises a 404 error.
    """
    authors = load_authors()
    for i, author in enumerate(authors):
        if author["author_id"] == author_id:
            deleted_author = AuthorOut(**authors[i])
            authors.pop(i)
            save_authors(authors)
            return deleted_author
    raise HTTPException(status_code=404, detail="Author not found")