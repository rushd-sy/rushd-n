import logging
import uuid

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start_time)
    logging.info(f"{request.method} {request.url.path} {response.status_code} {duration}ms")
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logging.info(f"Request ID: {request_id} - {request.method} {request.url.path}")
    return response

@app.get("/")
async def root():
    return {"message": "running"}
