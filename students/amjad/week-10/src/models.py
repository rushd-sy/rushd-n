from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import TypeVar, Generic
from datetime import datetime

T = TypeVar("T")


class PageParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=20)
    offset: int = Field(default=0, ge=0)


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    offset: int | None = None
    limit: int | None = None


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


class LoanCreate(BaseModel):
    book_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    return_date: datetime


class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    loan_id: int
    book_id: int
    user_id: int
    loan_date: datetime
    return_date: datetime


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author_id: int
    name: str
    birth_year: int
    created_at: datetime


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1)
    birth_year: int = Field(gt=0)



class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    name: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None
    