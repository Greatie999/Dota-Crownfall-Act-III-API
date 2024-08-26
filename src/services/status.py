from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.exceptions import StatusNotFound
from src.models import StatusORM
from src.schemas import (
    StatusSet,
    Status,
    ResponseOK
)
from src.utils import UnitOfWork


class StatusService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_status(
        cls,
        uow: UnitOfWork
    ) -> Status:
        async with uow:
            status = await uow.status.get_one()
            if status is None:
                raise StatusNotFound
            return Status.model_validate(status)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_status(
        cls,
        uow: UnitOfWork,
        data: StatusSet
    ) -> ResponseOK:
        async with uow:
            status = await uow.status.get_one()
            if status is None:
                model = StatusORM(**data.model_dump())
                await uow.status.create_one(model)
            else:
                await uow.status.update_one(status, data.model_dump())
            await uow.commit()
            return ResponseOK(message="Status updated successfully")
