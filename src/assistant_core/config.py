"""Load and validate settings from environment variables and an optional .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from assistant_core.errors import ConfigError


class Settings(BaseModel):
    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    llm_api_key: str | None = Field(default=None, repr=False)
    credit_rate_vnd: int = 450_000
    retake_multiplier: float = 1.5
    max_credits: int = 30
    log_level: str = "INFO"


def load_settings(env_file: str | None = ".env") -> Settings:
    """Read configuration without printing or exposing secrets."""
    if env_file:
        load_dotenv(env_file, override=False)

    try:
        settings = Settings(
            data_dir=Path(os.getenv("ASSISTANT_DATA_DIR", "data")),
            llm_provider=os.getenv("LLM_PROVIDER", "stub"),
            llm_api_key=os.getenv("LLM_API_KEY") or None,
            credit_rate_vnd=int(os.getenv("CREDIT_RATE_VND", "450000")),
            retake_multiplier=float(os.getenv("RETAKE_MULTIPLIER", "1.5")),
            max_credits=int(os.getenv("MAX_CREDITS", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
    except (ValueError, ValidationError) as exc:
        raise ConfigError("One or more assistant settings are invalid.") from exc

    if settings.credit_rate_vnd <= 0:
        raise ConfigError("CREDIT_RATE_VND must be positive.")
    if settings.retake_multiplier < 0:
        raise ConfigError("RETAKE_MULTIPLIER must not be negative.")
    if settings.max_credits < 1:
        raise ConfigError("MAX_CREDITS must be at least 1.")
    if settings.llm_provider != "stub" and not settings.llm_api_key:
        raise ConfigError(f"LLM_API_KEY is required when LLM_PROVIDER={settings.llm_provider!r}.")
    if settings.log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL.")
    return settings
