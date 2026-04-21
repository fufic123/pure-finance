from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.account_not_found import AccountNotFound


async def handle(request: Request, exc: AccountNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "account not found"})
