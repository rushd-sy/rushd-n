from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int 
    offset: int | None = None
    limit: int | None = None


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    genre: str = Field(min_length=1)
    year: int = Field(gt=0)

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
    book_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    return_date: str = Field(min_length=1)

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
    created_at: str

class AuthorOut(BaseModel):
    author_id: int
    name: str
    birth_year: int

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1)
    birth_year: int = Field(gt=0)