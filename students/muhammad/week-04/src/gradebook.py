"""
main function and commands handler
"""
import sys

from students import Student #type: ignore
from grades import Grade
from exceptions import WrongCommandError

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

        student: "Student" = Student(name=name, email=email, age=age)
        Student.add_student(student)

    elif command == 'list-students':
        if args_len != 2:
            raise WrongCommandError()
        
        Student.list_students()
    
    elif command == 'show-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        Student.show_student(student_id)
    
    elif command == 'update-student':
        if args_len <= 3 or args_len >= 10 or args_len % 2 == 0:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        fields = [field for field in args[3::2]]
        values = [value for value in args[4::2]]
        Student.update_student(student_id, fields, values)
    
    elif command == 'delete-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        Student.delete_student(student_id)

        
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
        Grade.add_grade(grade)
    
    elif command == 'student-report':
        if args_len != 3:
            raise WrongCommandError()

        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")

        Student.student_report(student_id)
    
    elif command == 'import-students':
        if args_len != 3:
            raise WrongCommandError()
        Student.import_students(args[2])
    else:
        raise WrongCommandError()



if __name__ == '__main__':
    main()