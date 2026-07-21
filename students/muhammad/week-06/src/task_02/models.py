from pydantic import BaseModel

class book_model(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    publish_year: int
    creation_date: str

class book_create(BaseModel):
    title: str
    author: str
    genre: str
    publish_year: int


class book_response(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    publish_year: int



class author_model(BaseModel):
    author_id: int
    name: str
    birth_year: int
    added_at: str
    
class author_create(BaseModel):
    name: str
    birth_year: int

class author_response(BaseModel):
    author_id: int
    name: str
    birth_year: int

class loan_model(BaseModel):
    loan_id: int
    date: str
    added_at: str
    
class loan_create(BaseModel):
    name: str
    date: str

class loan_response(BaseModel):
    loan_id: int
    date: str
