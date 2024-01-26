from fastapi import HTTPException


class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")


class EmailAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Email already exists")


class InactiveUser(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Inactive user")
