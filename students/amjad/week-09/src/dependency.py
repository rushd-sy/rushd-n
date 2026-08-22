import os

from fastapi import Depends, Header, Query
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from models import LoginData, LoginData, PageParams, TokenData, TokenData, UserOut
import jwt
from fastapi import HTTPException
from storage import load_users
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
    
async def get_current_user(self, token: str) -> UserOut:
    payload = self.decode_access_token(token)
    user_id = payload.user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    users = await load_users()
    for user in users:
        if user.user_id == user_id:
            return UserOut(
                user_id=user.user_id,
                name=user.name,
                email=user.email,
            )
    raise HTTPException(status_code=404, detail="User not found")


async def login_info(
    email: Annotated[EmailStr, Header()],
    password: Annotated[str, Header()],
) -> LoginData:
    return LoginData(email=email, password=password)

CommonsDepForPagination = Annotated[PageParams, Depends(get_pagination_params)]
CurrentUserDep = Annotated[UserOut, Depends(get_current_user)]
