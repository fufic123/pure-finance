from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory


async def handle(request: Request, exc: CannotDeleteSystemCategory) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": "cannot delete system category"})
