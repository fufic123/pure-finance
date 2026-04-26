from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user
from src.api.dtos.users.response import UserResponse
from src.db.models.user import User

router = APIRouter()


@router.get("/user", response_model=UserResponse)
async def get_user(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse.from_user(user)
