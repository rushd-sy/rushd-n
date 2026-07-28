from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import uuid

from routers.authors import router as authors_router
from routers.books import router as books_router
from routers.loans import router as loans_router
from exceptions import BookNotFoundError

app = FastAPI()
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(loans_router)

@app.exception_handler(BookNotFoundError)
async def book_not_found_error_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content=f"Book with id {exc.book_id} doesn't exist"
    )


@app.middleware("http")
async def logger(request: Request, call_next):
    beginning = time.perf_counter()
    response = await call_next(request)
    total_time = time.perf_counter() - beginning
    print(f"""---New Request---
Request Method: {request.method}
Request Path: {request.url.path}
Response Code: {response.status_code}
Duration: {total_time}
""")
    return response

@app.middleware("http")
async def uuid_logger(request: Request, call_next):
    request_id = uuid.uuid4()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(request_id)
    print(f"Request ID: {request_id}")
    return response
