from datetime import datetime
# from uuid import UUID

from pydantic import (
    Field,
    BaseModel,
    ConfigDict
)


class LauncherSet(BaseModel):
    version: str = Field(max_length=128)


class Launcher(BaseModel):
    # id: UUID
    version: str
    # created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
