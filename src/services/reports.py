from math import ceil

from sqlalchemy.exc import DBAPIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_before_delay,
    wait_random
)

from src.dependencies import QueryParams
from src.exceptions import ClientNotFound
from src.models import ReportORM
from src.schemas import (
    ReportCreate,
    ResponseOK,
    RetrieveReportsResponse
)
from src.utils import UnitOfWork


class ReportsService:
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
        params: QueryParams
    ) -> RetrieveReportsResponse:
        async with uow:
            reports = await uow.reports.get_many(
                limit=params.limit,
                offset=params.offset,
                order_by=ReportORM.created_at.desc()
            )
            reports_count = await uow.reports.count()
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
    async def create_report(
        cls,
        uow: UnitOfWork,
        data: ReportCreate
    ) -> ResponseOK:
        async with uow:
            client = await uow.clients.get_one(id=data.client_id)
            if client is None:
                raise ClientNotFound
            model = ReportORM(**data.model_dump())
            await uow.reports.create_one(model)
            await uow.commit()
            return ResponseOK(message="Report created successfully")
