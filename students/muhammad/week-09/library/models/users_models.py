from pydantic import BaseModel, field_validator, Field


class User(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    user_id: int = Field(gt=0)

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str = Field(min_length=8)

    @field_validator("username")
    @staticmethod
    def check_username(cls, v: str) -> str:  # type: ignore
        if not v.isalnum():
            raise ValueError("Username must not contain spaces or special characters")        
        return v
    
    @field_validator("email")
    @staticmethod
    def check_email(cls, v: str) -> str: # type: ignore
        if '@' not in v or len(v) < 3:
            raise ValueError("Email must contain '@' and be at least 3 characters")        
        return v

class UserLogin(BaseModel):
    username: str
    password: str
