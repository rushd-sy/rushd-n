from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func
from datetime import datetime

class Base(DeclarativeBase):
    pass

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

class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_year: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    loan_date: Mapped[datetime] = mapped_column(server_default=func.now())
    return_date: Mapped[datetime] = mapped_column(nullable=False)

    book: Mapped["Book"] = relationship(back_populates="loans")
    user: Mapped["User"] = relationship(back_populates="loans")

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    loans: Mapped[list["Loan"]] = relationship(back_populates="user")