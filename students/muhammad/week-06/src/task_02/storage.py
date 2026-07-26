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




def save_authors(authors: list[dict]) -> None:
    with open("authors.json", "w") as file:
        json.dump(authors, file, indent=4)

def load_authors() -> list[dict]:
    try:
        with open("authors.json", "r") as file:
            authors = json.load(file)
    except FileNotFoundError:
        save_authors([])
        authors = []
    return authors




def save_loans(loans: list[dict]) -> None:
    with open("loans.json", "w") as file:
        json.dump(loans, file, indent=4)

def load_loans() -> list[dict]:
    try:
        with open("loans.json", "r") as file:
            loans = json.load(file)
    except FileNotFoundError:
        save_loans([])
        loans = []
    return loans
