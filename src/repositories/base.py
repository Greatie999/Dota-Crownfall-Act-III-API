from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Any,
    TypeVar,
    Generic,
    Type,
    Sequence,
    Optional
)

from sqlalchemy import (
    select,
    delete,
    func,
    and_
)
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class IRepository(ABC, Generic[Model]):
    @abstractmethod
    async def create_one(
        self,
        model: Model
    ) -> Model:
        ...

    async def update_one(
        self,
        model: Model,
        data: dict
    ) -> None:
        ...

    @abstractmethod
    async def remove_one(
        self,
        model: Model
    ) -> None:
        ...

    @abstractmethod
    async def get_one(
        self,
        **filter_by: Any
    ) -> Optional[Model]:
        ...

    @abstractmethod
    async def get_many(
        self,
        *where,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Any] = None
    ) -> Sequence[Model]:
        ...

    @abstractmethod
    async def count(
        self,
        *where
    ) -> int:
        ...


class SQLAlchemyRepository(IRepository[Model]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Model]
    ):
        self.session = session
        self.model = model

    async def create_one(
        self,
        model: Model
    ) -> Model:
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def update_one(
        self,
        model: Model,
        data: dict
    ) -> None:
        for key, value in data.items():
            setattr(model, key, value)
        await self.session.flush()

    async def remove_one(
        self,
        model: Model
    ) -> None:
        stmt = delete(self.model).filter_by(id=model.id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_one(
        self,
        **filter_by: Any
    ) -> Optional[Model]:
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_many(
        self,
        *where,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Any] = None
    ) -> Sequence[Model]:
        query = (
            select(self.model)
            .where(*where)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(
        self,
        *where
    ) -> int:
        query = (
            select(func.count())
            .select_from(self.model).
            where(and_(*where))
        )
        result = await self.session.execute(query)
        return result.scalar()
