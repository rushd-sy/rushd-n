from pydantic import ValidationError
import pytest
import os
from tempfile import TemporaryDirectory

from ..storage import write_data, read_data

@pytest.fixture
def temp_json_file(monkeypatch):
    with TemporaryDirectory() as temp_dir:
        json_file_path = os.path.join(temp_dir, 'test_gradebook.json')
        temp = {
            "students" : []
        }
        write_data(temp, json_file_path)
    
        
        def temp_read() -> dict:
            return read_data(json_file_path)

        def temp_write(data) -> None:
            return write_data(data, json_file_path)
        
        from .. import storage
        monkeypatch.setattr(storage, "read_data", temp_read)
        monkeypatch.setattr(storage, "write_data", temp_write)

        from ..students import Student
        yield storage, Student


class TestGradeBook:
    
    def test_adding_valid_student_works(self, temp_json_file) -> None:
        storage, Student = temp_json_file
        
        student = Student(name="Muhammad", email="muhammad@email.com", age=21)
        Student.add_student(student)

        data = storage.read_data()
        
        assert len(data['students']) == 1
        assert data["students"][0]['name'] == "Muhammad"
        assert data["students"][0]['email'] == "muhammad@email.com"
        assert data["students"][0]['age'] == 21
    
    
    def test_adding_student_short_name_fails(self, temp_json_file) -> None:
        storage, Student = temp_json_file
        
        with pytest.raises(ValidationError):
            student = Student(name="M", email="muhammad@email.com", age=21)
            Student.add_student(student)

        data = storage.read_data()
        assert len(data['students']) == 0
    
    
    def test_adding_student_bad_email_fails(self, temp_json_file) -> None:
        storage, Student = temp_json_file
        
        with pytest.raises(ValidationError):
            student = Student(name="Muhammad", email="muhammad", age=21)
            Student.add_student(student)

        data = storage.read_data()
        assert len(data['students']) == 0
    
    def test_adding_student_age_out_of_range_fails(self, temp_json_file) -> None:
        storage, Student = temp_json_file
        
        with pytest.raises(ValidationError):
            student = Student(name="Muhammad", email="muhammad@email.com", age=5)
            Student.add_student(student)

        data = storage.read_data()
        assert len(data['students']) == 0

    # def test_adding_duplicated_email_fails(self, temp_json_file) -> None:
    #     storage, Student = temp_json_file
        
    #     student = Student(name="Muhammad", email="muhammad@email.com", age=21)
    #     Student.add_student(student)
        
    #     student2 = Student(name="Ahmad", email="muhammad@email.com", age=25)

    #     with pytest.raises(ValidationError):
    #         Student.add_student(student2)
        
    #     data = storage.read_data()  
        
    #     assert len(data['students']) == 1
    #     assert data["students"][0]['name'] == "Muhammad"
    #     assert data["students"][0]['email'] == "muhammad@email.com"
    #     assert data["students"][0]['age'] == 21
    