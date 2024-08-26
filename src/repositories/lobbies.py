from typing import (
    Optional,
    Any,
    Sequence
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import (
    LobbyORM,
    SessionORM
)
from src.repositories.base import SQLAlchemyRepository


class LobbiesRepository(SQLAlchemyRepository[LobbyORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, LobbyORM)

    async def get_one_with_joins(
        self,
        *where
    ) -> Optional[LobbyORM]:
        query = (
            select(LobbyORM)
            .options(
                selectinload(LobbyORM.sessions).joinedload(SessionORM.client),
                selectinload(LobbyORM.sessions).joinedload(SessionORM.account)
            )
            .where(*where)
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_many_with_joins(
        self,
        *where,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Any] = LobbyORM.created_at.desc()
    ) -> Sequence[LobbyORM]:
        query = (
            select(LobbyORM)
            .options(
                selectinload(LobbyORM.sessions).joinedload(SessionORM.client),
                selectinload(LobbyORM.sessions).joinedload(SessionORM.account)
            )
            .where(*where)
            .order_by(order_by)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_for_farming(
        self
    ) -> Optional[LobbyORM]:
        query = (
            select(LobbyORM)
            .where(LobbyORM.state == "Preparing")
        )
        result = await self.session.execute(query)
        return result.scalar()
