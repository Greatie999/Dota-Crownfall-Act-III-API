from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_factory
from src.repositories import (
    AccountsRepository,
    ClientsRepository,
    GamesRepository,
    LauncherRepository,
    LobbiesRepository,
    ReportsRepository,
    ServerRepository,
    SessionsRepository,
    StatusRepository,
    UsersRepository,
    VPNRepository
)


class UnitOfWork:
    def __init__(self):
        self._isolation_level: Literal[
            "AUTOCOMMIT",
            "READ COMMITTED",
            "REPEATABLE READ",
            "SERIALIZABLE"
        ] = "READ COMMITTED"
        self._session: AsyncSession | None = None

    @property
    def isolation_level(self) -> str:
        return self._isolation_level

    @isolation_level.setter
    def isolation_level(
        self,
        value: Literal[
            "AUTOCOMMIT",
            "READ COMMITTED",
            "REPEATABLE READ",
            "SERIALIZABLE"
        ]
    ):
        self._isolation_level = value

    @property
    def session(self) -> AsyncSession | None:
        return self._session

    async def __aenter__(self):
        self._session: AsyncSession = async_session_factory()
        await self.session.connection(execution_options={"isolation_level": self.isolation_level})
        self.accounts = AccountsRepository(self.session)
        self.clients = ClientsRepository(self.session)
        self.games = GamesRepository(self.session)
        self.launcher = LauncherRepository(self.session)
        self.lobbies = LobbiesRepository(self.session)
        self.reports = ReportsRepository(self.session)
        self.server = ServerRepository(self.session)
        self.sessions = SessionsRepository(self.session)
        self.status = StatusRepository(self.session)
        self.users = UsersRepository(self.session)
        self.vpn = VPNRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
