from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid


async def handle(request: Request, exc: OAuthStateInvalid) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": str(exc)})
