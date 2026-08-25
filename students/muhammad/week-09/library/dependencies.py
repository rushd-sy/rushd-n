from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
import jwt

from exceptions import InvalidCredentialsError
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_pagination_params(limit: int = 20, offset: int = 0):
    if limit > 20: 
        raise HTTPException(status_code=400, detail="limit cannot excced 20")
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be at least 1")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be at least 0")
    return {"limit" : limit, "offset" : offset}

async def get_current_user(token: str = Depends(oauth2_scheme)):

    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except InvalidTokenError:
        raise InvalidCredentialsError
    
    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsError
    
    return user_id
