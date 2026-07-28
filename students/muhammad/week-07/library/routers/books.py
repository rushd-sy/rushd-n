from fastapi import APIRouter, Path, Depends
from typing import Annotated

from models.page import Page
from models.books import BookResponse, BookCreate
from dependencies import get_pagination_params, get_current_user
from services.book_services import BookServices

router = APIRouter(prefix="/books")


@router.get('/')
async def get_books(
        pagination_params: Annotated[dict, Depends(get_pagination_params)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        author : str | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
    ) -> Page[BookResponse]:
    
    """
        A cool docstring
    """
    
    return book_service.get_books(
        author=author,
        genre=genre,
        min_publish_year=min_publish_year,
        offset=pagination_params['offset'],
        limit=pagination_params['limit']
    )



@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
        book_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[str, Depends(get_current_user)],
        book_service: Annotated[BookServices, Depends(BookServices)]
    ) -> BookResponse:
    return book_service.get_book_by_id(book_id=book_id)

@router.post("/", response_model=BookResponse)
async def create_book(request_book: BookCreate, book_service: Annotated[BookServices, Depends(BookServices)]) -> BookResponse:
    return book_service.create_book(request_book)


@router.delete("/{book_id}")
async def delete_book(book_id: Annotated[int, Path(gt=0)], book_service: Annotated[BookServices, Depends(BookServices)]) -> None:
    book_service.delete_book(book_id)
