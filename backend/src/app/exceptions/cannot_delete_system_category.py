from src.app.exceptions.base import AppError


class CannotDeleteSystemCategory(AppError):
    status_code = 403

    def __init__(self, *_: object) -> None:
        super().__init__("cannot delete system category")
