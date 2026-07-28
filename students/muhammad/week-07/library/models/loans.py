from pydantic import BaseModel

class LoanModel(BaseModel):
    loan_id: int
    book_id: int
    date: str
    name: str
    added_at: str
    
class LoanCreate(BaseModel):
    book_id: int
    name: str
    date: str

class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    date: str
    name: str
