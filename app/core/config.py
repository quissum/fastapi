from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/tasks"
    )
    auth_secret: str = Field(default="CHANGE_ME_SUPER_SECRET")
    reset_secret: str = Field(default="CHANGE_ME_RESET_SECRET")
    verify_secret: str = Field(default="CHANGE_ME_VERIFY_SECRET")
    access_token_lifetime_seconds: int = Field(default=60 * 60)

    cookie_name: str = Field(default="auth")
    cookie_max_age_seconds: int = Field(default=60 * 60 * 24 * 7)
    cookie_secure: bool = Field(default=False)  # local False, prod True

    cors_origins: list[str] = Field(default_factory=lambda: [
                                    "http://localhost:3000"])
    echo_sql: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
