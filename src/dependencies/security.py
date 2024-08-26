from typing import Annotated

from fastapi import Depends

from src.exceptions import (
    SecretKeyInvalid,
    UserAccessDenied
)
from src.schemas import (
    UserJWT,
    User
)
from src.security import (
    secret_key_scheme,
    oauth2_scheme
)
from src.services import UsersService
from src.settings import settings
from src.utils import UnitOfWork


async def correct_secret_key(
    key: Annotated[str, Depends(secret_key_scheme)]
) -> str:
    if key != settings.API_SECRET_KEY:
        raise SecretKeyInvalid
    return key


async def correct_user_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserJWT:
    return await UsersService.verify_token(token)


async def existing_user(
    user: Annotated[UserJWT, Depends(correct_user_token)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWork)]
) -> User:
    return await UsersService.get_current_user(uow, user)


async def admin_user(
    user: Annotated[User, Depends(existing_user)]
) -> User:
    if user.admin is not True:
        raise UserAccessDenied
    return user
