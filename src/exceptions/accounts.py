from fastapi import (
    HTTPException,
    status
)


class AccountNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )


class AccountAlreadyCreated(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already created"
        )


class AccountActionForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account action forbidden"
        )
