
from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .books import Book

from .users import User
from database.base import Base


class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    loan_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    added_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="loans"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="loans"
    )
