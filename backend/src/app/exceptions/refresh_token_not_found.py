from src.app.exceptions.base import AppError


class RefreshTokenNotFound(AppError):
    status_code = 401

    def __init__(self, *_: object) -> None:
        super().__init__("refresh token not found")
