from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    offset: int | None = None
    limit: int | None = None

class BookModel(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    publish_year: int
    creation_date: str

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    publish_year: int


class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    publish_year: int



class AuthorModel(BaseModel):
    author_id: int
    name: str
    birth_year: int
    added_at: str
    
class AuthorCreate(BaseModel):
    name: str
    birth_year: int

class AuthorResponse(BaseModel):
    author_id: int
    name: str
    birth_year: int

class LoanModel(BaseModel):
    loan_id: int
    date: str
    added_at: str
    
class LoanCreate(BaseModel):
    name: str
    date: str

class LoanResponse(BaseModel):
    loan_id: int
    date: str
