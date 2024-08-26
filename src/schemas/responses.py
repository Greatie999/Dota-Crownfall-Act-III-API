from typing import Optional

from pydantic import (
    BaseModel,
    Field
)


class ResponseOK(BaseModel):
    message: Optional[str] = Field(default=None)
    success: bool = True
