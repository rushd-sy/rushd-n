from fastapi import Depends, APIRouter
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm


from models import UserCreate, UserOut, Token
from dependency import login_info, oauth2_scheme
from services.auth_service import UserService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(UserService),
) -> Token:
    """
    Authenticate a user and return a new JWT token.
    - **login_data**: The login credentials of the user (email and password).
    - Returns a new JWT token if successful, otherwise raises a 401 error.
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