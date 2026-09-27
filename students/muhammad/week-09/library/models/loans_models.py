from pydantic import BaseModel, Field
from datetime import date

class LoanModel(BaseModel):
    loan_id: int = Field(ge=1)
    book_id: int = Field(ge=1)
    loan_date: date
    name: str = Field(min_length=3)
    added_at: date
    
class LoanCreate(BaseModel):
    book_id: int = Field(ge=1)
    name: str = Field(min_length=3)
    loan_date: date

class LoanResponse(BaseModel):
    loan_id: int = Field(ge=1)
    book_id: int = Field(ge=1)
    loan_date: date
    name: str = Field(min_length=3)
