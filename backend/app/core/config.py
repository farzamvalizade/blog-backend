import warnings
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Blog API"
    API_V1_STR: str = "/api/v1"

    FASTAPI_ENV: Literal["development", "production"] = "development"

    SECRET_KEY: str = "changethis"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str = "postgresql+psycopg://blog:blog_dev_password@localhost:5432/blog"

    FIRST_SUPERUSER: str = "admin@dev.com"
    FIRST_SUPERUSER_PASSWORD: str = "Test@1234"

    BACKEND_CORS_ORIGINS: list[str] = []

    @field_validator("DATABASE_URL")
    @classmethod
    def use_psycopg_driver(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    def _check_secret(self, name: str, value: str) -> None:
        if value == "changethis":
            message = f'{name} is using the default "changethis" value.'

            if self.FASTAPI_ENV == "development":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    def validate_secrets(self) -> None:
        self._check_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_secret(
            "FIRST_SUPERUSER_PASSWORD",
            self.FIRST_SUPERUSER_PASSWORD,
        )


settings = Settings()
settings.validate_secrets()
