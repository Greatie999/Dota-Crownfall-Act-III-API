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
    StatusSet,
    Status,
    User,
    ResponseOK
)
from src.services import StatusService
from src.utils.uow import UnitOfWork

router = APIRouter(
    prefix="/status",
    tags=["Status"]
)


@router.get(
    "/",
    response_model=Status
)
async def get_status(
    sc: Annotated[str, Depends(correct_secret_key)],
    service: Annotated[StatusService, Depends(StatusService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_status(uow)


@router.put(
    "/",
    response_model=ResponseOK
)
async def set_status(
    data: StatusSet,
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[StatusService, Depends(StatusService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_status(uow, data)
