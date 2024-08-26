from typing import TYPE_CHECKING
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
    created_at,
    updated_at
)

if TYPE_CHECKING:
    from src.models.clients import ClientORM


class ReportORM(Base):
    __tablename__ = "reports"

    id: Mapped[guid_pk]
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), index=True)
    error: Mapped[str]
    traceback: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    client: Mapped["ClientORM"] = relationship(back_populates="reports")
