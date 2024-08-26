from sqlalchemy.orm import Mapped

from src.models.base import (
    Base,
    guid_pk,
    str_128,
    created_at,
    updated_at
)


class LauncherORM(Base):
    __tablename__ = "launcher"

    id: Mapped[guid_pk]
    version: Mapped[str_128]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
