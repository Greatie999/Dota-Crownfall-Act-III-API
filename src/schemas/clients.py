from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

from src.schemas.sessions import SessionInClient


class ClientCreate(BaseModel):
    user_id: UUID
    ip_address: str = Field(max_length=128)
    name: str = Field(max_length=128)


class ClientCreateResponse(BaseModel):
    id: UUID
    ip_address: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class ClientUpdate(BaseModel):
    name: str = Field(max_length=128, default=None)
    active: bool = Field(default=None)


class Client(BaseModel):
    id: UUID
    ip_address: str
    name: str
    active: bool
    user_id: UUID
    success_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    session: Optional[SessionInClient]
    model_config = ConfigDict(from_attributes=True)


class ClientInSession(BaseModel):
    id: UUID
    ip_address: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class RetrieveClientsResponse(BaseModel):
    data: list[Client]
    page: int
    limit: int
    total: int
    pages: int
