class BookNotFoundError(Exception):
    def __intit__(self, book_id: int):
        self.book_id = book_id

