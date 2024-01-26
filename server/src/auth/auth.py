from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.dependencies import db_dependency
from src.models.User import User as UserModel
from src.schemas.User import User

# TODO move these constants to env before final deployment
# ? If you are reading this from github, these are not the real secrets
SECRET_KEY = "8a6b14faba9ca9866e9c9bfe4715254170824294b507b6d2758d4307cb210b77"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 2


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str


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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

router = APIRouter()


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
    db: db_dependency,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
) -> Token:
    """
    Authenticates the user and generates an access token.

    Args:
        response (Response): The response object.
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.

    Returns:
        Token: The access token.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires_delta
    )

    access_token_max_age_seconds = 60 * 60 * 24 * 7 * 2  # two weeks
    access_token_expires = datetime.now(timezone.utc) + timedelta(weeks=2)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=access_token_max_age_seconds,
        expires=access_token_expires,
        samesite="none",
        secure=True,
    )
    return Token(access_token=access_token, token_type="bearer")


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register/", response_model=Token)
async def register_user(
    response: Response,
    user: UserRegister,
    db: db_dependency,
) -> Token:
    existing_username = (
        db.query(UserModel).filter(UserModel.username == user.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    existing_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken",
        )

    hashed_password = get_password_hash(user.password)
    user = UserModel(
        username=user.username.lower(),
        email=user.email.lower(),
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires_delta
    )

    access_token_max_age_seconds = 60 * 60 * 24 * 7 * 2  # two weeks
    access_token_expires = datetime.now(timezone.utc) + timedelta(weeks=2)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=access_token_max_age_seconds,
        expires=access_token_expires,
        samesite="none",
        secure=True,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
