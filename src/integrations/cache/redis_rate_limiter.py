from redis.asyncio import Redis

from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded


class RedisRateLimiter:
    _PREFIX = "ratelimit:"

    def __init__(self, client: Redis) -> None:
        self._client = client

    async def hit(self, key: str, limit: int, window_seconds: int) -> None:
        prefixed = f"{self._PREFIX}{key}"
        count = await self._client.incr(prefixed)
        if count == 1:
            await self._client.expire(prefixed, window_seconds)
        if count > limit:
            raise RateLimitExceeded()
