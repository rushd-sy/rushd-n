from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.users import UserCreate, UserLogin
from models.token import TokenResponse
from services.auth_services import AuthServices

router = APIRouter(prefix='/auth')

@router.post("/register", response_model=TokenResponse)
async def register_user(
        user_create: UserCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        auth_services: Annotated[
            AuthServices,
            Depends(AuthServices)
        ]
    ) -> TokenResponse:

    return await auth_services.register_user(
        db=db,
        user_create=user_create
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(
        form_data: Annotated[
            OAuth2PasswordRequestForm,
            Depends()
        ],
        db: Annotated[AsyncSession, Depends(get_db)],
        auth_services: Annotated[
            AuthServices,
            Depends(AuthServices)
        ]
    ) -> TokenResponse:
    
    user_login = UserLogin(
        username=form_data.username,
        password=form_data.password,
    )
    
    return await auth_services.login_user(
        db=db, 
        user_login=user_login
    )
