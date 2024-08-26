from typing import Annotated

from annotated_types import MaxLen
from fastapi import (
    APIRouter,
    Depends
)

from src.dependencies import (
    existing_user,
    correct_secret_key,
    UnitOfWorkDependency
)
from src.schemas import (
    User,
    ResponseOK,
    Account,
    AccountCreate
)
from src.services import AccountsService
from src.utils import UnitOfWork

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post(
    "/",
    response_model=ResponseOK,
    tags=["Users"]
)
async def create_account(
    data: AccountCreate,
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[AccountsService, Depends(AccountsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.create_account(uow, user.id, data)


@router.get(
    "/{username}/",
    response_model=Account
)
async def get_account(
    username: Annotated[str, MaxLen(128)],
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[AccountsService, Depends(AccountsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_account(uow, username)


@router.delete(
    "/{username}/",
    response_model=ResponseOK
)
async def remove_account(
    username: Annotated[str, MaxLen(128)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[AccountsService, Depends(AccountsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.remove_account(uow, username)
