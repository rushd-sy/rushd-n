from pydantic import ValidationError
import pytest
from services import *
from conftest import *
from exceptions import *

def test_add_student_short_name(students):
    with pytest.raises(ValidationError):
        add_student(students, "b", "bakroexample.com", 25)

def test_add_student_invalid_email(students):
    with pytest.raises(ValidationError):
        add_student(students, "bakro", "invalid-email", 25)

def test_add_student_invalid_age(students):
    with pytest.raises(ValidationError):
        add_student(students, "bakro", "bakro@example.com", -5)

def test_add_student_duplicate_email(students):
    with pytest.raises(EmailAlreadyUsedError):
        add_student(students, "bakro", "amjad@example.com", 25)

def test_delete_student_not_found(students):
    with pytest.raises(StudentNotFoundError):
        delete_student(students, 1)

def test_add_grade_student_not_found(students):
    with pytest.raises(StudentNotFoundError):
        add_grade(students, 5, "Math", 90)

def test_add_grade_invalid_score(students):
    with pytest.raises(ValidationError):
        add_grade(students, 1, "Math", -10)

def test_update_student_not_found(students):
    with pytest.raises(StudentNotFoundError):
        update_student(students, name="Amjad_new", email="amjad_new@example.com", age=25, student_id=3)
    assert students[0]["email"] == "amjad@example.com"
    assert students[0]["age"] == 20


def test_import_csv_invalid_data(students, tmp_path):
    csv_path = tmp_path / "students.csv"
    csv_path.write_text("bakro@example.com,25")
    import_students(students, csv_path)
    assert len(students) == 1