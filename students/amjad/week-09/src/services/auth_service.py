from fastapi import HTTPException
from models import LoginData, TokenData, UserOut, UserCreate, User, Token
from storage import load_users, save_users
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    def create_access_token(self, data: TokenData, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> Token:
        to_encode = data.model_dump()
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta)})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt)
    
    def decode_access_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return TokenData(user_id=payload.get("user_id"))
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def login_using_jwt(self, token: str) -> Token:
        payload = self.decode_access_token(token)
        user_id = payload.user_id
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        users = await load_users()
        for user in users:
            if user.user_id == user_id:
                access_token = self.create_access_token(TokenData(user_id=user_id))
                return Token(access_token=access_token.access_token)
        raise HTTPException(status_code=404, detail="User not found")

    async def login(self, login_data: LoginData) -> Token:
        email, password = login_data.email, login_data.password
        users = await load_users()
        for user in users:
            if user.email == email and self.verify_password(password, user.password):
                user_id = user.user_id
                access_token = self.create_access_token(TokenData(user_id=user_id))
                return Token(access_token=access_token.access_token)
        raise HTTPException(status_code=401, detail="email or password is incorrect")

    async def create_user(self, user_create: UserCreate) -> UserOut:
        users = await load_users()
        new_user_id = max([user.user_id for user in users], default=0) + 1
        new_user = User(
            user_id=new_user_id,
            name=user_create.name,
            email=user_create.email,
            created_at=datetime.now().isoformat(),
            password=self.get_password_hash(user_create.password)
        )
        users.append(new_user)
        await save_users(users)
        return UserOut(**new_user.model_dump())
    