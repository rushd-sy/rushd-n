from pydantic import BaseModel, Field, field_validator

from storage import read_data, write_data
from exceptions import StudentNotFoundError
from students import Student #type: ignore

class Grade(BaseModel):
    student_id: int
    subject: str = Field(min_length=2)
    score: float = Field(ge=0.0, le=100.0)
    

    @field_validator("student_id")
    @classmethod
    def student_id_validator(cls, v: int) -> int:
        Student.validate_id(v)
        return v
    
    @staticmethod
    def add_grade(grade: "Grade") -> None:
        data = read_data()
        for ind, student in enumerate(data['students']):
            if student['id'] == grade.student_id:
                subject: dict = {
                    "subject-name": grade.subject,
                    "score": grade.score
                }
                data['students'][ind]['subjects'].append(subject)
                write_data(data)
                print(f"Grade added for student {grade.student_id}")
                return
        raise StudentNotFoundError()