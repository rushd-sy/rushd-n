from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar("T")


class PageParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=20)
    offset: int = Field(default=0, ge=0)


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    offset: int | None = None
    limit: int | None = None
