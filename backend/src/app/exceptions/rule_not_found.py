from src.app.exceptions.base import AppError


class RuleNotFound(AppError):
    status_code = 404

    def __init__(self, *_: object) -> None:
        super().__init__("rule not found")
