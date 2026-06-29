"""
Student Pydantic class
"""
from pydantic import BaseModel, Field, field_validator

class Student(BaseModel):
    id: int
    name: str = Field(min_length=2)
    email: str
    age: int = Field(ge=16, le=60)

    def __init__(self, id: int, name: str, email: str, age: int) -> None:
        super().__init__(id=id, name=name, email=email, age=age)

    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError("Email must contain @ symbol")
        return v
