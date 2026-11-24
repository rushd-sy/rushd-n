from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


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
