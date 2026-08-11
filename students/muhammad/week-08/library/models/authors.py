from pydantic import BaseModel
from datetime import date

class AuthorModel(BaseModel):
    author_id: int
    name: str
    birth_year: int
    added_at: date
    
class AuthorCreate(BaseModel):
    name: str
    birth_year: int

class AuthorResponse(BaseModel):
    author_id: int
    name: str
    birth_year: int
