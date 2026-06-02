from Student import Student
from Grades import Grade
from storage import load_students, to_json
from exceptions import *


def add_student(students: list[dict], name: str, email: str, age: int) -> None:
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
    print(f"Student added with ID: {student_id}")


def list_students(students: list[dict]) -> None:
    for student in students:
        print(
            f"{student['id']} - {student['name']} ({student['email']}, age {student['age']})"
        )


def show_student(students: list[dict], student_id: int) -> None:
    for student in students:
        if student["id"] == student_id:
            print(f"{student['name']} ({student['email']}, age {student['age']})")
            if "grades" not in student:
                return
            grades = student.get("grades", [])
            for grade in grades:
                print(f"{grade['subject']} - {grade['score']}")
            return

    raise StudentNotFoundError("Student not found")


def update_student(
    students: list[dict],
    student_id: int,
    name: str | None = None,
    email: str | None = None,
    age: int | None = None,
) -> None:

    for student in students:
        if student["email"] == email:
            raise EmailAlreadyUsedError("Email already used")
    Student(id=student_id, name=name or "Valid", email=email or "Valid@Email.com", age=age or 16)
    student_found = False
    for student in students:
        if student["id"] == student_id:
            student_found = True
            if name is not None:
                student["name"] = name
            if email is not None:
                student["email"] = email
            if age is not None:
                student["age"] = age
            break
    if not student_found:
        raise StudentNotFoundError("Student not found")
    to_json(students)
    print(f"Student {student_id} updated successfully")


def delete_student(students: list[dict], student_id: int) -> None:
    old_length = len(students)

    students[:] = [student for student in students if student["id"] != student_id]

    if len(students) == old_length:
        raise StudentNotFoundError("Student not found")

    to_json(students)
    print(f"Student {student_id} and their grades deleted")


def add_grade(students: list[dict], student_id: int, subject: str, score: float) -> None:
    student_found = False
    for student in students:
        if student["id"] == student_id:
            if "grades" not in student:
                student["grades"] = []
            grade = Grade(student_id=student_id, subject=subject, score=score)
            student["grades"].append(
                {"subject": grade.subject, "score": grade.score}
            )
            student_found = True
            break
    if not student_found:
        raise StudentNotFoundError("Student not found")
    to_json(students)
    print(f"Grade added for student {student_id}")


def student_report(students: list[dict], student_id: int) -> None:
    for student in students:
        if student["id"] == student_id:
            grades = student.get("grades", [])
            if not grades:
                print(f"Student {student['name']} has no grades.")
                return
            sum = 0
            highest = grades[0]
            lowest = grades[0]
            for grade in grades:
                sum += grade["score"]
                if grade["score"] > highest["score"]:
                    highest = grade
                if grade["score"] < lowest["score"]:
                    lowest = grade
            average = sum / len(grades)
            print(
                f"{student['name']} — {len(grades)} grades, average: {average}, highest: {highest['score']} ({highest['subject']}), lowest: {lowest['score']} ({lowest['subject']})"
            )
            return
    raise StudentNotFoundError("Student not found")


def import_students(students: list[dict], file_path: str) -> None:
    with open(file_path, "r") as f:
        lines = f.readlines()

    invalid = 0
    for line in lines:
        if line.count(",") != 2:
            invalid += 1
            continue
        name, email, age = line.strip().split(",")
        add_student(students, name, email, int(age))

    print(
        f"Imported {len(lines) - invalid} students, {invalid} rows skipped (invalid data)"
    )
