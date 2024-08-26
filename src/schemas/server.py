from datetime import datetime
# from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


class ServerSet(BaseModel):
    name: str = Field(max_length=128)


class Server(BaseModel):
    # id: UUID
    name: str
    # created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
