from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork


class RevokeAllSessions:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(self, user_id: UUID) -> None:
        now = self._clock.now()
        async with self._uow_factory() as uow:
            await uow.refresh_tokens.revoke_all_for_user(user_id, now)
