from fastapi import HTTPException, Path
from typing import Annotated

from datetime import datetime
from models import LoanCreate, LoanOut, Loan, Page
from storage import load_loans, save_loans
from dependency import CommonsDepForPagination, CurrentUserDep


class LoanService:

    async def get_loans(
        self,
        commons: CommonsDepForPagination,
        loan_date: datetime | None = None,
    ) -> Page[LoanOut]:
        loans = await load_loans()
        loans_out = []
        for loan in loans:
            if loan_date and loan.loan_date != loan_date.isoformat():
                continue
            loans_out.append(LoanOut(**loan.model_dump()))

        total = len(loans_out)
        offset = commons.offset
        limit = commons.limit
        loans_out = loans_out[offset:offset + limit]
        return Page[LoanOut](items=loans_out, total=total, offset=offset, limit=limit)

    async def create_loan(self, loan: LoanCreate, user_id: CurrentUserDep) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        loans = await load_loans()    
        loan_date = datetime.now().isoformat()
        new_loan = Loan(
            loan_id=max([stored_loan.loan_id for stored_loan in loans], default=0) + 1, 
            book_id=loan.book_id,
            user_id=loan.user_id,
            loan_date=loan_date,
            return_date=loan.return_date.isoformat()
            )
        loans.append(new_loan)
        await save_loans(loans)
        return LoanOut(**new_loan.model_dump())


    async def delete_loan(self, loan_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        loans = await load_loans()
        for i, loan in enumerate(loans):
            if loan.loan_id == loan_id:
                deleted_loan = LoanOut(**loans[i].model_dump())
                loans.pop(i)
                await save_loans(loans)
                return deleted_loan
        raise HTTPException(status_code=404, detail="Loan not found")

    async def get_loan(self, loan_id: Annotated[int, Path(gt=0)]) -> LoanOut:
        loans = await load_loans()
        for loan in loans:
            if loan.loan_id == loan_id:
                return LoanOut(**loan.model_dump())
        raise HTTPException(status_code=404, detail="Loan not found")

    async def update_loan(self, loan_id: Annotated[int, Path(gt=0)], loan: LoanCreate, user_id: CurrentUserDep) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        loans = await load_loans()
        for i, l in enumerate(loans):
            if l.loan_id == loan_id:
                updated_loan = Loan(
                    loan_id=loan_id,
                    book_id=loan.book_id,
                    user_id=loan.user_id,
                    loan_date=l.loan_date,
                    return_date=loan.return_date.isoformat()
                )
                loans[i] = updated_loan
                await save_loans(loans=loans)
                return LoanOut(**loans[i].model_dump())
        raise HTTPException(status_code=404, detail="Loan not found")
