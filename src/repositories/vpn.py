from random import choice
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import VPNORM
from src.repositories.base import SQLAlchemyRepository


class VPNRepository(SQLAlchemyRepository[VPNORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, VPNORM)

    async def get_one_for_farming(
        self
    ) -> Optional[VPNORM]:
        query = (
            select(VPNORM)
            .order_by(VPNORM.acquired_at.asc())
            .limit(3)
        )
        result = await self.session.execute(query)
        accounts = result.scalars().all()
        return choice(accounts) if accounts else None