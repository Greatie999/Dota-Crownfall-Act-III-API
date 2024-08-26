from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict
)


class ReportCreate(BaseModel):
    client_id: UUID
    error: str
    traceback: str


class Report(BaseModel):
    id: UUID
    client_id: UUID
    error: str
    traceback: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RetrieveReportsResponse(BaseModel):
    data: list[Report]
    page: int
    limit: int
    total: int
    pages: int
