from models.token_models import TokenResponse
from models.users_models import UserCreate, User, UserLogin
from utils.users_store import users
from exceptions import DuplicateEmailError, DuplicateUsernameError, InvalidCredentialsError
from utils.security import get_password_hash, verify_password, create_access_token

class AuthServices:
    
    async def register_user(self, user_create: UserCreate) -> TokenResponse:
        if user_create.username in [user.username for user in users]:
            raise DuplicateUsernameError(user_create.username)
        if user_create.email in [user.email for user in users]:
            raise DuplicateEmailError(user_create.email)
        
        new_id = max([user.user_id for user in users], default = 0) + 1
        hashed_password = get_password_hash(user_create.password)
        new_user = User(
            **user_create.model_dump(exclude={"password"}),
            password=hashed_password,
            user_id=new_id
        )
        users.append(new_user)
        
        access_token = create_access_token(
            data={"id": str(new_user.user_id)}
        )
        return TokenResponse (
            access_token= access_token,
            token_type= "bearer"
        )

    async def login_user(self, user_login: UserLogin) -> TokenResponse:
        user = next(
            (user for user in users if user.username == user_login.username),
            None
        )
        
        if user is None:
            verify_password(user_login.password)
            raise InvalidCredentialsError
        if not verify_password(user_login.password, user.password):
            raise InvalidCredentialsError
        access_token = create_access_token(
            data={"id": str(user.user_id)}
        )

        return TokenResponse (
            access_token= access_token,
            token_type= "bearer"
        )
