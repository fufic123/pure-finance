from redis.asyncio import Redis


class RedisStateStore:
    _PREFIX = "oauth:state:"

    def __init__(self, client: Redis) -> None:
        self._client = client

    async def save(self, state: str, ttl_seconds: int) -> None:
        await self._client.set(self._key(state), "", ex=ttl_seconds)

    async def consume(self, state: str) -> bool:
        value = await self._client.getdel(self._key(state))
        return value is not None

    @classmethod
    def _key(cls, state: str) -> str:
        return f"{cls._PREFIX}{state}"
