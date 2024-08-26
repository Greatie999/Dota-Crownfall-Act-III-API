from typing import (
    Any,
    Optional,
    Sequence
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import SessionORM
from src.repositories.base import SQLAlchemyRepository


class SessionsRepository(SQLAlchemyRepository[SessionORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, SessionORM)

    async def get_one_with_joins(
        self,
        *where,
    ) -> Optional[SessionORM]:
        query = (
            select(SessionORM)
            .options(
                joinedload(SessionORM.client),
                joinedload(SessionORM.account),
                joinedload(SessionORM.lobby),
                joinedload(SessionORM.game)
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
        order_by: Optional[Any] = SessionORM.created_at.asc()
    ) -> Sequence[SessionORM]:
        query = (
            select(SessionORM)
            .options(
                joinedload(SessionORM.client),
                joinedload(SessionORM.account),
                joinedload(SessionORM.lobby),
                joinedload(SessionORM.game)
            )
            .where(*where)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
