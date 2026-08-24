from fastapi import FastAPI

from routers.authors import router as authors_router
from routers.books import router as books_router
from routers.loans import router as loans_router
from routers.auth import router as auth_router
from exceptions import (
    BookNotFoundError,
    LoanNotFoundError,
    AuthorNotFoundError,
    DuplicateEmailError,
    DuplicateUsernameError, 
    InvalidCredentialsError
)
from exception_handlers import (
    book_not_found_error_handler,
    author_not_found_error_handler,
    loan_not_found_error_handler,
    duplicate_email_handler, 
    duplicate_username_handler,
    invalid_credentials_handler
)
from middlewares.logging import UUIDLoggerMiddleWare, LoggerMiddleWare

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(loans_router)
app.include_router(auth_router)

app.add_middleware(UUIDLoggerMiddleWare)
app.add_middleware(LoggerMiddleWare)

app.add_exception_handler(BookNotFoundError, book_not_found_error_handler)
app.add_exception_handler(LoanNotFoundError, loan_not_found_error_handler)
app.add_exception_handler(AuthorNotFoundError, author_not_found_error_handler)
app.add_exception_handler(AuthorNotFoundError, author_not_found_error_handler)
app.add_exception_handler(DuplicateUsernameError, duplicate_username_handler)
app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
