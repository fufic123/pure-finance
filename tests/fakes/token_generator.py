class StubTokenGenerator:
    def __init__(self, value: str) -> None:
        self._value = value

    def generate(self) -> str:
        return self._value
