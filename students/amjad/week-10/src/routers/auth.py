from fastapi import Depends, APIRouter, Path
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from dependency import CurrentUserDep

from models import UserCreate, UserOut, Token
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

@router.delete("/users/{user_id}", response_model=UserOut)
async def delete_user(
    user_id: CurrentUserDep,
    service: UserService = Depends(UserService),
) -> UserOut:
    """
    Delete a user by their ID.
    - **user_id**: The ID of the user to be deleted.
    - Returns the details of the deleted user if successful, otherwise raises a 404 error.
    """
    return await service.delete_User(user_id)