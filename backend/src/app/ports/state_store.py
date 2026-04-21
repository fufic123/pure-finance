from typing import Protocol


class StateStore(Protocol):
    async def save(self, state: str, ttl_seconds: int) -> None: ...

    async def consume(self, state: str) -> bool: ...
