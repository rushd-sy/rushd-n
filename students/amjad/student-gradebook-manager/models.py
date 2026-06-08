import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date

class Grade(BaseModel):
    subject: str
    score: float
    date: datetime.date = Field(default_factory=datetime.date.today)
    @field_validator("score")
    @classmethod
    def validate_score(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Score must be between 0 and 100")
        return value

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value):
        if len(value) < 2:
            raise ValueError("Subject must be at least 2 characters long")
        return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in the format YYYY-MM-DD")
        return value

class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int


    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 16 or value > 60:
            raise ValueError("Age must be between 16 and 60")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return value
