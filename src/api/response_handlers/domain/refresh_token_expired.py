from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired


async def handle(request: Request, exc: RefreshTokenExpired) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
