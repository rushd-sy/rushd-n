from pydantic import BaseModel

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
