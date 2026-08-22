from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.authors import router as authors_router
from routers.loans import router as loans_router
from routers.books import router as books_router
from routers.auth import router as auth_router
from routers.httpx_async import router as httpx_async_router
from exceptions import BookNotFoundError
from middlewares import log_requests, add_request_id
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_request_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authors_router, prefix="/authors", tags=["authors"])
app.include_router(loans_router, prefix="/loans", tags=["loans"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(httpx_async_router, prefix="/async_test", tags=["async_test"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.exception_handler(BookNotFoundError)
async def Book_Not_Found(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404, content={"message": f"Book {exc.book_id} not found"}
    )


@app.get("/")
async def root():
    return {"message": "running"}
