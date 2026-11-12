from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models.authors import Author
    from .loans import Loan

from database.base import Base


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id"),
        nullable=False
    )
    
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    genre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    publish_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    creation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
    
    loans: Mapped[list["Loan"]] = relationship(
        "Loan",
        back_populates="book"
    )
