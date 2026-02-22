"""Application configuration from environment variables."""

import logging
import warnings
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

_INSECURE_DEFAULT_KEY = "change-me-in-production-use-openssl-rand-hex-32"


class Settings(BaseSettings):
    """App settings loaded from env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "mycontext"
    debug: bool = False
    environment: str = "development"  # "development" | "production"
    port: int = 8000

    # Database (SQLite for dev; PostgreSQL for prod)
    database_url: str = "sqlite+aiosqlite:///./mycontext.db"

    # JWT
    secret_key: str = _INSECURE_DEFAULT_KEY
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # Encryption for user API keys
    encryption_key: str | None = None  # Set via env; base64 Fernet key

    # CORS
    cors_origins: str = (
        "https://mycontext.sadhiraai.com,"
        "https://mycontext.pages.dev,"
        "https://sadhiraai.com,"
        "http://localhost:5173,"
        "http://localhost:5174,"
        "http://localhost:3000,"
        "http://127.0.0.1:5173,"
        "http://127.0.0.1:5174"
    )

    # Trusted hosts (production only)
    allowed_hosts: str = "sadhiraai.com,mycontext.sadhiraai.com,api.sadhiraai.com,sadhiraai-api.fly.dev,localhost,127.0.0.1"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    s = Settings()
    if s.is_production and s.secret_key == _INSECURE_DEFAULT_KEY:
        raise RuntimeError(
            "SECRET_KEY must be set in production. "
            "Generate one with: openssl rand -hex 32"
        )
    if s.is_production and s.debug:
        warnings.warn("DEBUG=true in production is unsafe; forcing debug off.", stacklevel=2)
        object.__setattr__(s, "debug", False)
    return s
