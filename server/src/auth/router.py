from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    UserAlreadyExists,
)
from src.auth.schemas import Token
from src.auth.utils import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from src.database import db_session
from src.users.models import User as UserModel
from src.users.schemas import UserRegister

router = APIRouter()


@router.get("/token/")
def is_token_valid(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    if current_user:
        return {"valid": True}


@router.post("/token/")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_session,
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
        raise InvalidCredentials()
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


@router.post("/register/", response_model=Token)
async def register_user(
    response: Response,
    user: UserRegister,
    db: db_session,
) -> Token:
    existing_username = (
        db.query(UserModel).filter(UserModel.username == user.username).first()
    )
    if existing_username:
        raise UserAlreadyExists()
    existing_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_email:
        raise EmailAlreadyExists()

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
