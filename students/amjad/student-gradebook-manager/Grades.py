from pydantic import BaseModel, field_validator


class Grade(BaseModel):
    student_id: int
    subject: str
    score: float

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
