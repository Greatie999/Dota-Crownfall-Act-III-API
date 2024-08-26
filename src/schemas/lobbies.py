from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Literal,
    Optional
)
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict
)

if TYPE_CHECKING:
    from src.schemas.sessions import SessionInLobby


class Lobby(BaseModel):
    id: UUID
    steam_id: Optional[str]
    state: Literal[
        "Preparing",
        "AllJoined",
        "InvitesSent",
        "InvitesAccepted",
        "MembersLoaded",
        "SearchStarted"
    ]
    created_at: datetime
    updated_at: datetime
    sessions: list["SessionInLobby"]
    model_config = ConfigDict(from_attributes=True)


class LobbyInSession(BaseModel):
    id: UUID
    steam_id: Optional[str]
    state: Literal[
        "Preparing",
        "AllJoined",
        "InvitesSent",
        "InvitesAccepted",
        "MembersLoaded",
        "SearchStarted"
    ]
    model_config = ConfigDict(from_attributes=True)
