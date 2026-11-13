from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func
from datetime import datetime
from .Base import Base

if TYPE_CHECKING:
    from .Loan import Loan

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    loans: Mapped[list["Loan"]] = relationship(back_populates="user")