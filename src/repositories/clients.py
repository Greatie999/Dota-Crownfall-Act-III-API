from typing import (
    Any,
    Optional,
    Sequence
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import (
    ClientORM,
    SessionORM
)
from src.repositories.base import SQLAlchemyRepository


class ClientsRepository(SQLAlchemyRepository[ClientORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, ClientORM)

    async def get_one_with_joins(
        self,
        *where,
        order_by: Optional[Any] = None,
    ) -> Optional[ClientORM]:
        query = (
            select(ClientORM)
            .options(
                joinedload(ClientORM.session).joinedload(SessionORM.account),
                joinedload(ClientORM.session).joinedload(SessionORM.lobby),
                joinedload(ClientORM.session).joinedload(SessionORM.game)
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
        order_by: Optional[Any] = ClientORM.created_at.asc()
    ) -> Sequence[ClientORM]:
        query = (
            select(ClientORM)
            .options(
                joinedload(ClientORM.session).joinedload(SessionORM.account),
                joinedload(ClientORM.session).joinedload(SessionORM.lobby),
                joinedload(ClientORM.session).joinedload(SessionORM.game)
            )
            .where(*where)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
