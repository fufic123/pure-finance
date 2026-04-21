from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.connection_session_expired import ConnectionSessionExpired


async def handle(request: Request, exc: ConnectionSessionExpired) -> JSONResponse:
    return JSONResponse(status_code=410, content={"message": "connection session expired"})
