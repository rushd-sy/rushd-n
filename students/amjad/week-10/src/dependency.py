import os

from fastapi import Depends, Query
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from models import  PageParams, TokenData
import jwt
from fastapi import HTTPException
from dotenv import load_dotenv
from db.database import get_db, AsyncSession
from sqlalchemy import select
from db.db_models.User import User

CommonsDepForDB = Annotated[AsyncSession, Depends(get_db)]

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
async def get_pagination_params(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10,
):
    return PageParams(offset=offset, limit=limit)


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(user_id=payload.get("user_id"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : CommonsDepForDB) -> int:
    payload = decode_access_token(token)
    user_id = payload.user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id


CommonsDepForPagination = Annotated[PageParams, Depends(get_pagination_params)]
CurrentUserDep = Annotated[int, Depends(get_current_user)]