from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ServerORM
from src.repositories.base import SQLAlchemyRepository


class ServerRepository(SQLAlchemyRepository[ServerORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, ServerORM)
