from src.schemas.accounts import (
    AccountCreate,
    Account,
    AccountInSession,
    RetrieveAccountsResponse
)
from src.schemas.clients import (
    ClientCreate,
    ClientCreateResponse,
    ClientUpdate,
    Client,
    ClientInSession,
    RetrieveClientsResponse
)
from src.schemas.games import (
    Game,
    GameInSession
)
from src.schemas.launcher import (
    LauncherSet,
    Launcher
)
from src.schemas.lobbies import (
    Lobby,
    LobbyInSession
)
from src.schemas.reports import (
    ReportCreate,
    Report,
    RetrieveReportsResponse
)
from src.schemas.responses import ResponseOK
from src.schemas.server import (
    ServerSet,
    Server
)
from src.schemas.sessions import (
    SessionLobbyAcquireResponse,
    SessionGameAcquire,
    SessionLobbySteamIDSet,
    SessionInClient,
    Session,
    SessionInGame,
    SessionInLobby,
    SessionInAccount
)
from src.schemas.status import (
    StatusSet,
    Status
)
from src.schemas.users import (
    UserToken,
    UserJWT,
    UserUpdate,
    User
)
from src.schemas.vpn import (
    VPNCreate,
    VPN
)

RetrieveAccountsResponse.model_rebuild()
RetrieveClientsResponse.model_rebuild()
RetrieveReportsResponse.model_rebuild()
AccountInSession.model_rebuild()
SessionInClient.model_rebuild()
SessionInLobby.model_rebuild()
ClientInSession.model_rebuild()
Lobby.model_rebuild()
Game.model_rebuild()
Session.model_rebuild()
SessionInGame.model_rebuild()
SessionInAccount.model_rebuild()

__all__ = [
    "AccountCreate",
    "Account",
    "AccountInSession",
    "RetrieveAccountsResponse",
    "ClientCreate",
    "ClientCreateResponse",
    "ClientUpdate",
    "Client",
    "ClientInSession",
    "RetrieveClientsResponse",
    "Game",
    "GameInSession",
    "LauncherSet",
    "Launcher",
    "Lobby",
    "LobbyInSession",
    "ReportCreate",
    "Report",
    "RetrieveReportsResponse",
    "ResponseOK",
    "ServerSet",
    "Server",
    "SessionLobbyAcquireResponse",
    "SessionGameAcquire",
    "SessionLobbySteamIDSet",
    "SessionInClient",
    "Session",
    "SessionInGame",
    "SessionInLobby",
    "SessionInAccount",
    "StatusSet",
    "Status",
    "UserToken",
    "UserJWT",
    "UserUpdate",
    "User",
    "VPNCreate",
    "VPN",
]
