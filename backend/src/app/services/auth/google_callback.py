from typing import Callable

from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.ports.clock import Clock
from src.app.ports.jwt_issuer import JwtIssuer
from src.app.ports.oauth_provider import OauthProvider
from src.app.ports.state_store import StateStore
from src.app.ports.token_generator import TokenGenerator
from src.app.ports.unit_of_work import UnitOfWork
from src.app.services.auth.token_pair import TokenPair
from src.domain.entities.refresh_token import RefreshToken
from src.domain.entities.user import User


class GoogleCallback:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        jwt_issuer: JwtIssuer,
        oauth_provider: OauthProvider,
        state_store: StateStore,
        token_generator: TokenGenerator,
        refresh_lifetime_seconds: int,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._jwt = jwt_issuer
        self._oauth = oauth_provider
        self._state_store = state_store
        self._token_generator = token_generator
        self._refresh_lifetime_seconds = refresh_lifetime_seconds

    async def __call__(self, code: str, redirect_uri: str, state: str) -> TokenPair:
        if not await self._state_store.consume(state):
            raise OAuthStateInvalid()

        now = self._clock.now()
        info = await self._oauth.exchange_code(code, redirect_uri)

        async with self._uow_factory() as uow:
            user = await uow.users.get_by_google_id(info.google_id)
            if user is None:
                user = User.register(
                    google_id=info.google_id,
                    email=info.email,
                    now=now,
                )
                await uow.users.add(user)

            access = self._jwt.issue(user_id=user.id, now=now)
            raw_refresh = self._token_generator.generate()
            refresh = RefreshToken.issue(
                user_id=user.id,
                token_hash=RefreshToken.hash_raw(raw_refresh),
                now=now,
                lifetime_seconds=self._refresh_lifetime_seconds,
            )
            await uow.refresh_tokens.add(refresh)

        return TokenPair(access=access, refresh=raw_refresh)
