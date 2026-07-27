from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.authors import router as authors_router
from routers.loans import router as loans_router
from routers.books import router as books_router
from fastapi.exception_handlers import http_exception_handler
from exceptions import BookNotFoundError

app = FastAPI()
app.include_router(authors_router, prefix="/authors", tags=["authors"])
app.include_router(loans_router, prefix="/loans", tags=["loans"])
app.include_router(books_router, prefix="/books", tags=["books"])

@app.exception_handler(BookNotFoundError)
async def Book_Not_Found(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Book {exc.book_id} not found"}
    )

@app.get("/")
async def root():
    return {"message": "running"}
