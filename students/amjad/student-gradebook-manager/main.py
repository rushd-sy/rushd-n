import os
import json
import argparse

from pydantic import ValidationError
from services import *

if __name__ == "__main__":

    if not os.path.exists("students.json"):
        with open("students.json", "w") as f:
            json.dump([], f)

    parser = argparse.ArgumentParser(description="Student Gradebook Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_student_parser = subparsers.add_parser("add_student")
    add_student_parser.add_argument("--name", type=str)
    add_student_parser.add_argument("--email", type=str)
    add_student_parser.add_argument("--age", type=int)

    list_students_parser = subparsers.add_parser("list_students")

    show_student_parser = subparsers.add_parser("show_student")
    show_student_parser.add_argument("--student_id", type=int)

    update_student_parser = subparsers.add_parser("update_student")
    update_student_parser.add_argument("--student_id", type=int)
    update_student_parser.add_argument("--name", type=str, nargs="?")
    update_student_parser.add_argument("--email", type=str, nargs="?")
    update_student_parser.add_argument("--age", type=int, nargs="?")

    delete_student_parser = subparsers.add_parser("delete_student")
    delete_student_parser.add_argument("--student_id", type=int)

    add_grade_parser = subparsers.add_parser("add_grade")
    add_grade_parser.add_argument("--student_id", type=int)
    add_grade_parser.add_argument("--subject", type=str)
    add_grade_parser.add_argument("--grade", type=float)

    student_report_parser = subparsers.add_parser("student_report")
    student_report_parser.add_argument("--student_id", type=int)

    import_students_parser = subparsers.add_parser("import_students")
    import_students_parser.add_argument("--csv_file", type=str)

    list_parser = subparsers.add_parser("list")

    args = parser.parse_args()

    students = load_students()

    if args.command == "add_student":
        try:
            add_student(students, args.name, args.email, args.age)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "list_students":
        list_students(students)

    elif args.command == "show_student":
        try:
            show_student(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "update_student":
        try:
            update_student(students, args.student_id, args.name, args.email, args.age)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "delete_student":
        try:
            delete_student(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "add_grade":
        try:
            add_grade(students, args.student_id, args.subject, args.grade)
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except InvalidGradeError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "student_report":
        try:
            student_report(students, args.student_id)
        except StudentNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "import_students":
        try:
            import_students(students, args.csv_file)
        except EmailAlreadyUsedError as e:
            print(f"Error: {e}")
        except StudentNotFoundError as e:
            print(f"Error: {e}")
        except ValidationError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        print("Available commands:")
        print("add_student --name NAME --email EMAIL --age AGE")
        print("list_students")
        print("show_student --student_id ID")
        print("update_student --student_id ID [--name NAME] [--email EMAIL] [--age AGE]")
        print("delete_student --student_id ID")
        print("add_grade --student_id ID --subject SUBJECT --grade GRADE")
        print("student_report --student_id ID")
        print("import_students --csv_file FILE")