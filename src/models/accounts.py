from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    DateTime,
text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.models.base import (
    Base,
    guid_pk,
    str_128,
    unique_str_128,
    created_at,
    updated_at,
    false
)

if TYPE_CHECKING:
    from src.models.users import UserORM
    from src.models.sessions import SessionORM


class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[guid_pk]
    username: Mapped[unique_str_128]
    password: Mapped[str_128]
    shared_secret: Mapped[str_128]
    steam_id: Mapped[int]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    farmed: Mapped[false]
    failed: Mapped[false]
    farmed_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("'1900-01-01 00:00:00'"), index=True)
    played_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("'1900-01-01 00:00:00'"), index=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UserORM"] = relationship(back_populates="accounts")
    session: Mapped["SessionORM"] = relationship(back_populates="account")
