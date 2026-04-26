from typing import Callable

from src.app.ports.clock import Clock
from src.app.ports.jwt_issuer import JwtIssuer
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.user import User


class GetCurrentUser:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        jwt_issuer: JwtIssuer,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._jwt = jwt_issuer

    async def __call__(self, access_token: str) -> User:
        now = self._clock.now()
        user_id = self._jwt.verify(access_token, now)

        async with self._uow_factory() as uow:
            return await uow.users.get_by_id_or_raise(user_id)
