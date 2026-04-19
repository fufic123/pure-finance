from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.user_not_found import UserNotFound


async def handle(request: Request, exc: UserNotFound) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})
