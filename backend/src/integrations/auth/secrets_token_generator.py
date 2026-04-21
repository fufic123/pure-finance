import secrets


class SecretsTokenGenerator:
    def __init__(self, nbytes: int = 32) -> None:
        self._nbytes = nbytes

    def generate(self) -> str:
        return secrets.token_urlsafe(self._nbytes)
