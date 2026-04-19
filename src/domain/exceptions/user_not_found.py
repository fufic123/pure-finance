from src.domain.exceptions.base import DomainError


class UserNotFound(DomainError):
    def __init__(self) -> None:
        super().__init__("user not found")
