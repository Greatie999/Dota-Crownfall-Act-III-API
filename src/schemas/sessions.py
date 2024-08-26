from datetime import datetime
from typing import (
    Optional,
    TYPE_CHECKING,
    Literal
)
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

if TYPE_CHECKING:
    from src.schemas.clients import ClientInSession
    from src.schemas.accounts import AccountInSession
    from src.schemas.lobbies import LobbyInSession
    from src.schemas.games import GameInSession


class SessionLobbyAcquireResponse(BaseModel):
    role: Literal[
        "Leader",
        "Member"
    ]


class SessionGameAcquire(BaseModel):
    game_id: str = Field(max_length=128)


class SessionLobbySteamIDSet(BaseModel):
    steam_id: str = Field(max_length=128)


class Session(BaseModel):
    id: UUID
    client: "ClientInSession"
    account: "AccountInSession"
    lobby: Optional["LobbyInSession"]
    game: Optional["GameInSession"]
    accepted: bool
    loaded: bool
    role: Literal[
        "Leader",
        "Member",
        ""
    ]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SessionInAccount(BaseModel):
    id: UUID
    client: "ClientInSession"
    lobby: Optional["LobbyInSession"]
    game: Optional["GameInSession"]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SessionInClient(BaseModel):
    id: UUID
    account: "AccountInSession"
    lobby: Optional["LobbyInSession"]
    game: Optional["GameInSession"]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SessionInLobby(BaseModel):
    client: "ClientInSession"
    account: "AccountInSession"
    accepted: bool
    loaded: bool
    role: Literal[
        "Leader",
        "Member",
        ""
    ]
    model_config = ConfigDict(from_attributes=True)


class SessionInGame(BaseModel):
    client: "ClientInSession"
    account: "AccountInSession"
    role: Literal[
        "Leader",
        "Member",
        ""
    ]
    model_config = ConfigDict(from_attributes=True)
