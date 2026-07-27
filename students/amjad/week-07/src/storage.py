import json

def load_books() -> list[dict]:
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []

        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(books, f)

    return books
    
def save_books(books: list[dict]) -> None:
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4)


def load_loans() -> list[dict]:
    try:
        with open("loans.json", "r", encoding="utf-8") as f:
            loans = json.load(f)
    except FileNotFoundError:
        loans = []

        with open("loans.json", "w", encoding="utf-8") as f:
            json.dump(loans, f)

    return loans

def save_loans(loans: list[dict]) -> None:
    with open("loans.json", "w", encoding="utf-8") as f:
        json.dump(loans, f, indent=4)


def load_authors() -> list[dict]:
    try:
        with open("authors.json", "r", encoding="utf-8") as f:
            authors = json.load(f)
    except FileNotFoundError:
        authors = []

        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump(authors, f)

    return authors
    
def save_authors(authors: list[dict]) -> None:
    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, indent=4)

