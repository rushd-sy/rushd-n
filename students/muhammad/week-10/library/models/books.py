from pydantic import BaseModel, Field
from datetime import date

class BookModel(BaseModel):
    book_id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)
    creation_date: date

class BookCreate(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)


class BookResponse(BaseModel):
    book_id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)
