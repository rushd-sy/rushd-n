from pydantic import ValidationError
import pytest
import os
from tempfile import TemporaryDirectory

from .. import storage
from .. import gradebook
from ..students import Student
from ..grades import Grade
@pytest.fixture(autouse=True)
def temp_json_file(monkeypatch):
    with TemporaryDirectory() as temp_dir:
        json_file_path = os.path.join(temp_dir, 'test_gradebook.json')
        
        monkeypatch.setenv("GRADEBOOK_DB", json_file_path)
        
        temp = {"students": []}
        storage.write_data(temp)
        
        yield 


class TestGradeBook:
    def test_adding_valid_student_works(self) -> None:
        student = Student(id=0, name="MuhammadTest", email="muhammad@email.com", age=21)
        gradebook.add_student(student)

        data = storage.read_data()
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "MuhammadTest",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : []
        }
        assert dict_student == data['students'][0]
    
    def test_adding_student_short_name_fails(self) -> None:
        with pytest.raises(ValidationError):
            Student(id=0, name="M", email="muhammad@email.com", age=21)

        data = storage.read_data()
        assert len(data['students']) == 0
    
    def test_adding_student_bad_email_fails(self) -> None:
        with pytest.raises(ValidationError):
            Student(id=0, name="Muhammad", email="muhammad", age=21)

        data = storage.read_data()
        assert len(data['students']) == 0
    
    def test_adding_student_age_out_of_range_fails(self) -> None:
        with pytest.raises(ValidationError):
            Student(id=0, name="Muhammad", email="muhammad@email.com", age=5)

        data = storage.read_data()
        assert len(data['students']) == 0

    def test_adding_duplicated_email_fails(self) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        
        student2 = Student(id=0, name="Ahmad", email="muhammad@email.com", age=25)
        with pytest.raises(gradebook.DuplicateEmailError):
            gradebook.add_student(student2)
        
        data = storage.read_data()  
        
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "Muhammad",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : []
        }
        assert  dict_student == data['students'][0]
    
    def test_add_grade_to_existing_student_works(self) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        grade = Grade(student_id=1, subject="Math", score=95.0)
        gradebook.add_grade(grade)
        
        data  = storage.read_data()
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "Muhammad",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : [
                {
                    "subject-name" : "Math",
                    "score" : 95.0
                }
            ]
        }
        assert  dict_student == data['students'][0]
    
    def test_add_grade_to_non_existing_student_fails(self) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        grade = Grade(student_id=2, subject="Math", score=95.0)
        with pytest.raises(gradebook.StudentNotFoundError):
            gradebook.add_grade(grade)
        
        data  = storage.read_data()
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "Muhammad",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : []
        }
        assert  dict_student == data['students'][0]
    
    def test_score_out_of_range_fails(self) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        with pytest.raises(ValidationError):
            grade = Grade(student_id=1, subject="Math", score=105.0)
            gradebook.add_grade(grade)

        data  = storage.read_data()
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "Muhammad",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : []
        }
        assert  dict_student == data['students'][0]
    
    def test_deleted_student_deleted_their_grades(self) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        grade = Grade(student_id=1, subject="Math", score=99.0)
        gradebook.add_grade(grade)
        
        gradebook.delete_student(1)

        data  = storage.read_data()
        assert len(data['students']) == 0
    
    
    
    def test_student_report_average_works(self, capsys) -> None:
        student = Student(id=0, name="Muhammad", email="muhammad@email.com", age=21)
        gradebook.add_student(student)
        grade = Grade(student_id=1, subject="Math", score=99.0)
        gradebook.add_grade(grade)
        grade = Grade(student_id=1, subject="Physics", score=63.0)
        gradebook.add_grade(grade)
        
        captured = capsys.readouterr()
        gradebook.student_report(1)
        captured = capsys.readouterr()

        data  = storage.read_data()
        assert len(data['students']) == 1
        dict_student = {
            "id" : 1,
            "name" : "Muhammad",
            "email" : "muhammad@email.com",
            "age" : 21,
            "subjects" : [ 
                {
                    "subject-name" : "Math",
                    "score" : 99.0
                },
                {
                    "subject-name" : "Physics",
                    "score" : 63.0
                }
            ]
        }
        assert  dict_student == data['students'][0]
        assert captured.out == "Muhammad - 2 grades, average: 81.0, highest: 99.0 (Math), lowest: 63.0 (Physics)\n"   
    
    def test_csv_import_valid_rows_and_skip_invalid_rows(self) -> None:
        gradebook.import_students("students.csv")
        data  = storage.read_data()
        assert data == {
        "students": [
                {
                    "id": 1,
                    "name": "Nour",
                    "email": "nour@example.com",
                    "age": 21,
                    "subjects": []
                },
                {
                    "id": 2,
                    "name": "Ali",
                    "email": "ali@example.com",
                    "age": 20,
                    "subjects": []
                },
                {
                    "id": 3,
                    "name": "Sara",
                    "email": "sara@example.com",
                    "age": 22,
                    "subjects": []
                },
                {
                    "id": 4,
                    "name": "Omar",
                    "email": "omar@example.com",
                    "age": 19,
                    "subjects": []
                },
                {
                    "id": 5,
                    "name": "Mona",
                    "email": "mona@example.com",
                    "age": 25,
                    "subjects": []
                }
            ]
        }
