# from datetime import datetime
# from typing import Optional
# from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


class VPNCreate(BaseModel):
    username: str = Field(max_length=128)
    password: str = Field(max_length=128)


class VPN(BaseModel):
    # id: UUID
    username: str
    password: str
    # acquired_at: Optional[datetime]
    # created_at: datetime
    # updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
