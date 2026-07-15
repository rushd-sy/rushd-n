from ast import List
from datetime import datetime
from typing_extensions import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from models import Author, AuthorCreate, AuthorOut, BookCreate, Book, BookOut, LoanCreate, LoanOut, Loan
from storage import load_authors, load_books, load_loans, save_authors, save_books, save_loans

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "running"}

@app.get("/books", response_model=dict)
async def get_books(
    author: str | None = None,
    genre: str | None = None,
    min_year: int | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10
):
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
async def get_book(book_id: Annotated[int, Path(gt=0)]):
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return BookOut(**book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=BookOut)
async def create_book(book: BookCreate):
    books = load_books()    
    created_at = datetime.now().isoformat()
    new_book = Book(book_id=max([stored_book["book_id"] for stored_book in books], default=0) + 1, **book.model_dump(), created_at=created_at)
    books.append(new_book.model_dump())
    save_books(books)
    return BookOut(**new_book.model_dump())

@app.put("/books/{book_id}", response_model=BookOut)
async def update_book(book_id: Annotated[int, Path(gt=0)], book: BookCreate):
    books = load_books()
    for i, b in enumerate(books):
        if b["book_id"] == book_id:
            updated_book = Book(book_id=book_id, **book.model_dump(), created_at=b["created_at"])
            books[i] = updated_book.model_dump()
            save_books(books)
            return BookOut(**books[i])
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=BookOut)
async def delete_book(book_id: Annotated[int, Path(gt=0)]):
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
    loans = load_loans()
    return [LoanOut(**loan) for loan in loans]

@app.post("/loans", response_model=LoanOut)
async def create_loan(loan: LoanCreate):
    loans = load_loans()    
    created_at = datetime.now().isoformat()
    new_loan = Loan(loan_id=max([loan["loan_id"] for loan in loans], default=0) + 1, **loan.model_dump(), loan_date=created_at)
    loans.append(new_loan.model_dump())
    save_loans(loans)
    return LoanOut(**new_loan.model_dump())
    

@app.delete("/loans/{loan_id}", response_model=LoanOut)
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]):
    loans = load_loans()
    for i, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            deleted_loan = LoanOut(**loans[i])
            loans.pop(i)
            save_loans(loans)
            return deleted_loan
    raise HTTPException(status_code=404, detail="Loan not found")

@app.get("/loans/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: Annotated[int, Path(gt=0)]):
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanOut(**loan)
    raise HTTPException(status_code=404, detail="Loan not found")

@app.put("/loans/{loan_id}", response_model=LoanOut)
async def update_loan(loan_id: Annotated[int, Path(gt=0)], loan: LoanCreate):
    loans = load_loans()
    for i, l in enumerate(loans):
        if l["loan_id"] == loan_id:
            updated_loan = Loan(loan_id=loan_id, **loan.model_dump(), loan_date=l["loan_date"])
            loans[i] = updated_loan.model_dump()
            save_loans(loans)
            return LoanOut(**loans[i])
    raise HTTPException(status_code=404, detail="Loan not found")

@app.post("/authors", response_model=AuthorOut)
async def create_author(author: AuthorCreate):
    authors = load_authors()
    created_at = datetime.now().isoformat()
    new_author = Author(author_id=max([author["author_id"] for author in authors], default=0) + 1, **author.model_dump(), books=[], created_at=created_at)
    authors.append(new_author.model_dump())
    save_authors(authors)
    return AuthorOut(**new_author.model_dump())

@app.get("/authors", response_model=list[AuthorOut])
async def get_authors():
    authors = load_authors()
    return [AuthorOut(**author) for author in authors]

@app.get("/authors/{author_id}", response_model=AuthorOut)
async def get_author(author_id: Annotated[int, Path(gt=0)]):
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return AuthorOut(**author)
    raise HTTPException(status_code=404, detail="Author not found")

@app.put("/authors/{author_id}", response_model=AuthorOut)
async def update_author(author_id: Annotated[int, Path(gt=0)], author: AuthorCreate):
    authors = load_authors()
    for i, a in enumerate(authors):
        if a["author_id"] == author_id:
            updated_author = Author(author_id=author_id, **author.model_dump(), created_at=a["created_at"])
            authors[i] = updated_author.model_dump()
            save_authors(authors)
            return AuthorOut(**authors[i])
    raise HTTPException(status_code=404, detail="Author not found")