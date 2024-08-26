from typing import (
    Any,
    Optional,
    Sequence
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import (
    GameORM,
    SessionORM
)
from src.repositories.base import SQLAlchemyRepository


class GamesRepository(SQLAlchemyRepository[GameORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, GameORM)

    async def get_one_with_joins(
        self,
        *where,
    ) -> Optional[GameORM]:
        query = (
            select(GameORM)
            .options(
                selectinload(GameORM.sessions).joinedload(SessionORM.client),
                selectinload(GameORM.sessions).joinedload(SessionORM.account)
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
        order_by: Optional[Any] = GameORM.created_at.desc()
    ) -> Sequence[GameORM]:
        query = (
            select(GameORM)
            .options(
                selectinload(GameORM.sessions).joinedload(SessionORM.client),
                selectinload(GameORM.sessions).joinedload(SessionORM.account)
            )
            .where(*where)
            .order_by(order_by)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
