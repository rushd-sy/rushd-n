import json

from services import add_student, delete_student, add_grade, update_student, import_students


def test_add_student(students):
    add_student(students, "bakro", "bakro@example.com", 25)
    assert len(students) == 2
    assert students[1]["name"] == "bakro"


def test_delete_student(students):
    delete_student(students, 1)
    assert len(students) == 0

def test_add_grade(students):
    add_grade(students, 1, "Math", 90)
    assert "grades" in students[0]
    assert len(students[0]["grades"]) == 1
    assert students[0]["grades"][0]["subject"] == "Math"
    assert "date" in students[0]["grades"][0]

def test_update_student(students):
    update_student(students, name="Amjad_new", email="amjad_new@example.com", age=25, student_id=1)
    assert students[0]["name"] == "Amjad_new"
    assert students[0]["email"] == "amjad_new@example.com"
    assert students[0]["age"] == 25

def test_delete_all_student_info(students):
    add_grade(students, 1, "Math", 90)
    delete_student(students, 1)
    with open("students.json", "r") as f:
        data = json.load(f)
        assert data == []

def test_import_csv(students, tmp_path):
    csv_path = tmp_path / "students.csv"
    csv_path.write_text("bakro,bakro@example.com,25")
    assert csv_path.exists()
    import_students(students, csv_path)
    assert len(students) == 2