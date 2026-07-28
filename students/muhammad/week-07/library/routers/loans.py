from fastapi import APIRouter, Path, HTTPException, Depends
from typing import Annotated
from models.loans import LoanModel, LoanResponse, LoanCreate
from datetime import datetime

from utils.storage import load_loans, save_loans
from models.page import Page
from dependencies import get_pagination_params, get_current_user

router = APIRouter(prefix="/loans")


@router.get("/")
async def get_loans(
    pagination_params: Annotated[dict, Depends(get_pagination_params)],
    name: str | None = None,
    date: str | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    ) -> Page[LoanResponse]:
    
    loans = load_loans()
    loans_out = []
    offset = pagination_params['offset']
    limit = pagination_params['limit']
    
    for dict_loan in loans:
        loan = LoanResponse(**dict_loan)
        if name and loan.name != name:
            continue
        if date and loan.date != date:
            continue
        if min_date and loan.date < min_date:
            continue
        if max_date and loan.date > max_date:
            continue
        loans_out.append(loan)
    
    total = len(loans_out)
    loans_out = loans_out[offset:offset + limit]
    
    return Page[LoanResponse](
        items=loans_out,
        total=total,
        offset=offset,
        limit=limit
    )


@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
        loan_id: Annotated[int, Path(gt=0)],
        user_id: Annotated[str, Depends(get_current_user)]
    ):
    
    loans = load_loans()
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return LoanResponse(**loan)
    raise HTTPException(status_code=404, detail="Loan not found")


@router.post("/", response_model=LoanResponse)
async def create_loan(request_loan: LoanCreate):
    loans = load_loans()

    created_loan = LoanModel(
        loan_id=max([loan["loan_id"] for loan in loans], default=0) + 1,
        **request_loan.model_dump(),
        added_at=datetime.now().isoformat(),
    )
    loans.append(created_loan.model_dump())
    save_loans(loans)

    return LoanResponse(
        **created_loan.model_dump(),
    )


@router.put("/{loan_id}", response_model=LoanResponse)
async def update_loan(
    loan_id: Annotated[int, Path(gt=0)],
    request_loan: LoanCreate
    ):
    loans = load_loans()
    
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            existing = LoanModel(**loan)
            updated_loan = LoanModel(
                loan_id=loan_id,
                **request_loan.model_dump(),
                added_at=existing.added_at,
            )
            
            loans[index] = updated_loan.model_dump()
            save_loans(loans)
            
            return LoanResponse(
                **updated_loan.model_dump()
            )
    
    raise HTTPException(status_code=404, detail="Loan not found")


@router.delete("/{loan_id}")
async def delete_loan(loan_id: Annotated[int, Path(gt=0)]) -> None:
    loans = load_loans()
    for index, loan in enumerate(loans):
        if loan["loan_id"] == loan_id:
            del loans[index]
            save_loans(loans)
            return
    
    raise HTTPException(status_code=404, detail="Loan not found")
