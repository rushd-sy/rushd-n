from fastapi import FastAPI, Path, Query
from routers.authors import router as authors_router
from routers.loans import router as loans_router
from routers.books import router as books_router

app = FastAPI()
app.include_router(authors_router, prefix="/authors", tags=["authors"])
app.include_router(loans_router, prefix="/loans", tags=["loans"])
app.include_router(books_router, prefix="/books", tags=["books"])

@app.get("/")
async def root():
    return {"message": "running"}
