"""
Custom exceptions:
    StudentNotFoundError
    DuplicateEmailError
    WrongCommandError
"""

class StudentNotFoundError(Exception):
    
    def __init__(self) -> None:
        self.message = "Student ID is not valid"
        super().__init__(self.message)

class DuplicateEmailError(Exception):
    
    def __init__(self) -> None:
        self.message = "Email already exists"
        super().__init__(self.message)


wrong_commands_message = """The command is invalid.
Available commands:
    add-student <name> <email> <age>
    list-students
    show-student <id>
    update-student <id> --name/--email/--age
    delete-student <id>
    add-grade <student_id> <subject> <score>
    student-report <id>
    import-students <csv_file>
"""

class WrongCommandError(Exception):

    def __init__(self) -> None:
        self.message=wrong_commands_message
        super().__init__(self.message)
