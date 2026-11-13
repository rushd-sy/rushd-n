from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from datetime import datetime
from .Base import Base

if TYPE_CHECKING:
    from .Book import Book
    from .User import User


class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    loan_date: Mapped[datetime] = mapped_column(server_default=func.now())
    return_date: Mapped[datetime] = mapped_column(nullable=False)

    book: Mapped["Book"] = relationship(back_populates="loans")
    user: Mapped["User"] = relationship(back_populates="loans")