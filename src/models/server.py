from sqlalchemy.orm import Mapped

from src.models.base import (
    Base,
    guid_pk,
    created_at,
    updated_at,
    str_128
)


class ServerORM(Base):
    __tablename__ = "server"

    id: Mapped[guid_pk]
    name: Mapped[str_128]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
