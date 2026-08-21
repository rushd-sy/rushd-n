from fastapi import Depends, Path, Query, APIRouter
from typing import Annotated

from models import UserCreate, UserOut, LoginData
from dependency import login_info
from services.auth_service import UserService

router = APIRouter()

@router.post("/login", response_model=UserOut)
async def login(
    login_data: Annotated[LoginData, Depends(login_info)],
    service: UserService = Depends(UserService),
) -> UserOut:
    """
    Authenticate a user and return their details.
    - **login_data**: The login credentials of the user (email and password).
    - Returns the authenticated user's details if successful, otherwise raises a 401 error.
    """
    return await service.login(login_data)

@router.post("/register", response_model=UserOut)
async def register(
    user_create: UserCreate,
    service: UserService = Depends(UserService),
) -> UserOut:
    """
    Register a new user and return their details.
    - **name**: The name of the user.
    - **email**: The email of the user.
    - **password**: The password of the user (minimum 8 characters).
    - Returns the newly created user's details.
    """
    return await service.create_user(user_create)