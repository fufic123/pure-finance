from typing import Callable

from src.app.ports.clock import Clock
from src.app.ports.jwt_issuer import JwtIssuer
from src.app.ports.token_generator import TokenGenerator
from src.app.ports.unit_of_work import UnitOfWork
from src.app.services.auth.token_pair import TokenPair
from src.db.models.refresh_token import RefreshToken
from src.app.exceptions.refresh_token_not_found import RefreshTokenNotFound
from src.app.exceptions.refresh_token_revoked import RefreshTokenRevoked


class RefreshTokens:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        jwt_issuer: JwtIssuer,
        token_generator: TokenGenerator,
        refresh_lifetime_seconds: int,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._jwt = jwt_issuer
        self._token_generator = token_generator
        self._refresh_lifetime_seconds = refresh_lifetime_seconds

    async def __call__(self, refresh_token: str) -> TokenPair:
        now = self._clock.now()
        presented_hash = RefreshToken.hash_raw(refresh_token)

        async with self._uow_factory() as uow:
            current = await uow.refresh_tokens.get_by_hash(presented_hash)
            if current is None:
                raise RefreshTokenNotFound()

            try:
                current.ensure_usable(now)
            except RefreshTokenRevoked:
                await uow.refresh_tokens.revoke_all_for_user(current.user_id, now)
                raise

            current.revoke(now)
            await uow.refresh_tokens.update(current)

            new_raw = self._token_generator.generate()
            new_token = RefreshToken.issue(
                user_id=current.user_id,
                token_hash=RefreshToken.hash_raw(new_raw),
                now=now,
                lifetime_seconds=self._refresh_lifetime_seconds,
            )
            await uow.refresh_tokens.add(new_token)

            access = self._jwt.issue(user_id=current.user_id, now=now)

        return TokenPair(access=access, refresh=new_raw)
