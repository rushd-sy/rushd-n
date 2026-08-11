from pydantic import BaseModel
from datetime import date

class LoanModel(BaseModel):
    loan_id: int
    book_id: int
    loan_date: date
    name: str
    added_at: date
    
class LoanCreate(BaseModel):
    book_id: int
    name: str
    loan_date: date

class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    loan_date: date
    name: str
