from pydantic import BaseModel, Field

class Grade(BaseModel):
    student_id: int
    subject: str = Field(min_length=2)
    score: float = Field(ge=0.0, le=100.0)
    