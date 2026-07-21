from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Path
from models import book_create, book_model, book_response, author_create, author_model, author_response, loan_create, loan_model, loan_response
from storage import load_books, save_books, load_authors, save_authors, load_loans, save_loans

app = FastAPI()


@app.get("/books")
async def get_books(
        author : str | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
        offset : Annotated[int, Query(ge=0)] = 0,
        limit : Annotated[int, Query(ge=1)] = 10,
    ) -> list[dict]:
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
    books_out = books_out[offset:offset + limit]
    return books_out


@app.get("/books/{book_id}", response_model=book_response)
async def get_book(book_id: Annotated[int, Path(gt=1)]) -> book_response:
    books = load_books()
    for book in books:
        if book["book_id"] == book_id:
            return book_response(
                book_id=book["book_id"],
                title=book["title"],   
                author=book["author"],
                genre=book["genre"],
                publish_year=book["publish_year"],
            )
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=book_response)
async def create_book(request_book: book_create) -> book_response:
    books = load_books()

    created_book = book_model(
        book_id=max([book["book_id"] for book in books], default=0) + 1,
        **request_book.model_dump(),
        creation_date=datetime.now().isoformat(),
    )
    books.append(created_book.model_dump())
    save_books(books)

    respond = book_response(
        **created_book.model_dump(),
    )

    return respond

@app.put("/books/{book_id}", response_model=book_response)
async def update_book(book_id: int, request_book: book_create) -> book_response:
    books = load_books()
    
    for index, book in enumerate(books):
        if book["book_id"] == book_id:
            UpdatedBook = book_model ( # I have a question about this part
                book_id=book_id,
                **request_book.model_dump(),
                creation_date=book["creation_date"],
            )
            
            books[index] = UpdatedBook.model_dump()
            save_books(books)
            
            return book_response(
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
    ) -> list[dict]:
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
    
    authors_out = authors_out[offset:offset + limit]
    return authors_out

@app.get("/authors/{author_id}", response_model=author_response)
async def get_author(author_id: Annotated[int, Path(gt=0)]) -> author_response:
    """
    Get a specific author by ID.
    
    - **author_id**: ID of the author (must be greater than 0)
    """
    authors = load_authors()
    for author in authors:
        if author["author_id"] == author_id:
            return author_response(
                author_id=author["author_id"],
                name=author["name"],
                birth_year=author["birth_year"],
            )
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/authors", response_model=author_response)
async def create_author(request_author: author_create) -> author_response:
    authors = load_authors()

    created_author = author_model(
        author_id=max([author["author_id"] for author in authors], default=0) + 1,
        **request_author.model_dump(),
        added_at=datetime.now().isoformat(),
    )
    authors.append(created_author.model_dump())
    save_authors(authors)

    return author_response(
        **created_author.model_dump(),
    )
    
    
    
@app.put("/authors/{author_id}", response_model=author_response)
async def update_author(
    author_id: Annotated[int, Path(gt=0)],
    request_author: author_create
) -> author_response:
    authors = load_authors()
    
    for index, author in enumerate(authors):
        if author["author_id"] == author_id:
            updated_author = author_model(
                author_id=author_id,
                **request_author.model_dump(),
                added_at=author["added_at"], 
            )
            
            authors[index] = updated_author.model_dump()
            save_authors(authors)
            
            return author_response(
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
) -> list[dict]:
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
    
    loans_out = loans_out[offset:offset + limit]
    return loans_out


@app.get("/loans/{loan_id}", response_model=loan_response)
async def get_loan(loan_id: Annotated[int, Path(gt=0)]) -> loan_response:
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return loan_response(
                loan_id=loan["loan_id"],
                date=loan["date"],
            )
    raise HTTPException(status_code=404, detail="Loan not found")


@app.post("/loans", response_model=loan_response)
async def create_loan(request_loan: loan_create) -> loan_response:
    loans = load_loans()

    created_loan = loan_model(
        loan_id=max([loan["loan_id"] for loan in loans], default=0) + 1,
        **request_loan.model_dump(),
        added_at=datetime.now().isoformat(),
    )
    loans.append(created_loan.model_dump())
    save_loans(loans)

    return loan_response(
        **created_loan.model_dump(),
    )


@app.put("/loans/{loan_id}", response_model=loan_response)
async def update_loan(
    loan_id: Annotated[int, Path(gt=0)],
    request_loan: loan_create
) -> loan_response:
    loans = load_loans()
    
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            updated_loan = loan_model(
                loan_id=loan_id,
                **request_loan.model_dump(),
                added_at=loan["added_at"],
            )
            
            loans[index] = updated_loan.model_dump()
            save_loans(loans)
            
            return loan_response(
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
