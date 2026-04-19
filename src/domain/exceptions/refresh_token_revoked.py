from uuid import UUID

from src.domain.exceptions.base import DomainError


class RefreshTokenRevoked(DomainError):
    def __init__(self, token_id: UUID) -> None:
        self.token_id = token_id
        super().__init__(f"refresh token {token_id} is revoked")
