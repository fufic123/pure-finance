from src.app.exceptions.base import AppError


class CategoryNotFound(AppError):
    status_code = 404

    def __init__(self, *_: object) -> None:
        super().__init__("category not found")
