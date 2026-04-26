from typing import Callable

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.refresh_token import RefreshToken


class Logout:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(self, refresh_token: str) -> None:
        now = self._clock.now()
        presented_hash = RefreshToken.hash_raw(refresh_token)

        async with self._uow_factory() as uow:
            token = await uow.refresh_tokens.get_by_hash(presented_hash)
            if token is None:
                return
            token.revoke(now)
            await uow.refresh_tokens.update(token)
