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
from numpy import average
from students import Student # type: ignore
from grades import Grade
from gradebook_logic import (
    add_student,
    show_student,
    delete_student,
    update_student,
    add_grade,
    student_report,
    import_students,
    class_report,
    get_new_id
)
from storage import read_data

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

        student = add_student(Student(id=get_new_id(), name=name, email=email, age=age))
        print(f"Student added with id {student.id}")

    elif command == 'list-students':
        if args_len != 2:
            raise WrongCommandError()
        
        data: dict[str, list] = read_data()
        for student in data['students']:
            print(f"{student['id']}- {student['name']} ({student['email']}, age {student['age']})")


    elif command == 'show-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        student = show_student(student_id)
        output = [f"{student['name']} ({student['email']}, age {student['age']})"]
        if len(student['subjects']):
            output.append("Grades: ")
            for sub in student['subjects']:
                output.append(f"{sub['subject-name']} - {sub['score']}")

        for line in output:
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
        added: bool = update_student(student_id, fields, values)
        print("Student updated successfully" if added else "Couldn't update student")

    elif command == 'delete-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        deleted: bool = delete_student(student_id)
        print("Student and their grades were deleted successfully" if deleted else "Couldn't delete student")


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
        added: bool = add_grade(grade)
        print("Grade added successfully" if added else "Couldn't add garde")

    elif command == 'student-report':
        if args_len != 3:
            raise WrongCommandError()

        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")

        student_data = student_report(student_id)
        num_grades = student_data['num_grades']
        
        if num_grades:
            average = student_data['average']
            highest = student_data['highest']
            highest_name = student_data['highest_name']
            lowest = student_data['lowest']
            lowest_name = student_data['lowest_name']
            output = f"{student_data['name']} — {num_grades} grades, average: {average:.2f}, highest: {highest} ({highest_name}), lowest: {lowest} ({lowest_name})"
        else:
            output = f"{student_data['name']} — 0 grades"
        print(output)

    elif command == 'import-students':
        if args_len != 3:
            raise WrongCommandError()
        imported, skipped = import_students(args[2])
        print(f"Imported {imported} students, skipped {skipped} students")

    elif command == 'class-report':
        if args_len != 2:
            raise WrongCommandError()
        result: dict = class_report()
        
        if not result:
            print("There is no student to report")
            sys.exit()
        
        total_students = result['total_students']
        total_avg = result['total_avg']
        averages = result['averages']
        
        print(f"Total Students: {total_students}")
        print(f"Class average: {total_avg:.2f}")
        
        top_n = min(3, total_students)
        if total_students >= 2:
            print(f"Top {top_n} students: ")
        else:
            print("The only student: ")
        
        positions = ["1st-student", "2nd-student", "3rd-student"]
        for i in range(top_n):
            print(f" {positions[i]}: ")
            print(f"    {averages[i]['name']}, average: {averages[i]['average']:.2f}")    

    else:
        raise WrongCommandError()


if __name__ == '__main__':
    main()