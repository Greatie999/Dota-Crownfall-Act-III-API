from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    relationship
)

from src.models.base import (
    Base,
    guid_pk,
    str_128,
    unique_str_128,
    created_at,
    updated_at,
    false,
    true
)

if TYPE_CHECKING:
    from src.models.accounts import AccountORM
    from src.models.clients import ClientORM


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[guid_pk]
    username: Mapped[unique_str_128]
    password: Mapped[str_128]
    admin: Mapped[false]
    status: Mapped[true]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    clients: Mapped[list["ClientORM"]] = relationship(back_populates="user")
    accounts: Mapped[list["AccountORM"]] = relationship(back_populates="user")
