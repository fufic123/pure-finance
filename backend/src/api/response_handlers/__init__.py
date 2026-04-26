from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.app.exceptions.base import AppError


async def _handle_app_error(request: Request, exc: Exception) -> JSONResponse:
    err = exc if isinstance(exc, AppError) else AppError()
    return JSONResponse(status_code=err.status_code, content={"message": str(err)})


def install_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _handle_app_error)  # type: ignore[arg-type]
