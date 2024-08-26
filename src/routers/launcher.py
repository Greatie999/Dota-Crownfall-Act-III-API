from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)
from starlette.responses import FileResponse

from src.dependencies import (
    correct_secret_key,
    admin_user,
    UnitOfWorkDependency
)
from src.schemas import (
    LauncherSet,
    Launcher,
    User,
    ResponseOK
)
from src.services import LauncherService
from src.utils.uow import UnitOfWork

router = APIRouter(
    prefix="/launcher",
    tags=["Launcher"]
)


@router.get(
    "/",
    response_model=Launcher
)
async def get_launcher(
    sc: Annotated[str, Depends(correct_secret_key)],
    service: Annotated[LauncherService, Depends(LauncherService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_launcher(uow)


@router.put(
    "/",
    response_model=ResponseOK
)
async def set_launcher(
    data: LauncherSet,
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[LauncherService, Depends(LauncherService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_launcher(uow, data)


@router.get(
    "/download/",
    response_class=FileResponse
)
async def download_launcher(
    sc: Annotated[str, Depends(correct_secret_key)],
    service: Annotated[LauncherService, Depends(LauncherService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.download_launcher(uow)
