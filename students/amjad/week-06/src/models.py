from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int 
    offset: int | None = None
    limit: int | None = None


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int

class BookOut(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    year: int

class Book(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    year: int
    created_at: str

class Loan(BaseModel):
    loan_id: int
    book_id: int
    user_id: int
    loan_date: str
    return_date: str

class LoanCreate(BaseModel):
    book_id: int
    user_id: int
    return_date: str

class LoanOut(BaseModel):
    loan_id: int
    book_id: int
    user_id: int
    loan_date: str
    return_date: str

class Author(BaseModel):
    author_id: int
    name: str
    birth_year: int
    books: list[BookOut] = []
    created_at: str

class AuthorOut(BaseModel):
    author_id: int
    name: str
    birth_year: int
    books: list[BookOut] = []

class AuthorCreate(BaseModel):
    name: str
    birth_year: int