from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from database.models.loans import Loan
from database.models.books import Book
from models.loans import LoanCreate, LoanResponse
from models.page import Page
from exceptions import LoanNotFoundError, BookNotFoundError

class LoanServices:

    async def get_loans(
            self,
            db: AsyncSession,
            user_id: int,
            book_id: int | None = None,
            min_date: date | None = None,
            max_date: date | None = None,
            offset: int = 0,
            limit: int = 20
        ) -> Page[LoanResponse]:

        conditions = [Loan.user_id == user_id]
        
        if min_date is not None and max_date is not None:
            if min_date > max_date:
                raise HTTPException(
                    status_code=422,
                    detail="min_date cannot be later than max_date"
                )
                
        if book_id is not None:
            conditions.append(Loan.book_id == book_id)
        
        if min_date is not None:
            conditions.append(Loan.loan_date >= min_date)
        
        if max_date is not None:
            conditions.append(Loan.loan_date <= max_date)
        
        total = await db.scalar(
            select(func.count(Loan.loan_id))
            .where(*conditions)
        )
        
        result = await db.scalars(
            select(Loan)
            .where(*conditions)
            .order_by(Loan.loan_id)
            .offset(offset)
            .limit(limit)
        )
        
        loans = result.all()
        
        return Page[LoanResponse] (
            items=[
                LoanResponse.model_validate(loan)
                for loan in loans
            ],
            total=total or 0,
            offset=offset,
            limit=limit
        )
    
    async def get_loan_by_id(
        self, 
        db: AsyncSession, 
        loan_id: int,
        user_id: int,
    ) -> LoanResponse:
        
        loan = await db.scalar(
            select(Loan)
            .where(
                Loan.user_id == user_id,
                Loan.loan_id==loan_id
            )
        )
        
        if loan is None:
            raise LoanNotFoundError(loan_id)
        
        return LoanResponse.model_validate(loan)
    
    async def create_loan(
        self,
        db: AsyncSession,
        user_id: int,
        request_loan: LoanCreate
    ) -> LoanResponse:

        book = await db.get(Book, request_loan.book_id)

        if book is None:
            raise BookNotFoundError(request_loan.book_id)

        new_loan = Loan(
            book_id=request_loan.book_id,
            user_id=user_id,
            loan_date=request_loan.loan_date
        )

        db.add(new_loan)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        await db.refresh(new_loan)

        return LoanResponse.model_validate(new_loan)
    
    async def update_loan(
        self,
        db: AsyncSession,
        loan_id: int,
        user_id: int,
        request_loan: LoanCreate
    ) -> LoanResponse:

        loan = await db.scalar(
            select(Loan).where(
                Loan.loan_id == loan_id,
                Loan.user_id == user_id
            )
        )

        if loan is None:
            raise LoanNotFoundError(loan_id)

        book = await db.get(Book, request_loan.book_id)

        if book is None:
            raise BookNotFoundError(request_loan.book_id)

        loan.book_id = request_loan.book_id
        loan.loan_date = request_loan.loan_date

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        await db.refresh(loan)

        return LoanResponse.model_validate(loan)
    
    async def delete_loan(
        self,
        db: AsyncSession,
        loan_id: int,
        user_id: int
    ) -> LoanResponse:

        loan = await db.scalar(
            select(Loan).where(
                Loan.loan_id == loan_id,
                Loan.user_id == user_id
            )
        )

        if loan is None:
            raise LoanNotFoundError(loan_id)

        response = LoanResponse.model_validate(loan)

        try:
            await db.delete(loan)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        return response
