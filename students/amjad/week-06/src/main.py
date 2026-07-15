from datetime import datetime
from typing_extensions import Annotated

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
    books = load_books()
    books_out = []
    for book in books[offset:offset + limit]:
        if author and book["author"] != author:
            continue
        if genre and book["genre"] != genre:
            continue
        if min_year and book["year"] < min_year:
            continue
        books_out.append(BookOut(**book))
    return {"books": books_out}

@app.get("/books/{book_id}")
async def get_book(book_id: Annotated[int, Path(gt=0)]):
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return {"book": BookOut(**book)}
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books")
async def create_book(book: BookCreate):
    books = load_books()    
    created_at = datetime.now().isoformat()
    new_book = Book(book_id=max([book["book_id"] for book in books], default=0) + 1, **book.model_dump(), created_at=created_at)
    books.append(new_book.model_dump())
    save_books(books)
    return {"message": "Book created", "book": BookOut(**new_book.model_dump())}

@app.put("/books/{book_id}")
async def update_book(book_id: Annotated[int, Path(gt=0)], book: BookCreate):
    books = load_books()
    for i, b in enumerate(books):
        if b["book_id"] == book_id:
            updated_book = Book(book_id=book_id, **book.model_dump(), created_at=b["created_at"])
            books[i] = updated_book.model_dump()
            save_books(books)
            return {"message": "Book updated", "book": BookOut(**books[i])}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: Annotated[int, Path(gt=0)]):
    books = load_books()
    books = [book for book in books if book["book_id"] != book_id]
    save_books(books)
    return {"message": "Book deleted", "book_id": book_id}

@app.get("/loans")
async def get_loans():
    loans = load_loans()
    return {"loans": [LoanOut(**loan) for loan in loans]}

@app.post("/loans")
async def create_loan(loan: LoanCreate):
    loans = load_loans()    
    created_at = datetime.now().isoformat()
    new_loan = Loan(loan_id=max([loan["loan_id"] for loan in loans], default=0) + 1, **loan.model_dump(), loan_date=created_at)
    loans.append(new_loan.model_dump())
    save_loans(loans)
    return {"message": "loan created", "loan": LoanOut(**new_loan.model_dump())}
    

@app.delete("/loans/{loan_id}")
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]):
    loans = load_loans()
    loans = [loan for loan in loans if loan["loan_id"] != loan_id]
    save_loans(loans)
    return {"message": "Loan deleted", "loan_id": loan_id}

@app.get("/loans/{loan_id}")
async def get_loan(loan_id: Annotated[int, Path(gt=0)]):
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return {"loan": LoanOut(**loan)}
    raise HTTPException(status_code=404, detail="Loan not found")

@app.put("/loans/{loan_id}")
async def update_loan(loan_id: Annotated[int, Path(gt=0)], loan: LoanCreate):
    loans = load_loans()
    for i, l in enumerate(loans):
        if l["loan_id"] == loan_id:
            updated_loan = Loan(loan_id=loan_id, **loan.model_dump(), loan_date=l["loan_date"])
            loans[i] = updated_loan.model_dump()
            save_loans(loans)
            return {"message": "Loan updated", "loan": LoanOut(**loans[i])}
    raise HTTPException(status_code=404, detail="Loan not found")

@app.post("/authors")
async def create_author(author: AuthorCreate):
    authors = load_authors()
    created_at = datetime.now().isoformat()
    new_author = Author(author_id=max([author["author_id"] for author in authors], default=0) + 1, **author.model_dump(), books=[], created_at=created_at)
    authors.append(new_author.model_dump())
    save_authors(authors)
    return {"message": "Author created", "author": AuthorOut(**new_author.model_dump())}

@app.get("/authors")
async def get_authors():
    authors = load_authors()
    return {"authors": [AuthorOut(**author) for author in authors]}

@app.get("/authors/{author_id}")
async def get_author(author_id: Annotated[int, Path(gt=0)]):
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return {"author": AuthorOut(**author)}
    raise HTTPException(status_code=404, detail="Author not found")

@app.put("/authors/{author_id}")
async def update_author(author_id: Annotated[int, Path(gt=0)], author: AuthorCreate):
    authors = load_authors()
    for i, a in enumerate(authors):
        if a["author_id"] == author_id:
            updated_author = Author(author_id=author_id, **author.model_dump(), created_at=a["created_at"])
            authors[i] = updated_author.model_dump()
            save_authors(authors)
            return {"message": "Author updated", "author": AuthorOut(**authors[i])}
    raise HTTPException(status_code=404, detail="Author not found")