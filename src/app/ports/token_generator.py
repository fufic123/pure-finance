from typing import Protocol


class TokenGenerator(Protocol):
    def generate(self) -> str: ...
