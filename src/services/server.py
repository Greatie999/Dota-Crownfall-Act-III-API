from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.exceptions import ServerNotFound
from src.models import ServerORM
from src.schemas import (
    ServerSet,
    Server,
    ResponseOK
)
from src.utils import UnitOfWork


class ServerService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_server(
        cls,
        uow: UnitOfWork
    ) -> Server:
        async with uow:
            server = await uow.server.get_one()
            if server is None:
                raise ServerNotFound
            return Server.model_validate(server)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_server(
        cls,
        uow: UnitOfWork,
        data: ServerSet
    ) -> ResponseOK:
        async with uow:
            server = await uow.server.get_one()
            if server is None:
                model = ServerORM(**data.model_dump())
                await uow.server.create_one(model)
            else:
                await uow.server.update_one(server, data.model_dump())
            await uow.commit()
            return ResponseOK(message="Server updated successfully")
