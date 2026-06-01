"""
Students class, contains functions to:
    Create a new student 
    Print all students
    Print student info + all their grades
    Update one or more fields for a student
    Remove student AND all their grades
    Print student average, max and min grades 
"""
from pydantic import BaseModel, Field, field_validator
import csv

from .storage import read_data, write_data
from .exceptions import DuplicateEmailError, StudentNotFoundError

class Student(BaseModel):
    id: int
    name: str = Field(min_length=2)
    email: str
    age: int = Field(ge=16, le=60)

    @staticmethod
    def get_new_id() -> int:
        data: dict = read_data()
        return (1 if len(data['students']) == 0 else data['students'][-1]['id'] + 1)
    
    @staticmethod
    def validate_id(student_id: int) -> None:
        data: dict = read_data()
        for student in data['students']:
            if student['id'] == student_id:
                return 
        raise StudentNotFoundError
    
    def __init__(self, name: str, email: str, age: int) -> None:
        super().__init__(id = self.get_new_id(), name=name, email=email, age=age)

    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError("Email must contain @ symbol")
        students = read_data()
        if len(students['students']) == 0:
            return v
        for student in students['students']:    
            if v == student['email']:
                raise DuplicateEmailError()
        return v

    @staticmethod
    def add_student(student: "Student") -> None:
        data: dict = read_data()
        new_student = {
            "id" : Student.get_new_id(),
            "name" : student.name,
            "email" : student.email,
            "age" : student.age,
            "subjects" : []
        }
        data['students'].append(new_student)
        write_data(data)
        print(f"Student added with ID {student.id}")

    @staticmethod
    def list_students() -> None:
        data: dict = read_data()
        for student in data['students']:
            print(f"{student['id']}- {student['name']} ({student['email']}, age {student['age']})")
    
    @staticmethod
    def show_student(student_id: int) -> None:
        Student.validate_id(student_id)
        data: dict = read_data()
        for student in data['students']:
            if student_id == student['id']:
                print(f"{student['name']} ({student['email']}, age {student['age']})")
                if(len(student['subjects'])):
                    print("Grades: ")
                    for subject in student['subjects']:
                        print(f"{subject['subject-name']} - {subject['score']}")
                return


    @staticmethod
    def delete_student(student_id: int) -> None:
        Student.validate_id(student_id)
        data: dict = read_data()
        for ind, student in enumerate(data['students']):
            if student_id == student['id']:
                data['students'].pop(ind)
                write_data(data)
                print(f"Student {student_id} and their grades deleted")
                return

    @staticmethod
    def student_report(student_id: int) -> None:
        Student.validate_id(student_id)
        data: dict = read_data()
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
    
    @staticmethod
    def update_student(student_id: int, fields: list, values: list) -> None:
        Student.validate_id(student_id)
        data = read_data()
        for ind, student in enumerate(data['students']):
            if student['id'] == student_id:
                temp_instance: dict = {
                    "name" : student['name'],
                    "email" : student['email'],
                    "age" : student['age']
                }
                for field, value in zip(fields, values):
                    if field ==  '--name':
                        # data['students'][ind]['name'] = value
                        if len(value) < 2:
                            raise ValueError("Name must be at least 2 chars")
                        temp_instance['name'] = value
                    elif field == '--email':
                        if '@' not in value:
                            raise ValueError("Email must contain @ sybmol")
                        for ind2, student2 in enumerate(data['students']):
                            if ind2 == ind:
                                continue
                            if student2['email'] == value:
                                raise DuplicateEmailError()
                        temp_instance['email'] = value
                    elif field == '--age':
                        try:
                            int(value)
                        except ValueError:
                            raise ValueError("Age must be an integer")
                        if int(value) > 60 or int(value) < 16:
                            raise ValueError("Age must be between 16 and 60")
                        temp_instance['age'] = int(value)

                data['students'][ind]['age'] = temp_instance['age']
                data['students'][ind]['email'] = temp_instance['email']
                data['students'][ind]['name'] = temp_instance['name']                    
                write_data(data)
                print(f"Student {student_id} updated")
                return

    @staticmethod
    def import_students(csv_file: str) -> None:
        with open("test_students.csv", newline='') as csvfile:
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
                    Student.add_student(student)
                except DuplicateEmailError:
                    skipped += 1
                    imported -=1
        print(f"Imported {imported} students, {skipped} rows skipped (invalid data)")