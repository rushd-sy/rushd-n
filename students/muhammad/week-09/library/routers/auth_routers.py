from typing import Annotated
from fastapi import APIRouter, Depends

from models.users_models import UserCreate, UserLogin, UserResponse
from services.auth_services import AuthServices

router = APIRouter(prefix='/auth')

@router.post("/register")
async def register_user(
        user_create: UserCreate,
        auth_services: Annotated[
            AuthServices,
            Depends(AuthServices)
        ]
    ) -> UserResponse:
    return await auth_services.register_user(user_create=user_create)

@router.post("/login")
async def login_user(
        user_login: UserLogin,
        auth_services: Annotated[
            AuthServices,
            Depends(AuthServices)
        ]
    ) -> UserResponse:
    return await auth_services.login_user(user_login)
