from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired
from src.domain.exceptions.refresh_token_not_found import RefreshTokenNotFound
from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked
from src.domain.exceptions.user_not_found import UserNotFound


async def handle_refresh_token_expired(request: Request, exc: RefreshTokenExpired) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def handle_refresh_token_not_found(request: Request, exc: RefreshTokenNotFound) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def handle_refresh_token_revoked(request: Request, exc: RefreshTokenRevoked) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def handle_user_not_found(request: Request, exc: UserNotFound) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
