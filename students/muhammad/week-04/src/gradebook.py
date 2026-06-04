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
import csv

from students import Student
from grades import Grade
from exceptions import WrongCommandError, DuplicateEmailError, StudentNotFoundError
from storage import read_data, write_data

def add_student(student: "Student") -> None:
    data: dict[str, list] = read_data()
    new_student = {
        "id" : Student.get_new_id(),
        "name" : student.name,
        "email" : student.email,
        "age" : student.age,
        "subjects" : []
    }
    for temp_student in data['students']:    
        if student.email == temp_student['email']:
            raise DuplicateEmailError()
    data['students'].append(new_student)
    write_data(data)
    print(f"Student added with ID {new_student['id']}")


def list_students() -> None:
    data: dict[str, list] = read_data()
    for student in data['students']:
        print(f"{student['id']}- {student['name']} ({student['email']}, age {student['age']})")

def show_student(student_id: int) -> None:
    Student.validate_id(student_id)
    data: dict[str, list] = read_data()
    for student in data['students']:
        if student_id == student['id']:
            print(f"{student['name']} ({student['email']}, age {student['age']})")
            if(len(student['subjects'])):
                print("Grades: ")
                for subject in student['subjects']:
                    print(f"{subject['subject-name']} - {subject['score']}")
            return

def delete_student(student_id: int) -> None:
    Student.validate_id(student_id)
    data: dict[str, list] = read_data()
    for ind, student in enumerate(data['students']):
        if student_id == student['id']:
            data['students'].pop(ind)
            write_data(data)
            print(f"Student {student_id} and their grades deleted")
            return

def student_report(student_id: int) -> None:
    Student.validate_id(student_id)
    data: dict[str, list] = read_data()
    for student in data['students']:
        if student_id == student['id']:
            print(f"{student['name']} - {len(student['subjects'])} grades", end='')
            if len(student['subjects']):
                total = 0.0
                highest = -0.1
                highest_name: str = ""
                lowest = 100.1
                lowest_name: str = ""
                for subject in student['subjects']:
                    total += subject['score']
                    if subject['score'] > highest:
                        highest = subject['score']
                        highest_name = subject['subject-name']
                    if subject['score'] < lowest:
                        lowest = subject['score']
                        lowest_name = subject['subject-name']
                average = total / len(student['subjects'])
                print(f", average: {average}, highest: {highest} ({highest_name}), lowest: {lowest} ({lowest_name})")
            return
    

def update_student(student_id: int, fields: list, values: list) -> None:
    Student.validate_id(student_id)
    data: dict[str, list] = read_data()
    for ind, student in enumerate(data['students']):
        if student['id'] == student_id:
            temp_instance: dict = {
                "name" : student['name'],
                "email" : student['email'],
                "age" : student['age']
            }
            for field, value in zip(fields, values):
                if field ==  '--name':
                    temp_instance['name'] = value
                elif field == '--email':
                    for student in data['students']:    
                        if value == student['email']:
                            raise DuplicateEmailError()
                    temp_instance['email'] = value
                elif field == '--age':
                    try:
                        int(value)
                    except ValueError:
                        raise ValueError("Age must be an integer")
                    temp_instance['age'] = int(value)
            Student(name=temp_instance['name'], email=temp_instance['email'], age=temp_instance['age'])
            data['students'][ind]['name'] = temp_instance['name']                    
            data['students'][ind]['email'] = temp_instance['email']
            data['students'][ind]['age'] = temp_instance['age']
            write_data(data)
            print(f"Student {student_id} updated")
            return


def class_report() -> None:
    data = read_data()
    total_students = len(data['students'])
    if total_students == 0:
        print("No students availble")
        return

    total_avg = 0
    averages: list[dict] = []
    for student in data['students']:
        cur_avg = 0
        for subject in student['subjects']:
            cur_avg += subject['score']
        
        if len(student['subjects']):
            cur_avg = cur_avg / len(student['subjects'])
        total_avg += cur_avg
        average = {
            "name" :  student['name'],
            "average" :  cur_avg,
        }
        averages.append(average)
        
    total_avg = total_avg / total_students
    averages = sorted(averages, key=lambda x: x['average'], reverse=True)

    print(f"Total Sutdents: {total_students}")
    print(f"Class average: {total_avg:.2f}")
    
    if total_students >= 2:
        print(f"Top {min(3, total_students)} students: ")
    else:
        print("The only student: ")
    
    for i in range(min(3, total_students)):
        if i == 0:
            print(" 1st-student: ")
        elif i == 1:
            print(" 2nd-student: ")
        else:
            print(" 3rd-student: ")
        print(f"    {averages[i]['name']}, average: {averages[i]['average']:.2f}")

def import_students(csv_file: str) -> None:
    with open(csv_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        skipped = 0
        imported = 0
        for row in spamreader:
            if len(row) != 3:
                skipped += 1
                continue
            imported += 1
            name, email, age_str = row
            name = name.strip()
            email = email.strip()
            try:
                age = int(age_str.strip())
            except ValueError:
                raise ValueError("Age must be an integer")

            try:
                student = Student(name=name, email=email, age=age)
                add_student(student)
            except Exception:
                skipped += 1
                imported -=1
    print(f"Imported {imported} students, {skipped} rows skipped (invalid data)")

def add_grade(grade: "Grade") -> None:
    data: dict[str, list] = read_data()
    for ind, student in enumerate(data['students']):
        if student['id'] == grade.student_id:
            subject: dict = {
                "subject-name": grade.subject,
                "score": grade.score
            }
            data['students'][ind]['subjects'].append(subject)
            write_data(data)
            print(f"Grade added for student {grade.student_id}")
            return
    raise StudentNotFoundError()

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
        add_student(student)

    elif command == 'list-students':
        if args_len != 2:
            raise WrongCommandError()
        
        list_students()
    
    elif command == 'show-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        show_student(student_id)
    
    elif command == 'update-student':
        if args_len <= 3 or args_len >= 10 or args_len % 2 == 0:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        fields = [field for field in args[3::2]]
        values = [value for value in args[4::2]]
        update_student(student_id, fields, values)
    
    elif command == 'delete-student':
        if args_len != 3:
            raise WrongCommandError()
        
        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")
        
        delete_student(student_id)

        
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
        add_grade(grade)
    
    elif command == 'student-report':
        if args_len != 3:
            raise WrongCommandError()

        try:
            student_id = int(args[2])
        except ValueError:
            raise ValueError("Student ID must be an integer")

        student_report(student_id)
    
    elif command == 'import-students':
        if args_len != 3:
            raise WrongCommandError()
        import_students(args[2])
            
    elif command == 'class-report':
        if args_len != 2:
            raise WrongCommandError()
        class_report()
        
    else:
        raise WrongCommandError()



if __name__ == '__main__':
    main()
