from fastapi import HTTPException
from models import LoginData, UserOut, UserCreate, User
from datetime import datetime
from storage import load_users, save_users


class UserService:
    async def login(self, login_data: LoginData) -> UserOut:
        email, password = login_data.email, login_data.password
        users = await load_users()
        for user in users:
            if user.email == email and user.password == password:
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
            password=user_create.password
        )
        users.append(new_user)
        await save_users(users)
        return UserOut(**new_user.model_dump())
    