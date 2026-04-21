from datetime import datetime, timedelta
from uuid import UUID

import jwt

from src.app.exceptions.access_token_invalid import AccessTokenInvalid


class PyJwtIssuer:
    def __init__(
        self,
        secret: str,
        lifetime_seconds: int,
        algorithm: str = "HS256",
    ) -> None:
        self._secret = secret
        self._lifetime_seconds = lifetime_seconds
        self._algorithm = algorithm

    def issue(self, user_id: UUID, now: datetime) -> str:
        payload = {
            "sub": str(user_id),
            "exp": int(
                (now + timedelta(seconds=self._lifetime_seconds)).timestamp()
            ),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def verify(self, token: str, now: datetime) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
                options={"verify_exp": False},
            )
        except jwt.InvalidTokenError as e:
            raise AccessTokenInvalid() from e

        exp = payload.get("exp")
        sub = payload.get("sub")
        if exp is None or sub is None:
            raise AccessTokenInvalid()

        if now.timestamp() >= exp:
            raise AccessTokenInvalid()

        try:
            return UUID(sub)
        except ValueError as e:
            raise AccessTokenInvalid() from e
