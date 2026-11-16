from datetime import date
from sqlalchemy import Date, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .books import Book

from database.base import Base

class Author(Base):
    __tablename__ = "authors"
    
    author_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    birth_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    added_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )
    
    books: Mapped[list["Book"]] = relationship(
        back_populates="author"
    )
