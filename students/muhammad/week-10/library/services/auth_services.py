
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from models.token import TokenResponse
from models.users import UserCreate, UserLogin
from database.models.users import User as UserORM
from exceptions import DuplicateEmailError, DuplicateUsernameError, InvalidCredentialsError
from utils.security import get_password_hash, verify_password, create_access_token



class AuthServices:
    async def register_user(
        self,
        db: AsyncSession,
        user_create: UserCreate
    ) -> TokenResponse:

        existing_username = await db.scalar(
            select(UserORM.user_id).where(
                UserORM.username == user_create.username
            )
        )

        if existing_username is not None:
            raise DuplicateUsernameError(user_create.username)

        existing_email = await db.scalar(
            select(UserORM.user_id).where(
                UserORM.email == user_create.email
            )
        )

        if existing_email is not None:
            raise DuplicateEmailError(user_create.email)

        hashed_password = get_password_hash(user_create.password)

        new_user = UserORM(
            username=user_create.username,
            full_name=user_create.full_name,
            email=user_create.email,
            hashed_password=hashed_password
        )

        db.add(new_user)

        try:
            await db.commit()

        except IntegrityError:
            await db.rollback()
            existing_username = await db.scalar(
                select(UserORM.user_id).where(
                    UserORM.username == user_create.username
                )
            )

            if existing_username is not None:
                raise DuplicateUsernameError(user_create.username)

            existing_email = await db.scalar(
                select(UserORM.user_id).where(
                    UserORM.email == user_create.email
                )
            )

            if existing_email is not None:
                raise DuplicateEmailError(user_create.email)
            raise

        await db.refresh(new_user)

        access_token = create_access_token(
            data={"id": str(new_user.user_id)}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    async def login_user(
        self,
        db: AsyncSession,
        user_login: UserLogin
    ) -> TokenResponse:

        user = await db.scalar(
            select(UserORM).where(
                UserORM.username == user_login.username
            )
        )

        if user is None:
            verify_password(user_login.password)
            raise InvalidCredentialsError

        if not verify_password(
            user_login.password,
            user.hashed_password
        ):
            raise InvalidCredentialsError

        access_token = create_access_token(
            data={"id": str(user.user_id)}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
