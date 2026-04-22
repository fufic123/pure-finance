from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    redis_url: str
    jwt_secret: str
    access_token_lifetime_seconds: int = 900
    refresh_token_lifetime_seconds: int = 2592000
    google_client_id: str
    google_client_secret: str
    oauth_state_lifetime_seconds: int = 600
    cors_allowed_origins: list[str] = []

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _parse_comma_separated(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value
