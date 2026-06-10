import csv
from students import Student # type: ignore
from grades import Grade
from exceptions import DuplicateEmailError, StudentNotFoundError
from storage import read_data, write_data


def get_new_id() -> int:
    data = read_data()
    return (1 if len(data['students']) == 0 else data['students'][-1]['id'] + 1)

def add_student(student: "Student") -> str:
    data: dict[str, list] = read_data()
    for temp_student in data['students']:    
        if student.email == temp_student['email']:
            raise DuplicateEmailError()
    
    new_student = {
        **student.model_dump(),
        "subjects": []
    }
    
    data['students'].append(new_student)
    write_data(data)
    return f"Student added with ID {new_student['id']}"


def list_students() -> list[str]:
    data: dict[str, list] = read_data()
    output = []
    for student in data['students']:
        output.append(f"{student['id']}- {student['name']} ({student['email']}, age {student['age']})")
    return output


def validate_id(student_id: int) -> bool:
    data: dict = read_data()
    for student in data['students']:
        if student['id'] == student_id:
            return True
    raise StudentNotFoundError()


def show_student(student_id: int) -> list[str]:
    validate_id(student_id)
    data: dict[str, list] = read_data()
    
    for student in data['students']:
        if student_id == student['id']:
            output = [f"{student['name']} ({student['email']}, age {student['age']})"]
            if len(student['subjects']):
                output.append("Grades: ")
                for subject in student['subjects']:
                    output.append(f"{subject['subject-name']} - {subject['score']}")
            return output
    return []  

def delete_student(student_id: int) -> str:
    validate_id(student_id)
    data: dict[str, list] = read_data()
    
    for ind, student in enumerate(data['students']):
        if student_id == student['id']:
            data['students'].pop(ind)
            write_data(data)
            return f"Student {student_id} and their grades deleted"
    return ""

def student_report(student_id: int) -> str:
    validate_id(student_id)
    data: dict[str, list] = read_data()
    
    for student in data['students']:
        if student_id == student['id']:
            num_grades = len(student['subjects'])
            if num_grades == 0:
                return f"{student['name']} — 0 grades"
            
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
            
            average = total / num_grades
            return f"{student['name']} — {num_grades} grades, average: {average:.2f}, highest: {highest} ({highest_name}), lowest: {lowest} ({lowest_name})"
    
    return "" 


def update_student(student_id: int, fields: list, values: list) -> str:
    validate_id(student_id)
    data: dict[str, list] = read_data()
    
    for ind, student in enumerate(data['students']):
        if student['id'] == student_id:
            temp_instance: dict = {
                "name": student['name'],
                "email": student['email'],
                "age": student['age']
            }
            
            for field, value in zip(fields, values):
                if field == '--name':
                    temp_instance['name'] = value
                elif field == '--email':
                    for s in data['students']:
                        if value == s['email'] and s['id'] != student_id:
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
            return f"Student {student_id} updated"
    
    return ""


def class_report() -> list[str]:
    data = read_data()
    total_students = len(data['students'])
    
    if total_students == 0:
        return ["No students available"]

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
            "name": student['name'],
            "average": cur_avg,
        }
        averages.append(average)
    
    total_avg = total_avg / total_students
    averages = sorted(averages, key=lambda x: x['average'], reverse=True)

    output = []
    output.append(f"Total Students: {total_students}")
    output.append(f"Class average: {total_avg:.2f}")
    
    top_n = min(3, total_students)
    if total_students >= 2:
        output.append(f"Top {top_n} students: ")
    else:
        output.append("The only student: ")
    
    positions = ["1st-student", "2nd-student", "3rd-student"]
    for i in range(top_n):
        output.append(f" {positions[i]}: ")
        output.append(f"    {averages[i]['name']}, average: {averages[i]['average']:.2f}")
    
    return output


def import_students(csv_file: str) -> str:
    imported = 0
    skipped = 0
    
    with open(csv_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for row in spamreader:
            if len(row) != 3:
                skipped += 1
                continue
            
            name, email, age_str = row
            name = name.strip()
            email = email.strip()
            
            try:
                age = int(age_str.strip())
                student = Student(id=get_new_id(), name=name, email=email, age=age)
                try:
                    add_student(student)
                    imported += 1
                except (DuplicateEmailError, ValueError):
                    skipped += 1
            except ValueError:
                skipped += 1
    
    return f"Imported {imported} students, {skipped} rows skipped (invalid data)"


def add_grade(grade: "Grade") -> str:
    data: dict[str, list] = read_data()
    
    for ind, student in enumerate(data['students']):
        if student['id'] == grade.student_id:
            subject: dict = {
                "subject-name": grade.subject,
                "score": grade.score
            }
            data['students'][ind]['subjects'].append(subject)
            write_data(data)
            return f"Grade added for student {grade.student_id}"
    
    raise StudentNotFoundError()