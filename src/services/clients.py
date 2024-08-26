from datetime import datetime
from math import ceil
from typing import Literal
from uuid import UUID

from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random,
    wait_chain,
    wait_fixed
)

from src.dependencies import QueryParams
from src.exceptions import (
    UserNotFound,
    ClientNotFound,
    SessionNotFound,
    AccountNotFound,
    SessionActionForbidden,
    LobbyNotFound,
    GameNotFound
)
from src.models import (
    ClientORM,
    ReportORM,
    SessionORM,
    LobbyORM,
    GameORM
)
from src.schemas import (
    ClientCreate,
    ClientCreateResponse,
    ClientUpdate,
    Client,
    ResponseOK,
    Account,
    Lobby,
    Game,
    RetrieveClientsResponse,
    SessionLobbyAcquireResponse,
    SessionGameAcquire,
    SessionLobbySteamIDSet,
    RetrieveReportsResponse
)
from src.utils import UnitOfWork


class ClientsService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_clients(
        cls,
        uow: UnitOfWork,
        params: QueryParams
    ) -> RetrieveClientsResponse:
        async with uow:
            clients = await uow.clients.get_many_with_joins(limit=params.limit, offset=params.offset)
            clients_count = await uow.clients.count()
            pages = ceil(clients_count / params.limit) if params.limit else 1
            return RetrieveClientsResponse(
                data=clients,
                page=params.page,
                limit=params.limit,
                total=clients_count,
                pages=pages
            )

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_client(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> Client:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            return Client.model_validate(client)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def create_client(
        cls,
        uow: UnitOfWork,
        data: ClientCreate
    ) -> ClientCreateResponse:
        async with uow:
            user = await uow.users.get_one(id=data.user_id)
            if user is None:
                raise UserNotFound

            model = ClientORM(**data.model_dump())
            client = await uow.clients.create_one(model)
            await uow.commit()
            return ClientCreateResponse.model_validate(client)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def update_client(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        data: ClientUpdate
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one(id=client_id)
            if client is None:
                raise ClientNotFound

            await uow.clients.update_one(client, data.model_dump())
            await uow.commit()
            return ResponseOK(message="Client updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def remove_client(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one(id=client_id)
            if client is not None:
                await uow.clients.remove_one(client)
                await uow.commit()
            return ResponseOK(message="Client removed successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_reports(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        params: QueryParams
    ) -> RetrieveReportsResponse:
        async with uow:
            reports = await uow.reports.get_many(
                ReportORM.client_id == client_id,
                limit=params.limit,
                offset=params.offset,
                order_by=ReportORM.created_at.desc()
            )
            reports_count = await uow.reports.count(ReportORM.client_id == client_id)
            pages = ceil(reports_count / params.limit) if params.limit else 1
            return RetrieveReportsResponse(
                data=reports,
                page=params.page,
                limit=params.limit,
                total=reports_count,
                pages=pages
            )

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_session_lobby(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> Lobby:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound

            lobby = await uow.lobbies.get_one_with_joins(LobbyORM.id == client.session.lobby_id)
            if lobby is None:
                raise LobbyNotFound
            return Lobby.model_validate(lobby)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_session_game(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> Game:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound

            game = await uow.games.get_one_with_joins(GameORM.id == client.session.game_id)
            if game is None:
                raise GameNotFound
            return Game.model_validate(game)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_chain(
            *[wait_fixed(0.25) for _ in range(5)] + [wait_fixed(0.1)]
        ),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(30)
    )
    async def acquire_session_account(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> Account:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is not None:
                raise SessionActionForbidden

            account = await uow.accounts.get_one_for_farming(client.user_id)
            if account is None:
                raise AccountNotFound

            data = dict(
                client_id=client.id,
                account_id=account.id
            )
            model = SessionORM(**data)
            await uow.sessions.create_one(model)
            await uow.commit()
            return Account.model_validate(account)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(30)
    )
    async def acquire_session_lobby(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> SessionLobbyAcquireResponse:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound
            if client.session.lobby is not None:
                raise SessionActionForbidden

            lobby = await uow.lobbies.get_one_for_farming()
            if lobby is None:
                model = LobbyORM()
                lobby = await uow.lobbies.create_one(model)

            data = dict(lobby_id=lobby.id)
            await uow.sessions.update_one(client.session, data)
            await uow.commit()
            await uow.session.refresh(client.session)
            return SessionLobbyAcquireResponse(role=client.session.role)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_session_lobby_state(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        state: Literal["InvitesSent", "SearchStarted"]
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound
            if client.session.lobby is None:
                raise LobbyNotFound

            data = dict(state=state)
            await uow.lobbies.update_one(client.session.lobby, data)
            await uow.commit()
            return ResponseOK(message="Lobby updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_session_lobby_steam_id(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        data: SessionLobbySteamIDSet
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound
            if client.session.lobby is None:
                raise LobbyNotFound

            data = dict(steam_id=data.steam_id)
            await uow.lobbies.update_one(client.session.lobby, data)
            await uow.commit()
            return ResponseOK(message="Lobby updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_session(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        _as: Literal["Accepted", "Loaded"]
    ) -> ResponseOK:
        async with uow:
            _ = {
                "Accepted": dict(accepted=True),
                "Loaded": dict(loaded=True)
            }

            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound

            data = _.get(_as)
            await uow.sessions.update_one(client.session, data)
            await uow.commit()
            return ResponseOK(message="Session updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(30)
    )
    async def acquire_session_game(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        data: SessionGameAcquire
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound
            if client.session.game is not None:
                raise SessionActionForbidden

            game = await uow.games.get_one(id=data.game_id)
            if game is None:
                model = GameORM(id=data.game_id)
                game = await uow.games.create_one(model)

            data = dict(game_id=game.id)
            await uow.sessions.update_one(client.session, data)
            await uow.commit()
            return ResponseOK(message="Session updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_session_account(
        cls,
        uow: UnitOfWork,
        client_id: UUID,
        _as: Literal["Farmed", "Failed"]
    ):
        async with uow:
            _ = {
                "Farmed": dict(farmed=True),
                "Failed": dict(failed=True)
            }

            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound

            data = _.get(_as)
            await uow.accounts.update_one(client.session.account, data)
            await uow.commit()
            return ResponseOK(message="Account updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def release_session(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is not None:
                data = dict(farmed_at=datetime.utcnow())
                await uow.accounts.update_one(client.session.account, data)
                await uow.sessions.remove_one(client.session)
                await uow.session.commit()
            return ResponseOK(message="Session updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def set_success(
        cls,
        uow: UnitOfWork,
        client_id: UUID
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one_with_joins(ClientORM.id == client_id)
            if client is None:
                raise ClientNotFound
            if client.session is None:
                raise SessionNotFound

            data = dict(success_at=datetime.utcnow())
            await uow.clients.update_one(client, data)
            data = dict(played_at=datetime.utcnow())
            await uow.accounts.update_one(client.session.account, data)
            await uow.commit()
            return ResponseOK(message="Client updated successfully")
