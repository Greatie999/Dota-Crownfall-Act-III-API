from typing import Literal

from src.utils import UnitOfWork


class UnitOfWorkDependency:
    def __init__(
        self,
        isolation_level: Literal[
            "AUTOCOMMIT",
            "READ COMMITTED",
            "REPEATABLE READ",
            "SERIALIZABLE"
        ]
    ):
        self.isolation_level = isolation_level

    async def __call__(self) -> UnitOfWork:
        uow = UnitOfWork()
        uow.isolation_level = self.isolation_level
        return uow
