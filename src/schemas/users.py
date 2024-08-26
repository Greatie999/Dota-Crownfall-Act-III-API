from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict
)


class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserJWT(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    status: bool


class User(BaseModel):
    id: UUID
    username: str
    admin: bool
    status: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
