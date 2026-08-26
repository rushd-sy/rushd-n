from fastapi import APIRouter, BackgroundTasks, Path, Depends
from typing import Annotated
import asyncio 

from models.page_models import Page
from models.books_models import BookResponse, BookCreate
from dependencies import get_pagination_params, get_current_user_id
from services.book_services import BookServices
from middlewares.logging import logger

router = APIRouter(prefix="/books")


@router.get('/')
async def get_books(
        pagination_params: Annotated[dict, Depends(get_pagination_params)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
        author : str | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
    ) -> Page[BookResponse]:
    
    """
        A cool docstring
    """
    
    return await book_service.get_books(
        author=author,
        genre=genre,
        min_publish_year=min_publish_year,
        offset=pagination_params['offset'],
        limit=pagination_params['limit']
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
        book_id: Annotated[int, Path(gt=0)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    return await book_service.get_book_by_id(book_id=book_id)


async def write_notification():
    await asyncio.sleep(2)
    logger.info("Email sent successfully.")

@router.post("/", response_model=BookResponse)
async def create_book(
        request_book: BookCreate,
        book_service: Annotated[BookServices, Depends(BookServices)],
        background_tasks: BackgroundTasks,
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    response = await book_service.create_book(request_book)
    background_tasks.add_task(write_notification)
    return response

@router.put("/{book_id}")
async def update_book(
        book_id: Annotated[int, Path(gt=0)], 
        request_book: BookCreate,
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:

    return await book_service.update_book(book_id, request_book)

@router.delete("/{book_id}")
async def delete_book(
        book_id: Annotated[int, Path(gt=0)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    return await book_service.delete_book(book_id)
