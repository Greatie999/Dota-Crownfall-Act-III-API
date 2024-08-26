from datetime import datetime

from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.exceptions import VPNAccountNotFound
from src.models import VPNORM
from src.schemas import (
    VPNCreate,
    VPN,
    ResponseOK
)
from src.utils import UnitOfWork


class VPNService:
    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(10)
    )
    async def get_accounts(
        cls,
        uow: UnitOfWork
    ) -> list[VPN]:
        async with uow:
            accounts = await uow.vpn.get_many()
            return [VPN.model_validate(account) for account in accounts]

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
        data: VPNCreate
    ) -> ResponseOK:
        async with uow:
            model = VPNORM(**data.dict())
            await uow.vpn.create_one(model)
            await uow.commit()
            return ResponseOK(message="Account created successfully")

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random(min=0.1, max=0.3),
        retry=retry_if_exception_type(DBAPIError),
        stop=stop_before_delay(30)
    )
    async def acquire_account(
        cls,
        uow: UnitOfWork
    ) -> VPN:
        async with uow:
            account = await uow.vpn.get_one_for_farming()
            if account is None:
                raise VPNAccountNotFound

            data = dict(acquired_at=datetime.utcnow())
            await uow.vpn.update_one(account, data)
            await uow.commit()
            return VPN.model_validate(account)
