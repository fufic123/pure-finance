from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.category_not_found import CategoryNotFound


async def handle(request: Request, exc: CategoryNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "category not found"})
