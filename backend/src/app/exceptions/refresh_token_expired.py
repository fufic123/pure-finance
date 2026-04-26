from uuid import UUID

from src.app.exceptions.base import AppError


class RefreshTokenExpired(AppError):
    status_code = 401

    def __init__(self, token_id: UUID) -> None:
        self.token_id = token_id
        super().__init__(f"refreshtokenexpired {token_id}")
