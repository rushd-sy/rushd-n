from pydantic import BaseModel, ValidationError, field_validator
import pytest

class User(BaseModel):
    age: int
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def name_validator(cls, name: str):
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters")
        return name

    @field_validator("age")
    @classmethod
    def age_validator(cls, age: int):
        if age < 13 or age > 120:
            raise ValueError("Age must be between 13 and 120")
        return age

    @field_validator("email")
    @classmethod
    def email_validator(cls, email: str):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email

    def user_info(self) -> str:
        return f"Name: {self.name}, Age: {self.age}, Email: {self.email}"
    


def test_user_name_invalid():
    try:
        User(age=25, name="A", email="amjad@gmail.com")
        assert False, "Expected validation error"
    except ValidationError as e:
        assert "Name must be at least 2 characters" in str(e)

def test_user_age_invalid():
    try:
        User(age=10, name="amjad", email="amjad@gmail.com")
        assert False, "Expected validation error"
    except ValidationError as e:
        assert "Age must be between 13 and 120" in str(e)

def test_user_email_invalid():
    try:
        User(age=25, name="amjad", email="amjadgmail.com")
        assert False, "Expected validation error"
    except ValidationError as e:
        assert "Invalid email address" in str(e)

def test_user_name_valid():
    user = User(age=25, name="Amjad", email="amjad@gmail.com")
    assert user.name == "Amjad"

def test_user_age_valid():
    user = User(age=25, name="Amjad", email="amjad@gmail.com")
    assert user.age == 25
