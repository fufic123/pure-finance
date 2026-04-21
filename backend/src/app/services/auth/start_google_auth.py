from urllib.parse import urlencode

from src.app.ports.state_store import StateStore
from src.app.ports.token_generator import TokenGenerator


class StartGoogleAuth:
    _AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    _SCOPE = "openid email"

    def __init__(
        self,
        state_store: StateStore,
        token_generator: TokenGenerator,
        client_id: str,
        state_lifetime_seconds: int,
    ) -> None:
        self._state_store = state_store
        self._token_generator = token_generator
        self._client_id = client_id
        self._state_lifetime_seconds = state_lifetime_seconds

    async def __call__(self, redirect_uri: str) -> str:
        state = self._token_generator.generate()
        await self._state_store.save(state, self._state_lifetime_seconds)
        params = {
            "client_id": self._client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": self._SCOPE,
            "state": state,
            "access_type": "online",
        }
        return f"{self._AUTHORIZATION_URL}?{urlencode(params)}"
