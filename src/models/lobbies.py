from typing import (
    TYPE_CHECKING,
    Optional
)

from sqlalchemy.orm import (
    Mapped,
    relationship
)

from src.models.base import (
    Base,
    guid_pk,
    lobby_state,
    unique_str_128,
    created_at,
    updated_at
)

if TYPE_CHECKING:
    from src.models.accounts import SessionORM


class LobbyORM(Base):
    __tablename__ = "lobbies"

    id: Mapped[guid_pk]
    steam_id: Mapped[Optional[unique_str_128]]
    state: Mapped[lobby_state]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    sessions: Mapped[list["SessionORM"]] = relationship(back_populates="lobby")
