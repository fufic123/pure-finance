from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user
from src.api.dtos.user_response import UserResponse
from src.domain.entities.user import User

router = APIRouter()


@router.get("/user", response_model=UserResponse)
async def get_user(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse.from_user(user)
