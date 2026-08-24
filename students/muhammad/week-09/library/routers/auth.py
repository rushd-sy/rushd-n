from typing import Annotated
from fastapi import APIRouter, Depends

from models.users import UserCreate
from services.auth_services import AuthServices

router = APIRouter(prefix='/auth')

@router.post("/register")
async def  register_user(
        user_create: UserCreate,
        auth_services: Annotated[
            AuthServices,
            Depends(AuthServices)
        ]
    ):
    return await auth_services.register_user(user_create=user_create)
