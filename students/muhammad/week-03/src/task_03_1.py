from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    name: str = Field(
        min_length=2
    )
    email: str
    age: int
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Email must contain @.')
        return v
    
    @field_validator('age')
    @classmethod
    def age_validator(cls, v: int) -> int:
        if v < 13 or v > 120:
            raise ValueError('Age must be between 13 and 120.')
        return v
