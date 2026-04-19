from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound


async def handle(request: Request, exc: ConnectionSessionNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "connection session not found"})
