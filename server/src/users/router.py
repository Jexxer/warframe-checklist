from typing import Annotated

from auth.utils import get_current_active_user
from fastapi import APIRouter, Depends
from users.schemas import User

router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
