from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded


async def handle(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(status_code=429, content={"message": str(exc)})
