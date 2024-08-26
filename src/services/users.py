from datetime import datetime
from math import ceil
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from jose import (
    JWTError,
    jwt
)
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.dependencies import QueryParams
from src.exceptions import (
    UserNotFound,
    UserNotAuthorized,
    UserIncorrectPassword
)
from src.models import (
    UserORM,
    AccountORM,
    ClientORM,
    ReportORM
)
from src.schemas import (
    UserToken,
    UserJWT,
    User,
    UserUpdate,
    ResponseOK,
    RetrieveAccountsResponse,
    RetrieveClientsResponse,
    RetrieveReportsResponse
)
from src.settings import settings
from src.utils import UnitOfWork


class UsersService:
    @classmethod
    async def verify_token(
        cls,
        token: str
    ) -> UserJWT:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            user = payload.get("user")
            return UserJWT.model_validate(user)

        except (
            AttributeError,
            JWTError,
            ValidationError
        ):
            raise UserNotAuthorized

    @classmethod
    def create_access_token(
        cls,
        user: UserORM
    ) -> UserToken:
        data = UserJWT.model_validate(user)
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "user": data.model_dump(),
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            settings.ALGORITHM
        )
        return UserToken(access_token=token)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def authenticate_user(
        cls,
        uow: UnitOfWork,
        data: OAuth2PasswordRequestForm
    ) -> UserToken:
        async with uow:
            user = await uow.users.get_one(username=data.username)
            if user is None:
                raise UserNotFound
            if data.password != user.password:
                raise UserIncorrectPassword
            return cls.create_access_token(user)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_current_user(
        cls,
        uow: UnitOfWork,
        data: UserJWT
    ) -> User:
        async with uow:
            user = await uow.users.get_one(username=data.username)
            if user is None:
                raise UserNotFound
            return User.model_validate(user)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def update_user(
        cls,
        uow: UnitOfWork,
        user_id: UUID,
        data: UserUpdate
    ) -> ResponseOK:
        async with uow:
            user = await uow.users.get_one(id=user_id)
            if user is None:
                raise UserNotFound
            await uow.users.update_one(user, data.model_dump(exclude_unset=True))
            await uow.commit()
            return ResponseOK(message="User updated successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_user_accounts(
        cls,
        uow: UnitOfWork,
        user_id: UUID,
        params: QueryParams
    ) -> RetrieveAccountsResponse:
        async with uow:
            accounts = await uow.accounts.get_many_with_joins(
                AccountORM.user_id == user_id,
                limit=params.limit,
                offset=params.offset
            )
            accounts_count = await uow.accounts.count(AccountORM.user_id == user_id)
            pages = ceil(accounts_count / params.limit) if params.limit else 1
            return RetrieveAccountsResponse(
                data=accounts,
                page=params.page,
                limit=params.limit,
                total=accounts_count,
                pages=pages
            )

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_user_clients(
        cls,
        uow: UnitOfWork,
        user_id: UUID,
        params: QueryParams
    ) -> RetrieveClientsResponse:
        async with uow:
            clients = await uow.clients.get_many_with_joins(
                ClientORM.user_id == user_id,
                limit=params.limit,
                offset=params.offset
            )
            clients_count = await uow.clients.count(ClientORM.user_id == user_id)
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
    async def get_user_clients_reports(
        cls,
        uow: UnitOfWork,
        user_id: UUID,
        params: QueryParams
    ) -> RetrieveReportsResponse:
        async with uow:
            clients = await uow.clients.get_many_with_joins(
                ClientORM.user_id == user_id,
                limit=params.limit,
                offset=params.offset
            )
            reports = await uow.reports.get_many(
                ReportORM.client_id.in_([client.id for client in clients]),
                limit=params.limit,
                offset=params.offset,
                order_by=ReportORM.created_at.desc()
            )
            reports_count = await uow.reports.count(ReportORM.client_id.in_([client.id for client in clients]))
            pages = ceil(reports_count / params.limit) if params.limit else 1
            return RetrieveReportsResponse(
                data=reports,
                page=params.page,
                limit=params.limit,
                total=reports_count,
                pages=pages
            )
