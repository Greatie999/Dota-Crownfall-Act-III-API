from datetime import datetime
from typing import (
    Optional
)
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

from src.schemas.sessions import SessionInAccount


class AccountCreate(BaseModel):
    username: str = Field(max_length=128)
    password: str = Field(max_length=128)
    shared_secret: str = Field(max_length=128)
    steam_id: int


class Account(BaseModel):
    id: UUID
    username: str
    password: str
    shared_secret: str
    steam_id: int
    farmed: bool
    failed: bool
    session: Optional[SessionInAccount]
    farmed_at: Optional[datetime]
    played_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AccountInSession(BaseModel):
    id: UUID
    username: str
    steam_id: int
    model_config = ConfigDict(from_attributes=True)


class RetrieveAccountsResponse(BaseModel):
    data: list[Account]
    page: int
    limit: int
    total: int
    pages: int
