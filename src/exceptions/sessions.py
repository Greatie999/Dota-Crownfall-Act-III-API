from fastapi import (
    HTTPException,
    status
)


class SessionNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )


class SessionActionForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session action forbidden"
        )
