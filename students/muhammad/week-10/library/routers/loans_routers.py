from fastapi import APIRouter, Path, Depends
from typing import Annotated
from models.loans import LoanResponse, LoanCreate
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.page import Page
from dependencies import get_pagination_params, get_current_user_id
from services.loan_services import LoanServices
router = APIRouter(prefix="/loans")


@router.get("/")
async def get_loans(
    loan_services: Annotated[LoanServices, Depends(LoanServices)],
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination_params: Annotated[dict, Depends(get_pagination_params)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    book_id: int | None = None,
    min_date: date | None = None,
    max_date: date | None = None,
) -> Page[LoanResponse]:

    return await loan_services.get_loans(
        db=db,
        user_id=user_id,
        book_id=book_id,
        min_date=min_date,
        max_date=max_date,
        offset=pagination_params['offset'],
        limit=pagination_params['limit']
    )



@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        db: Annotated[AsyncSession, Depends(get_db)],
        loan_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[int, Depends(get_current_user_id)],
    ):
    
    return await loan_services.get_loan_by_id(
        db=db,
        loan_id=loan_id,
        user_id=user_id
    )

@router.post("/", response_model=LoanResponse)
async def create_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        db: Annotated[AsyncSession, Depends(get_db)],
        request_loan: LoanCreate,
        user_id: Annotated[int, Depends(get_current_user_id)],
    ):
    return await loan_services.create_loan(
        db=db,
        request_loan=request_loan,
        user_id=user_id
    )


@router.put("/{loan_id}", response_model=LoanResponse)
async def update_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        db: Annotated[AsyncSession, Depends(get_db)],
        loan_id: Annotated[int, Path(gt=0)],
        request_loan: LoanCreate,
        user_id: Annotated[int, Depends(get_current_user_id)],
    ):
    return await loan_services.update_loan(
        db=db,
        loan_id=loan_id,
        request_loan=request_loan,
        user_id=user_id
    )



@router.delete("/{loan_id}")
async def delete_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        db: Annotated[AsyncSession, Depends(get_db)],
        loan_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[int, Depends(get_current_user_id)],
    ) -> LoanResponse:
    return await loan_services.delete_loan(
        db=db,
        loan_id=loan_id,
        user_id=user_id,
    )
