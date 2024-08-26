from sqlalchemy.ext.asyncio import AsyncSession

from src.models import StatusORM
from src.repositories.base import SQLAlchemyRepository


class StatusRepository(SQLAlchemyRepository[StatusORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, StatusORM)
