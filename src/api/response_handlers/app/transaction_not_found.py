from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.transaction_not_found import TransactionNotFound


async def handle(request: Request, exc: TransactionNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "transaction not found"})
