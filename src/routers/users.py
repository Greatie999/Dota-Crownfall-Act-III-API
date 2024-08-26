from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import (
    correct_user_token,
    existing_user,
    QueryParams,
    UnitOfWorkDependency
)
from src.schemas import (
    UserJWT,
    UserToken,
    User,
    UserUpdate,
    ResponseOK,
    RetrieveAccountsResponse,
    RetrieveClientsResponse,
    RetrieveReportsResponse
)
from src.services import UsersService
from src.utils import UnitOfWork

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/sign-in/",
    response_model=UserToken
)
async def authenticate_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.authenticate_user(uow, data)


@router.get(
    "/me/",
    response_model=User
)
async def get_current_user(
    user: Annotated[UserJWT, Depends(correct_user_token)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_current_user(uow, user)


@router.patch(
    "/me/",
    response_model=ResponseOK
)
async def update_current_user(
    data: UserUpdate,
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.update_user(uow, user.id, data)


@router.get(
    "/me/accounts/",
    response_model=RetrieveAccountsResponse,
    tags=["Accounts"]
)
async def get_current_user_accounts(
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("REPEATABLE READ"))]
):
    return await service.get_user_accounts(uow, user.id, params)


@router.get(
    "/me/clients/",
    response_model=RetrieveClientsResponse,
    tags=["Clients"]
)
async def get_current_user_clients(
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("REPEATABLE READ"))]
):
    return await service.get_user_clients(uow, user.id, params)


@router.get(
    "/me/clients/reports/",
    response_model=RetrieveReportsResponse,
    tags=["Reports"]
)
async def get_current_user_clients_reports(
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[UsersService, Depends(UsersService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("REPEATABLE READ"))]
):
    return await service.get_user_clients_reports(uow, user.id, params)
