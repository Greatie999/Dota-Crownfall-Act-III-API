from datetime import (
    datetime,
    timedelta
)
from random import choice
from typing import (
    Any,
    Optional,
    Sequence
)
from uuid import UUID

from sqlalchemy import (
    select
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import (
    AccountORM,
    SessionORM,
    UserORM
)
from src.repositories.base import (
    SQLAlchemyRepository
)


class AccountsRepository(SQLAlchemyRepository[AccountORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, AccountORM)

    async def create_one(
        self,
        model: AccountORM
    ) -> None:
        self.session.add(model)

    async def get_one_with_joins(
        self,
        *where
    ) -> Optional[AccountORM]:
        query = (
            select(AccountORM)
            .options(
                joinedload(AccountORM.session).joinedload(SessionORM.client),
                joinedload(AccountORM.session).joinedload(SessionORM.lobby),
                joinedload(AccountORM.session).joinedload(SessionORM.game)
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
        order_by: Optional[Any] = AccountORM.created_at.asc()
    ) -> Sequence[AccountORM]:
        query = (
            select(AccountORM)
            .options(
                joinedload(AccountORM.session).joinedload(SessionORM.client),
                joinedload(AccountORM.session).joinedload(SessionORM.lobby),
                joinedload(AccountORM.session).joinedload(SessionORM.game)
            )
            .where(*where)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_for_farming(
        self,
        user_id: UUID
    ) -> Optional[AccountORM]:
        _farm_limit = datetime.utcnow() - timedelta(minutes=15)

        query = (
            select(AccountORM)
            .options(
                joinedload(AccountORM.user),
                joinedload(AccountORM.session)
            )
            .where(
                AccountORM.user_id == user_id,
                AccountORM.farmed.is_(False),
                AccountORM.failed.is_(False),
                AccountORM.farmed_at < _farm_limit,
                AccountORM.session == None,  # noqa: E711
                AccountORM.user.has(UserORM.status.is_(True))
            )
            .order_by(
                AccountORM.farmed_at.asc()
            )
            .limit(50)
        )
        result = await self.session.execute(query)
        accounts = result.scalars().all()
        return choice(accounts) if accounts else None
