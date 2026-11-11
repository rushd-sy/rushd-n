
from fastapi import HTTPException, Path
from typing import Annotated

from datetime import datetime

from sqlalchemy import func, select, func
from models import LoanCreate, LoanOut, Page
from db.db_models.Loan import Loan as DBLoan
from dependency import CommonsDepForPagination, CurrentUserDep, CommonsDepForDB

class LoanService:
    def __init__(self, db: CommonsDepForDB) -> None:
        self.db = db

    async def get_loans(
        self,
        commons: CommonsDepForPagination,
        loan_date: datetime | None = None,
    ) -> Page[LoanOut]:
        offset = commons.offset
        limit = commons.limit
        query = select(DBLoan)
        if loan_date is not None:
            query = query.where(func.date(DBLoan.loan_date) == loan_date.date())
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()
        result = await self.db.execute(query.order_by(DBLoan.loan_id).offset(offset).limit(limit))
        db_loans = result.scalars().all()
        loans_out = [LoanOut.model_validate(loan) for loan in db_loans]
        return Page[LoanOut](items=loans_out, total=total, offset=offset, limit=limit)

    async def create_loan(self, loan: LoanCreate, user_id: CurrentUserDep) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        new_loan = DBLoan(
            book_id=loan.book_id,
            user_id=user_id,
            loan_date=datetime.now(),
            return_date=loan.return_date,
        )
        self.db.add(new_loan)
        await self.db.commit()
        await self.db.refresh(new_loan)
        return LoanOut.model_validate(new_loan)

    async def delete_loan(
        self, loan_id: Annotated[int, Path(gt=0)], user_id: CurrentUserDep
    ) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBLoan).where(DBLoan.loan_id == loan_id)
        result = await self.db.execute(query)
        db_loan = result.scalar_one_or_none()
        if not db_loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        loan_out = LoanOut.model_validate(db_loan)
        await self.db.delete(db_loan)
        await self.db.commit()
        return loan_out

    async def get_loan(self, loan_id: Annotated[int, Path(gt=0)]) -> LoanOut:
        query = select(DBLoan).where(DBLoan.loan_id == loan_id)
        result = await self.db.execute(query)
        db_loan = result.scalar_one_or_none()
        if not db_loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return LoanOut.model_validate(db_loan)

    async def update_loan(
        self,
        loan_id: Annotated[int, Path(gt=0)],
        loan: LoanCreate,
        user_id: CurrentUserDep,
    ) -> LoanOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        query = select(DBLoan).where(DBLoan.loan_id == loan_id)
        result = await self.db.execute(query)
        db_loan = result.scalar_one_or_none()
        if not db_loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        db_loan.book_id = loan.book_id
        db_loan.user_id = user_id
        db_loan.return_date = loan.return_date
        await self.db.commit()
        await self.db.refresh(db_loan)
        return LoanOut.model_validate(db_loan)
