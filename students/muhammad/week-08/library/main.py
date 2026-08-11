from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.authors import router as authors_router
from routers.books import router as books_router
from routers.loans import router as loans_router
from exceptions import BookNotFoundError
from middlewares.logging import UUIDLoggerMiddleWare, LoggerMiddleWare

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(loans_router)

app.add_middleware(UUIDLoggerMiddleWare)
app.add_middleware(LoggerMiddleWare)

@app.exception_handler(BookNotFoundError)
async def book_not_found_error_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "details" : f"Book with id {exc.book_id} doesn't exist"
        }
    )

