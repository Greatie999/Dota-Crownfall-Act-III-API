from datetime import datetime
# from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict
)


class StatusSet(BaseModel):
    value: bool


class Status(BaseModel):
    # id: UUID
    value: bool
    # created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
