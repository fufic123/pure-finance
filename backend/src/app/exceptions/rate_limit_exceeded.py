from src.app.exceptions.base import AppError


class RateLimitExceeded(AppError):
    status_code = 429

    def __init__(self, *_: object) -> None:
        super().__init__("rate limit exceeded")
