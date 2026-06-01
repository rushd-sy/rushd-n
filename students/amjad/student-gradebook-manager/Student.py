from pydantic import BaseModel, field_validator


class Student(BaseModel):
    id: int
    name: str
    email: str
    age: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value

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
