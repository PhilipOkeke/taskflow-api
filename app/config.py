"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the API."""

    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./taskflow.db"


def get_settings() -> Settings:
    """Build settings from environment variables."""

    return Settings(
        app_name=getenv("APP_NAME", "TaskFlow API"),
        app_version=getenv("APP_VERSION", "1.0.0"),
        database_url=getenv("DATABASE_URL", "sqlite:///./taskflow.db"),
    )
