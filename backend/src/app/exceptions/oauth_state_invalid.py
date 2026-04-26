from src.app.exceptions.base import AppError


class OAuthStateInvalid(AppError):
    status_code = 400

    def __init__(self, *_: object) -> None:
        super().__init__("oauth state is invalid or expired")
