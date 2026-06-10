# gradebook.py
"""
main function and commands handler
contains functions to:
    Create a new student 
    Print all students
    Print student info + all their grades
    Update one or more fields for a student
    Remove student AND all their grades
    Print student average, max and min grades 
"""

import sys
from exceptions import WrongCommandError, DuplicateEmailError, StudentNotFoundError 
from students import Student # type: ignore
from grades import Grade
from gradebook_logic import (
    add_student,
    list_students,
    show_student,
    delete_student,
    update_student,
    add_grade,
    student_report,
    import_students,
    class_report,
    get_new_id
)


def main():
    args: list = sys.argv
    args_len: int = len(args)

    if args_len < 2:
        raise WrongCommandError()
    
    command: str = args[1]

    if command == 'add-student':
        if args_len != 5:
            raise WrongCommandError()

        name: str = args[2]
        email: str = args[3]
        try:
            age: int = int(args[4])
        except ValueError:
            raise ValueError("Age must be an integer")

        student: "Student" = Student(id=get_new_id(), name=name, email=email, age=age)
        result = add_student(student)
        print(result)

    elif command == 'list-students':
        if args_len != 2:
            raise WrongCommandError()
        
        result = list_students()
        for line in result:
            print(line)

    elif command == 'show-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        result = show_student(student_id)
        for line in result:
            print(line)

    elif command == 'update-student':
        if args_len <= 3 or args_len >= 10 or args_len % 2 == 0:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        fields = [field for field in args[3::2]]
        values = [value for value in args[4::2]]
        result = update_student(student_id, fields, values)
        print(result)

    elif command == 'delete-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        result = delete_student(student_id)
        print(result)

    elif command == 'add-grade':
        if args_len != 5:
            raise WrongCommandError()

        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")

        try:
            score = float(args[4])
        except ValueError:
            raise ValueError("Score must be a float")

        subject: str = args[3]
        grade: Grade = Grade(student_id=student_id, subject=subject, score=score)
        result = add_grade(grade)
        print(result)

    elif command == 'student-report':
        if args_len != 3:
            raise WrongCommandError()

        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")

        result = student_report(student_id)
        print(result)

    elif command == 'import-students':
        if args_len != 3:
            raise WrongCommandError()
        result = import_students(args[2])
        print(result)

    elif command == 'class-report':
        if args_len != 2:
            raise WrongCommandError()
        result = class_report()
        for line in result:
            print(line)

    else:
        raise WrongCommandError()


if __name__ == '__main__':
    main()