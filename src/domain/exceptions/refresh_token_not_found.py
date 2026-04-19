from src.domain.exceptions.base import DomainError


class RefreshTokenNotFound(DomainError):
    def __init__(self) -> None:
        super().__init__("refresh token not found")
