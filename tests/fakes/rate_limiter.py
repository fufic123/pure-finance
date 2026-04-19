from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    async def hit(self, key: str, limit: int, window_seconds: int) -> None:
        self._counts[key] = self._counts.get(key, 0) + 1
        if self._counts[key] > limit:
            raise RateLimitExceeded()


class AllowingRateLimiter:
    async def hit(self, key: str, limit: int, window_seconds: int) -> None:
        return None
