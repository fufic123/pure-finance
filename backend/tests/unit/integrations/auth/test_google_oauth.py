import base64
import json
from collections.abc import Callable

import httpx

from src.app.ports.google_user_info import GoogleUserInfo
from src.integrations.auth.google_oauth import GoogleOauthClient

GOOGLE_ID = "google-sub-123"
EMAIL = "user@example.com"
CLIENT_ID = "client-id"
CLIENT_SECRET = "client-secret"
CODE = "auth-code"
REDIRECT = "http://localhost/cb"


class TestExchangeCode:
    async def test_returns_user_info_from_id_token(self) -> None:
        transport = httpx.MockTransport(
            _respond_with_id_token(_build_id_token(GOOGLE_ID, EMAIL))
        )
        async with httpx.AsyncClient(transport=transport) as http:
            client = GoogleOauthClient(CLIENT_ID, CLIENT_SECRET, http)
            result = await client.exchange_code(code=CODE, redirect_uri=REDIRECT)

        assert result == GoogleUserInfo(google_id=GOOGLE_ID, email=EMAIL)

    async def test_posts_code_exchange_to_google_token_endpoint(self) -> None:
        captured: list[httpx.Request] = []
        transport = httpx.MockTransport(
            _capture_and_respond(
                captured, id_token=_build_id_token(GOOGLE_ID, EMAIL)
            )
        )
        async with httpx.AsyncClient(transport=transport) as http:
            client = GoogleOauthClient(CLIENT_ID, CLIENT_SECRET, http)
            await client.exchange_code(code=CODE, redirect_uri=REDIRECT)

        assert len(captured) == 1
        request = captured[0]
        assert str(request.url) == "https://oauth2.googleapis.com/token"
        form = dict(httpx.QueryParams(request.content.decode()))
        assert form == {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": CODE,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT,
        }


def _respond_with_id_token(
    id_token: str,
) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"id_token": id_token, "access_token": "ignored"},
        )

    return handler


def _capture_and_respond(
    captured: list[httpx.Request],
    id_token: str,
) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            200,
            json={"id_token": id_token, "access_token": "ignored"},
        )

    return handler


def _build_id_token(sub: str, email: str) -> str:
    header = _b64url(b'{"alg":"RS256","typ":"JWT"}')
    payload = _b64url(json.dumps({"sub": sub, "email": email}).encode())
    return f"{header}.{payload}.signature-placeholder"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()
