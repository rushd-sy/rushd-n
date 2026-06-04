"""
Student Pydantic class
"""
from pydantic import BaseModel, Field, field_validator

from storage import read_data
from exceptions import StudentNotFoundError

class Student(BaseModel):
    id: int
    name: str = Field(min_length=2)
    email: str
    age: int = Field(ge=16, le=60)

    @staticmethod
    def get_new_id() -> int:
        data: dict = read_data()
        return (1 if len(data['students']) == 0 else data['students'][-1]['id'] + 1)
    
    @staticmethod
    def validate_id(student_id: int) -> None:
        data: dict = read_data()
        for student in data['students']:
            if student['id'] == student_id:
                return 
        raise StudentNotFoundError()
    
    def __init__(self, name: str, email: str, age: int) -> None:
        super().__init__(id = self.get_new_id(), name=name, email=email, age=age)

    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError("Email must contain @ symbol")
        return v
