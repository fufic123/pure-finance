from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.refresh_token_not_found import RefreshTokenNotFound


async def handle(request: Request, exc: RefreshTokenNotFound) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
