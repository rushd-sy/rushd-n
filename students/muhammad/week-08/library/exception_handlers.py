from fastapi import Request
from fastapi.responses import JSONResponse
from typing import cast

from exceptions import (
    BookNotFoundError,
    LoanNotFoundError,
    AuthorNotFoundError,
)


async def book_not_found_error_handler(
    request: Request,
    exc: Exception
):
    exc = cast(BookNotFoundError, exc)
    return JSONResponse(
        status_code=404,
        content={
            "details": f"Book with id {exc.book_id} doesn't exist"
        }
    )


async def loan_not_found_error_handler(
    request: Request,
    exc: Exception
):
    exc = cast(LoanNotFoundError, exc)
    return JSONResponse(
        status_code=404,
        content={
            "details": f"Loan with id {exc.loan_id} doesn't exist"
        }
    )


async def author_not_found_error_handler(
    request: Request,
    exc: Exception
):
    exc = cast(AuthorNotFoundError, exc)
    return JSONResponse(
        status_code=404,
        content={
            "details": f"Author with id {exc.author_id} doesn't exist"
        }
    )