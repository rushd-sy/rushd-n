from models import Student, Grade
from storage import to_json
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

    student_found = False
    for student in students:
        if email is not None and student["email"] == email and student["id"] != student_id:
            raise EmailAlreadyUsedError("Email already used")
        if student["id"] == student_id:
            student_found = True
            Student(
                    id=student_id, 
                    name=name if name is not None else student["name"], 
                    email=email if email is not None else student["email"],
                    age=age if age is not None else student["age"]
            )
    if not student_found:
        raise StudentNotFoundError("Student not found")
    for student in students:
        if student["id"] == student_id:
            if name is not None:
                student["name"] = name
            if email is not None:
                student["email"] = email
            if age is not None:
                student["age"] = age
            break
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
            print(
                f"{student['name']} — {len(grades)} grades, average: {average}, highest: {highest['score']} ({highest['subject']}), lowest: {lowest['score']} ({lowest['subject']})"
            )
            return
    raise StudentNotFoundError("Student not found")


def import_students(students: list[dict], file_path: str) -> None:
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
            except ValueError:
                invalid += 1
            except EmailAlreadyUsedError:
                invalid += 1

    print(
        f"Imported {total - invalid} students, {invalid} rows skipped (invalid data)"
    )

def class_report(students: list[dict]) -> None:
    if not students:
        print("No students in the class.")
        return

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

    print(f"Total students: {total_students}")
    print(f"Class average: {class_average}")
    print("Top 3 students by average:")
    for name, avg in top_students:
        print(f"{name} - Average: {avg}")