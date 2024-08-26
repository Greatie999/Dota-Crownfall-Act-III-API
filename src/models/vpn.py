from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.models.base import (
    Base,
    guid_pk,
    str_128,
    unique_str_128,
    created_at,
    updated_at
)


class VPNORM(Base):
    __tablename__ = "vpn"

    id: Mapped[guid_pk]
    username: Mapped[unique_str_128]
    password: Mapped[str_128]
    acquired_at: Mapped[datetime] = mapped_column(DateTime, default=datetime(1900, 1, 1), index=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
