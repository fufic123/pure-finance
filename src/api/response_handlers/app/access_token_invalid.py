from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.access_token_invalid import AccessTokenInvalid


async def handle(request: Request, exc: AccessTokenInvalid) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
