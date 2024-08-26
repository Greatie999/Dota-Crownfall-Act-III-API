from pathlib import Path

from fastapi.responses import FileResponse
from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.exceptions import LauncherNotFound
from src.models import LauncherORM
from src.schemas import (
    LauncherSet,
    Launcher,
    ResponseOK
)
from src.utils import UnitOfWork


class LauncherService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_launcher(
        cls,
        uow: UnitOfWork,
    ) -> Launcher:
        async with uow:
            launcher = await uow.launcher.get_one()
            if launcher is None:
                raise LauncherNotFound
            return Launcher.model_validate(launcher)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_launcher(
        cls,
        uow: UnitOfWork,
        data: LauncherSet
    ) -> ResponseOK:
        async with uow:
            launcher = await uow.launcher.get_one()
            if launcher is None:
                model = LauncherORM(**data.model_dump())
                await uow.launcher.create_one(model)
            else:
                await uow.launcher.update_one(launcher, data.model_dump())
            await uow.commit()
            return ResponseOK(message="Launcher updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def download_launcher(
        cls,
        uow: UnitOfWork
    ) -> FileResponse:
        async with uow:
            launcher = await uow.launcher.get_one()
            file = Path(f"files/Bot_{launcher.version}.zip")
            if launcher is None or not file.exists():
                raise LauncherNotFound

            return FileResponse(
                path=file,
                filename="Launcher.zip",
                media_type="application/zip"
            )
