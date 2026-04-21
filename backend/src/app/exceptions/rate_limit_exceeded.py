from src.app.exceptions.base import AppError


class RateLimitExceeded(AppError):
    def __init__(self) -> None:
        super().__init__("rate limit exceeded")
