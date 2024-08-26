from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserORM
from src.repositories.base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[UserORM]):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(session, UserORM)
