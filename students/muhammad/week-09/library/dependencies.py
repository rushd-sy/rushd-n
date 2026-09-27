from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
    InvalidSignatureError
    )
import jwt

from exceptions import InvalidCredentialsError
from config import settings
from utils.users_store import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_pagination_params(limit: int = 20, offset: int = 0) -> dict[str, int]:
    if limit > 20: 
        raise HTTPException(status_code=400, detail="limit cannot excced 20")
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be at least 1")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be at least 0")
    return {"limit" : limit, "offset" : offset}

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, login again")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Token signature verification failed")
    except InvalidTokenError:
        raise InvalidCredentialsError
    
    cur_user_id = payload.get("id")
    if cur_user_id is None:
        raise InvalidCredentialsError
    try:
        cur_user_id = int(cur_user_id)
    except (TypeError, ValueError):
        raise InvalidCredentialsError

    if cur_user_id not in [user.user_id for user in users]:
        raise InvalidCredentialsError
        
    return cur_user_id
