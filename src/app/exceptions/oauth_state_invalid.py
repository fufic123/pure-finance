from src.app.exceptions.base import AppError


class OAuthStateInvalid(AppError):
    def __init__(self) -> None:
        super().__init__("oauth state is invalid or expired")
