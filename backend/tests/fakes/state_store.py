class InMemoryStateStore:
    def __init__(self) -> None:
        self._states: set[str] = set()

    async def save(self, state: str, ttl_seconds: int) -> None:
        self._states.add(state)

    async def consume(self, state: str) -> bool:
        if state in self._states:
            self._states.remove(state)
            return True
        return False
