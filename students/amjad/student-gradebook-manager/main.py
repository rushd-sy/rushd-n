import os
import json
import argparse

from pydantic import ValidationError
from services import (
    add_student,
    list_students,
    show_student,
    update_student,
    delete_student,
    add_grade,
    student_report,
    import_students,
    class_report
)
from storage import load_students
from exceptions import StudentNotFoundError, EmailAlreadyUsedError, InvalidGradeError

if __name__ == "__main__":

    if not os.path.exists("students.json"):
        with open("students.json", "w") as f:
            json.dump([], f)

    parser = argparse.ArgumentParser(description="Student Gradebook Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_student_parser = subparsers.add_parser("add-student")
    add_student_parser.add_argument("--name", type=str)
    add_student_parser.add_argument("--email", type=str)
    add_student_parser.add_argument("--age", type=int)

    list_students_parser = subparsers.add_parser("list-students")

    show_student_parser = subparsers.add_parser("show-student")
    show_student_parser.add_argument("--student_id", type=int)

    update_student_parser = subparsers.add_parser("update-student")
    update_student_parser.add_argument("--student_id", type=int)
    update_student_parser.add_argument("--name", type=str, nargs="?")
    update_student_parser.add_argument("--email", type=str, nargs="?")
    update_student_parser.add_argument("--age", type=int, nargs="?")

    delete_student_parser = subparsers.add_parser("delete-student")
    delete_student_parser.add_argument("--student_id", type=int)

    add_grade_parser = subparsers.add_parser("add-grade")
    add_grade_parser.add_argument("--student_id", type=int)
    add_grade_parser.add_argument("--subject", type=str)
    add_grade_parser.add_argument("--grade", type=float)

    student_report_parser = subparsers.add_parser("student-report")
    student_report_parser.add_argument("--student_id", type=int)

    import_students_parser = subparsers.add_parser("import-students")
    import_students_parser.add_argument("--csv_file", type=str)

    class_report_parser = subparsers.add_parser("class-report")

    list_parser = subparsers.add_parser("list")

    args = parser.parse_args()

    students = load_students()

    if args.command == "add-student":
        try:
            add_student(students, args.name, args.email, args.age)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "list-students":
        list_students(students)

    elif args.command == "show-student":
        try:
            show_student(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "update-student":
        try:
            update_student(students, args.student_id, args.name, args.email, args.age)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "delete-student":
        try:
            delete_student(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "add-grade":
        try:
            add_grade(students, args.student_id, args.subject, args.grade)
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except InvalidGradeError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "student-report":
        try:
            student_report(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "import-students":
        try:
            import_students(students, args.csv_file)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "class-report":
        class_report(students)

    elif args.command == "list":
        print("Available commands:")
        print("add-student --name NAME --email EMAIL --age AGE")
        print("list-students")
        print("show-student --student_id ID")
        print("update-student --student_id ID [--name NAME] [--email EMAIL] [--age AGE]")
        print("delete-student --student_id ID")
        print("add-grade --student_id ID --subject SUBJECT --grade GRADE")
        print("student-report --student_id ID")
        print("class-report")
        print("import-students --csv_file FILE")