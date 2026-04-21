import base64
import json
from typing import Any

import httpx

from src.app.ports.google_user_info import GoogleUserInfo


class GoogleOauthClient:
    _TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._http = http_client

    async def exchange_code(self, code: str, redirect_uri: str) -> GoogleUserInfo:
        response = await self._http.post(
            self._TOKEN_ENDPOINT,
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
        )
        response.raise_for_status()
        claims = self._decode_id_token(response.json()["id_token"])
        return GoogleUserInfo(
            google_id=claims["sub"],
            email=claims["email"],
        )

    @staticmethod
    def _decode_id_token(id_token: str) -> dict[str, Any]:
        _, payload, _ = id_token.split(".")
        padding = "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload + padding))
