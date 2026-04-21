from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.rule_not_found import RuleNotFound


async def handle(request: Request, exc: RuleNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "rule not found"})
