from fastapi import HTTPException, Path, APIRouter
from typing import Annotated

from datetime import datetime
from models import LoanCreate, LoanOut, Loan, Page
from storage import load_loans, save_loans
from dependency import CommonsDepForPagination, CurrentUserDep

router = APIRouter()


@router.get("/", response_model=Page[LoanOut])
async def get_loans(
    commons: CommonsDepForPagination,
    loan_date: str | None = None,
) -> Page[LoanOut]:
    """
    Retrieve a list of loans with optional filters.
    - **loan_date**: Filter loans by the date they were made.
    - **offset**: The number of items to skip before starting to collect the result set.
    - **limit**: The maximum number of items to return (default is 10, maximum is 20).
    """
    loans = load_loans()
    loans_out = []
    for loan in loans:
        if loan_date and loan["loan_date"] != loan_date:
            continue
        loans_out.append(LoanOut(**loan))
    
    total = len(loans_out)
    offset = commons["offset"]
    limit = commons["limit"]
    loans_out = loans_out[offset:offset + limit]
    return Page[LoanOut](items=loans_out, total=total, offset=offset, limit=limit)

@router.post("/", response_model=LoanOut)
async def create_loan(loan: LoanCreate, user_id: CurrentUserDep) -> LoanOut:
    """
    Create a new loan.
    - **loan**: The details of the loan to create.
    - **user_id**: The ID of the user creating the loan.
    - Returns the created loan details.
    """
    if user_id is None:
        raise HTTPException(status_code=403, detail="unauthorized")
    loans = load_loans()    
    created_at = datetime.now().isoformat()
    new_loan = Loan(loan_id=max([stored_loan["loan_id"] for stored_loan in loans], default=0) + 1, **loan.model_dump(), loan_date=created_at)
    loans.append(new_loan.model_dump())
    save_loans(loans)
    return LoanOut(**new_loan.model_dump())
    

@router.delete("/{loan_id}", response_model=LoanOut)
async def delete_loan(loan_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep) -> LoanOut:
    """
    Delete a loan by its ID.
    - **loan_id**: The ID of the loan to delete and must be a positive integer.
    - **user_id**: The ID of the user deleting the loan.
    - Returns the deleted loan details if found, otherwise raises a 404 error.
    """
    if user_id is None:
        raise HTTPException(status_code=403, detail="unauthorized")
    loans = load_loans()
    for i, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            deleted_loan = LoanOut(**loans[i])
            loans.pop(i)
            save_loans(loans)
            return deleted_loan
    raise HTTPException(status_code=404, detail="Loan not found")

@router.get("/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: Annotated[int, Path(gt=0)]) -> LoanOut:
    """
    Retrieve a loan by its ID.
    - **loan_id**: The ID of the loan to retrieve and must be a positive integer.
    - Returns the loan details if found, otherwise raises a 404 error.
    """
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanOut(**loan)
    raise HTTPException(status_code=404, detail="Loan not found")

@router.put("/{loan_id}", response_model=LoanOut)
async def update_loan(loan_id: Annotated[int, Path(gt=0)], loan: LoanCreate, user_id: CurrentUserDep) -> LoanOut:
    """
    Update an existing loan.
    - **loan_id**: The ID of the loan to update and must be a positive integer.
    - **loan**: The updated details of the loan.
    - **user_id**: The ID of the user updating the loan.
    - Returns the updated loan details if found, otherwise raises a 404 error.
    """
    if user_id is None:
        raise HTTPException(status_code=403, detail="unauthorized")
    loans = load_loans()
    for i, l in enumerate(loans):
        if l["loan_id"] == loan_id:
            updated_loan = Loan(loan_id=loan_id, **loan.model_dump(), loan_date=l["loan_date"])
            loans[i] = updated_loan.model_dump()
            save_loans(loans)
            return LoanOut(**loans[i])
    raise HTTPException(status_code=404, detail="Loan not found")