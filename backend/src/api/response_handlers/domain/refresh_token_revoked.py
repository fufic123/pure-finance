from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked


async def handle(request: Request, exc: RefreshTokenRevoked) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
