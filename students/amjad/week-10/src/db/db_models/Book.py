from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func
from datetime import datetime
from .Base import Base

if TYPE_CHECKING:
    from .Loan import Loan
    from .Author import Author

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"), index=True, nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    loans: Mapped[list["Loan"]] = relationship(back_populates="book")
    author: Mapped["Author"] = relationship(back_populates="books")