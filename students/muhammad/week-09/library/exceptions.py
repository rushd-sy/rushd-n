class BookNotFoundError(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id

class LoanNotFoundError(Exception):
    def __init__(self, loan_id: int):
        self.loan_id = loan_id

class AuthorNotFoundError(Exception):
    def __init__(self, author_id: int):
        self.author_id = author_id

class DuplicateUsernameError(Exception):
    def __init__(self, username: str):
        self.username = username

class DuplicateEmailError(Exception):
    def __init__(self, email: str):
        self.email = email
