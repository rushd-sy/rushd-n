from fastapi import Depends, Path, APIRouter
from typing import Annotated
from datetime import datetime

from models import LoanCreate, LoanOut, Page
from dependency import CommonsDepForPagination, CurrentUserDep
from services.loan_service import LoanService

router = APIRouter()


# `async def` because they perform I/O operations
@router.get("/", response_model=Page[LoanOut])
async def get_loans(
    commons: CommonsDepForPagination,
    service: LoanService = Depends(LoanService),
    loan_date: datetime | None = None,
) -> Page[LoanOut]:
    """
    Retrieve a list of loans with optional filters.
    - **loan_date**: Filter loans by the date they were made.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    return await service.get_loans(commons, loan_date)


# `async def` because they perform I/O operations
@router.post("/", response_model=LoanOut)
async def create_loan(
    loan: LoanCreate,
    user_id: CurrentUserDep,
    service: LoanService = Depends(LoanService),
) -> LoanOut:
    """
    Create a new loan.
    - **loan**: The details of the loan to create.
    - **user_id**: The ID of the user creating the loan.
    - Returns the created loan details.
    """
    return await service.create_loan(loan, user_id)


# `async def` because they perform I/O operations
@router.delete("/{loan_id}", response_model=LoanOut)
async def delete_loan(
    loan_id: Annotated[int, Path(gt=0)],
    user_id: CurrentUserDep,
    service: LoanService = Depends(LoanService),
) -> LoanOut:
    """
    Delete a loan by its ID.
    - **loan_id**: The ID of the loan to delete and must be a positive integer.
    - **user_id**: The ID of the user deleting the loan.
    - Returns the deleted loan details if found, otherwise raises a 404 error.
    """
    return await service.delete_loan(loan_id, user_id)


# `async def` because they perform I/O operations
@router.get("/{loan_id}", response_model=LoanOut)
async def get_loan(
    loan_id: Annotated[int, Path(gt=0)], service: LoanService = Depends(LoanService)
) -> LoanOut:
    """
    Retrieve a loan by its ID.
    - **loan_id**: The ID of the loan to retrieve and must be a positive integer.
    - Returns the loan details if found, otherwise raises a 404 error.
    """
    return await service.get_loan(loan_id)


# `async def` because they perform I/O operations
@router.put("/{loan_id}", response_model=LoanOut)
async def update_loan(
    loan_id: Annotated[int, Path(gt=0)],
    loan: LoanCreate,
    user_id: CurrentUserDep,
    service: LoanService = Depends(LoanService),
) -> LoanOut:
    """
    Update an existing loan.
    - **loan_id**: The ID of the loan to update and must be a positive integer.
    - **loan**: The updated details of the loan.
    - **user_id**: The ID of the user updating the loan.
    - Returns the updated loan details if found, otherwise raises a 404 error.
    """
    return await service.update_loan(loan_id, loan, user_id)
