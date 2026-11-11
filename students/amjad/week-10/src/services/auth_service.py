from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import  TokenData, UserOut, UserCreate, Token
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from dependency import CommonsDepForDB, CurrentUserDep
from sqlalchemy import select
from db.db_models.User import User as DBUser
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    def __init__(self, db : CommonsDepForDB) -> None:
        self.password_hash = PasswordHash.recommended()
        self.db = db

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    def create_access_token(self, data: TokenData, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> Token:
        to_encode = data.model_dump()
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta)})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt)

    async def login(self, login_data: OAuth2PasswordRequestForm) -> Token:
        email, password = login_data.username, login_data.password
        query = select(DBUser).where(DBUser.email == email)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            raise HTTPException(status_code=401, detail="email or password is incorrect")
        if not self.verify_password(password, db_user.password):
            raise HTTPException(status_code=401, detail="email or password is incorrect")
        user_id = db_user.user_id
        access_token = self.create_access_token(TokenData(user_id=user_id))
        return Token(access_token=access_token.access_token)

    async def create_user(self, user_create: UserCreate) -> UserOut:
        query = select(DBUser).where(DBUser.email == user_create.email)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = DBUser(
            name=user_create.name,
            email=user_create.email,
            created_at=datetime.now(),
            password=self.get_password_hash(user_create.password)
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserOut.model_validate(new_user)

    async def delete_User(
        self, user_id: CurrentUserDep
    ) -> UserOut:
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        db_user = await self.db.get(DBUser, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_out = UserOut.model_validate(db_user)
        await self.db.delete(db_user)
        await self.db.commit()
        return user_out