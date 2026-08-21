from fastapi import Depends, Header, Query
from typing import Annotated

from pydantic import EmailStr
from models import LoginData, LoginData, PageParams


async def get_pagination_params(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10,
):
    return PageParams(offset=offset, limit=limit)


async def get_current_user(
    X_user_id: Annotated[int | None, Header()] = None,
) -> int | None:
    return X_user_id

async def login_info(
    email: Annotated[EmailStr, Header()],
    password: Annotated[str, Header()],
) -> LoginData:
    return LoginData(email=email, password=password)

CommonsDepForPagination = Annotated[PageParams, Depends(get_pagination_params)]
CurrentUserDep = Annotated[int, Depends(get_current_user)]
