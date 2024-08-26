from fastapi import (
    HTTPException,
    status
)


class SecretKeyInvalid(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="X-Secret-Key header invalid"
        )
