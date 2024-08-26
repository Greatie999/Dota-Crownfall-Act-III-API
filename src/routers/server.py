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
    ServerSet,
    Server,
    User,
    ResponseOK
)
from src.services import ServerService
from src.utils.uow import UnitOfWork

router = APIRouter(
    prefix="/server",
    tags=["Server"]
)


@router.get(
    "/",
    response_model=Server
)
async def get_server(
    sc: Annotated[str, Depends(correct_secret_key)],
    service: Annotated[ServerService, Depends(ServerService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_server(uow)


@router.put(
    "/",
    response_model=ResponseOK
)
async def set_server(
    data: ServerSet,
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[ServerService, Depends(ServerService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_server(uow, data)
