from fastapi import Depends

from src.api.dependencies import get_current_user
from src.app.exceptions.base import AppError
from src.db.models.user import User


class AdminRequired(AppError):
    status_code = 403

    def __init__(self, *_: object) -> None:
        super().__init__("admin access required")


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise AdminRequired()
    return user
