from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author_id: int
    name: str
    birth_year: int
    created_at: datetime


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1)
    birth_year: int = Field(gt=0)
