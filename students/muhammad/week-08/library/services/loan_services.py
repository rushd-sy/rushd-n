from datetime import date

from utils.storage import load_loans, save_loans
from models.loans import LoanCreate, LoanModel, LoanResponse
from models.page import Page
from exceptions import LoanNotFoundError

class LoanServices:
    
    @staticmethod
    async def _load_loans() -> list[LoanModel]:
        return await load_loans()
    
    @staticmethod
    async def _save_loans(loans: list[LoanModel]) -> None:
        await save_loans(loans)
    
    async def get_loans(
            self,
            name: str | None = None,
            loan_date: date | None = None,
            min_date: date | None = None,
            max_date: date | None = None,
            offset: int = 0,
            limit: int = 20
        ) -> Page[LoanResponse]:
        
        loans = await LoanServices._load_loans()
        loans_out = []
        
        for loan_model in loans:
            loan = LoanResponse(**loan_model.model_dump())
            if name and loan.name != name:
                continue
            if loan_date and loan.loan_date != loan_date:
                continue
            if min_date and loan.loan_date < min_date:
                continue
            if max_date and loan.loan_date > max_date:
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
    
    async def get_loan_by_id(self, loan_id: int) -> LoanResponse:
        loans = await LoanServices._load_loans()
        for loan in loans:
            if loan.loan_id == loan_id:
                return LoanResponse(**loan.model_dump())
        raise LoanNotFoundError(loan_id)
    
    async def create_loan(self, request_loan: LoanCreate) -> LoanResponse:
        loans = await LoanServices._load_loans()
        created_loan = LoanModel(
            loan_id=max([loan.loan_id for loan in loans], default=0) + 1,
            **request_loan.model_dump(),
            added_at=date.today(),
        )
        loans.append(created_loan)
        await save_loans(loans)

        return LoanResponse(
            **created_loan.model_dump(),
        )
    
    async def update_loan(self, loan_id: int, request_loan: LoanCreate) -> LoanResponse:
        loans = await load_loans()
        for index, loan in enumerate(loans):
            if loan.loan_id == loan_id:
                updated_loan = LoanModel(
                    loan_id=loan_id,
                    **request_loan.model_dump(),
                    added_at=loan.added_at,
                )
                
                loans[index] = updated_loan
                await save_loans(loans)
                return LoanResponse(**updated_loan.model_dump())
        
        raise LoanNotFoundError(loan_id)
    
    async def delete_loan(self, loan_id: int) -> LoanResponse:        
        loans = await load_loans()
        for index, loan in enumerate(loans):
            if loan.loan_id == loan_id:
                del loans[index]
                await save_loans(loans)
                return LoanResponse(**loan.model_dump())
        
        raise LoanNotFoundError(loan_id)
