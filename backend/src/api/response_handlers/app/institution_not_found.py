from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.institution_not_found import InstitutionNotFound


async def handle(request: Request, exc: InstitutionNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "institution not found"})
