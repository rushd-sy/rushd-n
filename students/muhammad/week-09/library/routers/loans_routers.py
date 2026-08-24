from fastapi import APIRouter, Path, Depends
from typing import Annotated
from models.loans_models import LoanResponse, LoanCreate
from datetime import date

from models.page_models import Page
from dependencies import get_pagination_params, get_current_user
from services.loan_services import LoanServices
router = APIRouter(prefix="/loans")


@router.get("/")
async def get_loans(
    loan_services: Annotated[LoanServices, Depends(LoanServices)],
    pagination_params: Annotated[dict, Depends(get_pagination_params)],
    name: str | None = None,
    loan_date: date | None = None,
    min_date: date | None = None,
    max_date: date | None = None,
    ) -> Page[LoanResponse]:
    
    return await loan_services.get_loans(
        name=name,
        loan_date=loan_date,
        min_date=min_date,
        max_date=max_date,
        offset=pagination_params['offset'],
        limit=pagination_params['limit']
    )



@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        loan_id: Annotated[int, Path(gt=0)],
    ):
    return await loan_services.get_loan_by_id(loan_id)

@router.post("/", response_model=LoanResponse)
async def create_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        request_loan: LoanCreate,
        user_id: Annotated[str, Depends(get_current_user)],
    ):
    return await loan_services.create_loan(request_loan)


@router.put("/{loan_id}", response_model=LoanResponse)
async def update_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        loan_id: Annotated[int, Path(gt=0)],
        request_loan: LoanCreate,
        user_id: Annotated[str, Depends(get_current_user)],
    ):
    return await loan_services.update_loan(loan_id, request_loan)



@router.delete("/{loan_id}")
async def delete_loan(
        loan_services: Annotated[LoanServices, Depends(LoanServices)],
        loan_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[str, Depends(get_current_user)],
    ) -> LoanResponse:
    return await loan_services.delete_loan(loan_id)
