from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    relationship
)

from src.models.base import (
    Base,
    str_128_pk,
    game_state,
    created_at,
    updated_at
)

if TYPE_CHECKING:
    from src.models.sessions import SessionORM


class GameORM(Base):
    __tablename__ = "games"

    id: Mapped[str_128_pk]
    state: Mapped[game_state]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    sessions: Mapped[list["SessionORM"]] = relationship(back_populates="game")
