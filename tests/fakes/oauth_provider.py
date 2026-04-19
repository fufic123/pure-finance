from src.app.ports.google_user_info import GoogleUserInfo


class StubOauthProvider:
    def __init__(self, user_info: GoogleUserInfo) -> None:
        self._user_info = user_info

    async def exchange_code(self, code: str, redirect_uri: str) -> GoogleUserInfo:
        return self._user_info
