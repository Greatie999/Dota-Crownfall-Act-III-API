from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Optional
)
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.models.base import (
    Base,
    guid_pk,
    str_128,
    true,
    created_at,
    updated_at
)

if TYPE_CHECKING:
    from src.models.users import UserORM
    from src.models.reports import ReportORM
    from src.models.sessions import SessionORM


class ClientORM(Base):
    __tablename__ = "clients"

    id: Mapped[guid_pk]
    ip_address: Mapped[str_128]
    name: Mapped[str_128]
    active: Mapped[true]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    success_at: Mapped[Optional[datetime]]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UserORM"] = relationship(back_populates="clients")
    reports: Mapped[list["ReportORM"]] = relationship(back_populates="client")
    session: Mapped["SessionORM"] = relationship(back_populates="client")
