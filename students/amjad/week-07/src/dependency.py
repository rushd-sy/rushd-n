from fastapi import Depends, Query
from typing import Annotated

async def get_pagination_params(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=20)] = 10,
):
    return {"limit": limit, "offset": offset}

CommonsDepForPagination = Annotated[dict, Depends(get_pagination_params)]