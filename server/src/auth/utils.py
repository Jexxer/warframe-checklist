from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from auth.config import ALGORITHM, SECRET_KEY
from auth.exceptions import InactiveUser, InvalidCredentials
from auth.schemas import TokenData
from database import db_session
from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from users.models import User as UserModel
from users.schemas import User as UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    OAuth2PasswordBearerWithCookie is an extension of the OAuth2 class that supports token retrieval from a cookie.

    Args:
        tokenUrl (str): The URL where the token can be obtained.
        scheme_name (str, optional): The name of the authentication scheme. Defaults to None.
        scopes (dict, optional): The scopes required for the token. Defaults to None.
        auto_error (bool, optional): Whether to automatically raise an error if authentication fails. Defaults to True.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("access_token")

        if cookie_authorization:
            # Returns jwt token without "Bearer " prefix
            return cookie_authorization.split(" ")[1]
        else:
            raise InvalidCredentials()


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user = db.query(UserModel).filter(UserModel.username == username.lower()).first()
    if user:
        return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: db_session,
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentials()
        token_data = TokenData(username=username)
    except JWTError:
        raise InvalidCredentials()
    user = get_user(db, username=token_data.username)
    if user is None:
        raise InvalidCredentials()
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.is_active is False:
        raise InactiveUser()
    return current_user
