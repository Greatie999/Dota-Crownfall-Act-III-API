from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import LauncherORM
from src.repositories.base import SQLAlchemyRepository


class LauncherRepository(SQLAlchemyRepository[LauncherORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, LauncherORM)
