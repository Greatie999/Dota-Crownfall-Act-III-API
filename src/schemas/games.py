from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Literal
)

from pydantic import (
    BaseModel,
    ConfigDict
)

if TYPE_CHECKING:
    from src.schemas.sessions import SessionInGame


class Game(BaseModel):
    id: str
    state: Literal[
        "Preparing",
        "Confirmed"
    ]
    created_at: datetime
    updated_at: datetime
    sessions: list["SessionInGame"]
    model_config = ConfigDict(from_attributes=True)


class GameInSession(BaseModel):
    id: str
    state: Literal[
        "Preparing",
        "Confirmed"
    ]
    model_config = ConfigDict(from_attributes=True)
