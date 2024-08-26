from contextlib import suppress
from typing import Literal
from uuid import UUID

from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.exceptions import (
    AccountNotFound,
    AccountAlreadyCreated
)
from src.models import (
    AccountORM
)
from src.schemas import (
    AccountCreate,
    Account,
    ResponseOK
)
from src.utils.uow import UnitOfWork


class AccountsService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_account(
        cls,
        uow: UnitOfWork,
        account_username: str
    ) -> Account:
        async with uow:
            account = await uow.accounts.get_one_with_joins(AccountORM.username == account_username)
            if account is None:
                raise AccountNotFound
            return Account.model_validate(account)

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def create_account(
        cls,
        uow: UnitOfWork,
        user_id: UUID,
        data: AccountCreate
    ) -> ResponseOK:
        async with uow:
            data = dict(data, user_id=user_id)
            model = AccountORM(**data)

            with suppress(IntegrityError):
                await uow.accounts.create_one(model)
                await uow.commit()
                return ResponseOK(message="Account created successfully")
            raise AccountAlreadyCreated

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def remove_account(
        cls,
        uow: UnitOfWork,
        account_username: str
    ) -> ResponseOK:
        async with uow:
            account = await uow.accounts.get_one(username=account_username)
            if account is not None:
                await uow.accounts.remove_one(account)
                await uow.commit()
            return ResponseOK(message="Account removed successfully")
