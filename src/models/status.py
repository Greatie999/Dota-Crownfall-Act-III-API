from sqlalchemy.orm import Mapped

from src.models.base import (
    Base,
    guid_pk,
    created_at,
    updated_at,
    true
)


class StatusORM(Base):
    __tablename__ = "status"

    id: Mapped[guid_pk]
    value: Mapped[true]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
