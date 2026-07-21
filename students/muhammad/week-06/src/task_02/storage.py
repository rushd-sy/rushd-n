import json

def save_books(books: list[dict]) -> None:
    with open("books.json", "w") as file:
        json.dump(books, file, indent=4)

def load_books() -> list[dict]:
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        save_books([])
        books = []
    return books




def save_authors(books: list[dict]) -> None:
    with open("authors.json", "w") as file:
        json.dump(books, file, indent=4)

def load_authors() -> list[dict]:
    try:
        with open("authors.json", "r") as file:
            authors = json.load(file)
    except FileNotFoundError:
        save_books([])
        authors = []
    return authors




def save_loans(books: list[dict]) -> None:
    with open("loans.json", "w") as file:
        json.dump(books, file, indent=4)

def load_loans() -> list[dict]:
    try:
        with open("loans.json", "r") as file:
            loans = json.load(file)
    except FileNotFoundError:
        save_books([])
        loans = []
    return loans
