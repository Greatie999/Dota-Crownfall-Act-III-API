from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReportORM
from src.repositories.base import SQLAlchemyRepository


class ReportsRepository(SQLAlchemyRepository[ReportORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, ReportORM)
