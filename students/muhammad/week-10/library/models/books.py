from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class BookModel(BaseModel):
    book_id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)
    creation_date: date

class BookCreate(BaseModel):
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)


class BookResponse(BaseModel):
    book_id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    genre: str = Field(min_length=3)
    publish_year: int = Field(gt=1000)
    
    model_config = ConfigDict(from_attributes=True)
