from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author_id: int = Field(gt=0)
    genre: str = Field(min_length=1)
    year: int = Field(gt=0)


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    title: str
    author_id: int
    genre: str
    year: int
    created_at: datetime
