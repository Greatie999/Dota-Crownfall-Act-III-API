from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)

from src.dependencies import (
    QueryParams,
    existing_user,
    correct_secret_key,
    UnitOfWorkDependency
)
from src.schemas import (
    User,
    RetrieveReportsResponse,
    ResponseOK,
    ReportCreate
)
from src.services import ReportsService
from src.utils import UnitOfWork

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/",
    response_model=RetrieveReportsResponse
)
async def get_reports(
    params: Annotated[QueryParams, Depends(QueryParams)],
    user: Annotated[User, Depends(existing_user)],
    service: Annotated[ReportsService, Depends(ReportsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("REPEATABLE READ"))]
):
    return await service.get_reports(uow, params=params)


@router.post(
    "/",
    response_model=ResponseOK,
    tags=["Clients"]
)
async def create_report(
    data: ReportCreate,
    sc: Annotated[User, Depends(correct_secret_key)],
    service: Annotated[ReportsService, Depends(ReportsService)],
    uow: Annotated[UnitOfWork, Depends(UnitOfWorkDependency("READ COMMITTED"))]
):
    return await service.create_report(uow, data)
