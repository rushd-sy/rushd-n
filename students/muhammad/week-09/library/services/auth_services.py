from models.users import UserResponse, UserCreate, User
from utils.users_store import users
from exceptions import DuplicateEmailError, DuplicateUsernameError
from middlewares.logging import logger

class AuthServices:
    
    async def register_user(self, user_create: UserCreate) -> UserResponse:
        if user_create.username in [user.username for user in users]:
            raise DuplicateUsernameError(user_create.username)
        if user_create.email in [user.email for user in users]:
            raise DuplicateEmailError(user_create.email)
        
        new_id = max([user.user_id for user in users], default = 0) + 1
        new_user = User(**user_create.model_dump(), user_id=new_id)
        users.append(new_user)
        logger.info(f"""User with the following information successfully added:
        username: {new_user.username}
        id: {new_user.user_id}
        email: {new_user.email}
""")
        return UserResponse(**new_user.model_dump())
