from fastapi import Depends, Header, Query
from typing import Annotated

async def get_pagination_params(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=20)] = 10,
):
    return {"limit": limit, "offset": offset}

async def get_current_user(
        X_user_id: Annotated[int | None, Header()] = None,
) -> int | None:
    return X_user_id

CommonsDepForPagination = Annotated[dict, Depends(get_pagination_params)]
CurrentUserDep = Annotated[int, Depends(get_current_user)]