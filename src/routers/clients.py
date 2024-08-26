from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from src.dependencies import (
    QueryParams,
    existing_user,
    admin_user,
    correct_secret_key,
    UnitOfWorkDependency
)
from src.schemas import (
    User,
    ClientCreate,
    ClientCreateResponse,
    ClientUpdate,
    Client,
    RetrieveClientsResponse,
    ResponseOK,
    Account,
    Lobby,
    Game,
    SessionLobbyAcquireResponse,
    SessionGameAcquire,
    SessionLobbySteamIDSet,
    RetrieveReportsResponse
)
from src.services import ClientsService
from src.utils import UnitOfWork

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get(
    "/{id}/",
    response_model=Client
)
async def get_client(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_client(uow, id)


@router.post(
    "/",
    response_model=ClientCreateResponse
)
async def create_client(
    data: ClientCreate,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.create_client(uow, data)


@router.get(
    "/",
    response_model=RetrieveClientsResponse
)
async def get_clients(
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(admin_user)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_clients(uow, params=params)


@router.delete(
    "/{id}/",
    response_model=ResponseOK,
)
async def remove_client(
    id: UUID,
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.remove_client(uow, id)


@router.patch(
    "/{id}/",
    response_model=ResponseOK,
)
async def update_client(
    id: UUID,
    data: ClientUpdate,
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.update_client(uow, id, data)


@router.get(
    "/{id}/session/lobby/",
    response_model=Lobby
)
async def get_client_session_lobby(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_session_lobby(uow, id)


@router.get(
    "/{id}/session/game/",
    response_model=Game
)
async def get_client_session_game(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_session_game(uow, id)


@router.post(
    "/{id}/session/account/acquire/",
    response_model=Account
)
async def acquire_client_session_account(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.acquire_session_account(uow, id)


@router.post(
    "/{id}/session/lobby/acquire/",
    response_model=SessionLobbyAcquireResponse
)
async def acquire_client_session_lobby(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.acquire_session_lobby(uow, id)


@router.post(
    "/{id}/session/lobby/steam-id/",
    response_model=ResponseOK
)
async def set_client_session_lobby_steam_id(
    id: UUID,
    data: SessionLobbySteamIDSet,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.set_session_lobby_steam_id(uow, id, data)


@router.post(
    "/{id}/session/lobby/invites-sent/",
    response_model=ResponseOK
)
async def set_client_session_lobby_state(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.set_session_lobby_state(uow, id, "InvitesSent")


@router.post(
    "/{id}/session/accepted/",
    response_model=ResponseOK
)
async def set_session_as_accepted(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.set_session(uow, id, "Accepted")


@router.post(
    "/{id}/session/loaded/",
    response_model=ResponseOK
)
async def set_session_as_loaded(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.set_session(uow, id, "Loaded")


@router.post(
    "/{id}/session/lobby/started-search/",
    response_model=ResponseOK
)
async def set_client_session_lobby_state(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.set_session_lobby_state(uow, id, "SearchStarted")


@router.post(
    "/{id}/session/game/acquire/",
    response_model=ResponseOK
)
async def acquire_client_session_game(
    id: UUID,
    data: SessionGameAcquire,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
):
    return await service.acquire_session_game(uow, id, data)


@router.post(
    "/{id}/session/account/farmed/",
    response_model=ResponseOK
)
async def set_client_session_account_as_farmed(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_session_account(uow, id, "Farmed")


@router.post(
    "/{id}/session/account/failed/",
    response_model=ResponseOK
)
async def set_client_session_account_as_failed(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_session_account(uow, id, "Failed")


@router.post(
    "/{id}/session/release/",
    response_model=ResponseOK
)
async def release_client_session(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    # uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("SERIALIZABLE"))]
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("REPEATABLE READ"))]
):
    return await service.release_session(uow, id)


@router.post(
    "/{id}/success/",
    response_model=ResponseOK
)
async def set_client_success(
    id: UUID,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.set_success(uow, id)


@router.get(
    "/{id}/reports/",
    response_model=RetrieveReportsResponse,
    tags=["Reports"]
)
async def get_client_reports(
    id: UUID,
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[ClientsService, Depends(ClientsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.get_reports(uow, id, params=params)
