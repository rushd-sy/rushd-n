from fastapi import HTTPException, Header
from typing import Annotated

async def get_pagination_params(limit: int = 20, offset: int = 0):
    if limit > 20: 
        raise HTTPException(status_code=400, detail="limit cannot excced 20")
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be at least 1")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be at least 0")
    return {"limit" : limit, "offset" : offset}

async def get_current_user(x_user_id: Annotated[str | None, Header()] = None):
    if not x_user_id:
        raise HTTPException(status_code=401)
    return x_user_id
