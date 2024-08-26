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
    false,
    session_role,
    created_at,
    updated_at
)

if TYPE_CHECKING:
    from src.models.clients import ClientORM
    from src.models.accounts import AccountORM
    from src.models.lobbies import LobbyORM
    from src.models.games import GameORM


class SessionORM(Base):
    __tablename__ = "sessions"

    id: Mapped[guid_pk]
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), unique=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), unique=True)
    lobby_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("lobbies.id", ondelete="SET NULL"))
    game_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("games.id", ondelete="SET NULL"))
    accepted: Mapped[false]
    loaded: Mapped[false]
    role: Mapped[session_role]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    client: Mapped["ClientORM"] = relationship(back_populates="session")
    account: Mapped["AccountORM"] = relationship(back_populates="session")
    lobby: Mapped["LobbyORM"] = relationship(back_populates="sessions")
    game: Mapped["GameORM"] = relationship(back_populates="sessions")
