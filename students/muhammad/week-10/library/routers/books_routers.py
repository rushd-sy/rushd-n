from fastapi import APIRouter, BackgroundTasks, Path, Depends
from typing import Annotated
import asyncio 
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.page import Page
from models.books import BookResponse, BookCreate
from dependencies import get_pagination_params, get_current_user_id
from services.book_services import BookServices
from middlewares.logging import logger

router = APIRouter(prefix="/books")


@router.get('/')
async def get_books(
        pagination_params: Annotated[dict, Depends(get_pagination_params)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        db: Annotated[AsyncSession, Depends(get_db)],
        user_id: Annotated[str, Depends(get_current_user_id)],
        author_id : int | None = None,
        genre : str | None = None,
        min_publish_year : int | None = None,
        max_publish_year : int | None = None,
    ) -> Page[BookResponse]:
    
    return await book_service.get_books(
        db=db,
        author_id=author_id,
        genre=genre,
        min_publish_year=min_publish_year,
        max_publish_year=max_publish_year,
        offset=pagination_params['offset'],
        limit=pagination_params['limit']
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
        db: Annotated[AsyncSession, Depends(get_db)],
        book_id: Annotated[int, Path(gt=0)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    
    return await book_service.get_book_by_id(db, book_id=book_id)


async def write_notification():
    await asyncio.sleep(2)
    logger.info("Email sent successfully.")

@router.post("/", response_model=BookResponse)
async def create_book(
        request_book: BookCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        background_tasks: BackgroundTasks,
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    response = await book_service.create_book(db, request_book)
    background_tasks.add_task(write_notification)
    return response

@router.put("/{book_id}")
async def update_book(
        db: Annotated[AsyncSession, Depends(get_db)],
        book_id: Annotated[int, Path(gt=0)], 
        request_book: BookCreate,
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:

    return await book_service.update_book(db, book_id, request_book)

@router.delete("/{book_id}")
async def delete_book(
        db: Annotated[AsyncSession, Depends(get_db)],
        book_id: Annotated[int, Path(gt=0)],
        book_service: Annotated[BookServices, Depends(BookServices)],
        user_id: Annotated[str, Depends(get_current_user_id)],
    ) -> BookResponse:
    return await book_service.delete_book(db, book_id)
