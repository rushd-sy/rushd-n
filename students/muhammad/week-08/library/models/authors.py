from pydantic import BaseModel, Field
from datetime import date

class AuthorModel(BaseModel):
    author_id: int = Field(gt=0)
    name: str = Field(min_length=3)
    birth_year: int = Field(ge=1)
    added_at: date
    
class AuthorCreate(BaseModel):
    name: str = Field(min_length=3)
    birth_year: int = Field(ge=1)

class AuthorResponse(BaseModel):
    author_id: int = Field(gt=0)
    name: str = Field(min_length=3)
    birth_year: int = Field(ge=1)
