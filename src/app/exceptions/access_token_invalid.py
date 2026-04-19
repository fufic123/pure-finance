from src.app.exceptions.base import AppError


class AccessTokenInvalid(AppError):
    def __init__(self) -> None:
        super().__init__("access token is invalid")
