from pydantic import BaseModel

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
