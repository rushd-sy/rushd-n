from pydantic import ValidationError

from models import Student, Grade
from storage import to_json
from exceptions import EmailAlreadyUsedError, StudentNotFoundError
import datetime

def add_student(students: list[dict], name: str, email: str, age: int) -> int:
    if students:
        student_id = max(student["id"] for student in students) + 1
    else:
        student_id = 1

    for student in students:
        if student["email"] == email:
            raise EmailAlreadyUsedError("Email already used")

    student = Student(id=student_id, name=name, email=email, age=age)

    students.append(student.model_dump())
    to_json(students)
    return student_id


def show_student(students: list[dict], student_id: int) -> dict:
    for student in students:
        if student["id"] == student_id:
            return student

    raise StudentNotFoundError("Student not found")


def update_student(
    students: list[dict],
    student_id: int,
    name: str | None = None,
    email: str | None = None,
    age: int | None = None,
) -> None:

    target_student = None
    
    for student in students:
        if email is not None and student["email"] == email and student["id"] != student_id:
            raise EmailAlreadyUsedError("Email already used")
        if student["id"] == student_id:
            target_student = student

    if target_student is None:
        raise StudentNotFoundError("Student not found")

    Student(
        id=student_id, 
        name=name if name is not None else target_student["name"], 
        email=email if email is not None else target_student["email"],
        age=age if age is not None else target_student["age"]
    )

    if name is not None:
        target_student["name"] = name
    if email is not None:
        target_student["email"] = email
    if age is not None:
        target_student["age"] = age
        
    to_json(students)


def delete_student(students: list[dict], student_id: int) -> None:
    old_length = len(students)

    students[:] = [student for student in students if student["id"] != student_id]

    if len(students) == old_length:
        raise StudentNotFoundError("Student not found")

    to_json(students)


def add_grade(students: list[dict], student_id: int, subject: str, score: float) -> None:
    student_found = False
    for student in students:
        if student["id"] == student_id:
            if "grades" not in student:
                student["grades"] = []
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            grade = Grade(subject=subject, score=score)
            student["grades"].append(
                {"subject": grade.subject, "score": grade.score, "date": grade.date}
            )
            student_found = True
            break
    if not student_found:
        raise StudentNotFoundError("Student not found")
    to_json(students)


def student_report(students: list[dict], student_id: int) -> dict:
    for student in students:
        if student["id"] == student_id:
            grades = student.get("grades", [])
            if not grades:
                return {"name": student['name'], "has_grades": False}
            elif grades:
                total = 0
                highest = grades[0]
                lowest = grades[0]
                for grade in grades:
                    total += grade["score"]
                    if grade["score"] > highest["score"]:
                        highest = grade
                    if grade["score"] < lowest["score"]:
                        lowest = grade
                        
                average = total / len(grades)
                round(average, 2)
                return {
                    "name": student['name'],
                    "has_grades": True,
                    "grades_count": len(grades),
                    "average": average,
                    "highest_score": highest['score'],
                    "highest_subject": highest['subject'],
                    "lowest_score": lowest['score'],
                    "lowest_subject": lowest['subject']
                }
    raise StudentNotFoundError("Student not found")


def import_students(students: list[dict], file_path: str) -> tuple[int, int]:
    invalid = 0
    total = 0
    with open(file_path, "r") as f:
        lines = (line for line in f)
        for line in lines:
            total += 1
            if line.count(",") != 2:
                invalid += 1
                continue
            name, email, age = line.strip().split(",")
            try:
                add_student(students, name, email, int(age))
            except (ValueError, EmailAlreadyUsedError, ValidationError):
                invalid += 1

    imported_count = total - invalid
    return imported_count, invalid

def class_report(students: list[dict]) -> dict | None:
    if not students:
        return None

    total_students = len(students)
    total_average = 0
    student_averages = []

    for student in students:
        grades = student.get("grades", [])
        if grades:
            average = sum(grade["score"] for grade in grades) / len(grades)
            total_average += average
            student_averages.append((student["name"], average))

    class_average = total_average / len(student_averages) if student_averages else 0
    top_students = sorted(student_averages, key=lambda x: x[1], reverse=True)[:3]

    return {
        "total_students": total_students,
        "class_average": class_average,
        "top_students": top_students
    }