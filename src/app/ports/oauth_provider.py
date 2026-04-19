from typing import Protocol

from src.app.ports.google_user_info import GoogleUserInfo


class OauthProvider(Protocol):
    async def exchange_code(self, code: str, redirect_uri: str) -> GoogleUserInfo: ...
