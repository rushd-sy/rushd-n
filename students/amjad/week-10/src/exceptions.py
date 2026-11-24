class BookNotFoundError(Exception):
    def __init__(self, book_id: int) -> None:
        self.book_id = book_id
