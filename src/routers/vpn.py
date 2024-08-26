from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)

from src.dependencies import (
    correct_secret_key,
    admin_user,
    UnitOfWorkDependency
)
from src.schemas import (
    VPNCreate,
    VPN,
    User,
    ResponseOK
)
from src.services import VPNService
from src.utils.uow import UnitOfWork

router = APIRouter(
    prefix="/vpn",
    tags=["VPN"]
)


@router.get(
    "/",
    response_model=list[VPN]
)
async def get_accounts(
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[VPNService, Depends(VPNService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_accounts(uow)


@router.post(
    "/",
    response_model=ResponseOK
)
async def create_account(
    data: VPNCreate,
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[VPNService, Depends(VPNService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.create_account(uow, data)


@router.post(
    "/acquire/",
    response_model=VPN
)
async def acquire_account(
    sc: Annotated[str, Depends(correct_secret_key)],
    service: Annotated[VPNService, Depends(VPNService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.acquire_account(uow)
