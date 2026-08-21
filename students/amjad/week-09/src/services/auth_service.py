from fastapi import HTTPException
from models import LoginData, UserOut, UserCreate, User
from datetime import datetime
from storage import load_users, save_users
from pwdlib import PasswordHash



class UserService:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    async def login(self, login_data: LoginData) -> UserOut:
        email, password = login_data.email, login_data.password
        users = await load_users()
        for user in users:
            if user.email == email and self.verify_password(password, user.password):
                return UserOut(**user.model_dump())
        raise HTTPException(status_code=401, detail="unauthorized")

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
    