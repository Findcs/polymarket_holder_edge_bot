from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/polymarket_holder_edge_bot",
        alias="DATABASE_URL",
    )

    polymarket_api_base_url: str = Field(
        default="https://clob.polymarket.com",
        alias="POLYMARKET_API_BASE_URL",
    )
    polymarket_gamma_api_base_url: str = Field(
        default="https://gamma-api.polymarket.com",
        alias="POLYMARKET_GAMMA_API_BASE_URL",
    )
    http_timeout_seconds: float = Field(default=10.0, alias="HTTP_TIMEOUT_SECONDS")
    http_max_retries: int = Field(default=3, alias="HTTP_MAX_RETRIES")
    http_backoff_seconds: float = Field(default=0.5, alias="HTTP_BACKOFF_SECONDS")

    wallet_score_weight_roi: float = Field(default=0.4, alias="WALLET_SCORE_WEIGHT_ROI")
    wallet_score_weight_recent_roi: float = Field(default=0.3, alias="WALLET_SCORE_WEIGHT_RECENT_ROI")
    wallet_score_weight_sample: float = Field(default=0.15, alias="WALLET_SCORE_WEIGHT_SAMPLE")
    wallet_score_weight_volume: float = Field(default=0.15, alias="WALLET_SCORE_WEIGHT_VOLUME")
    wallet_sample_shrinkage: float = Field(default=20.0, alias="WALLET_SAMPLE_SHRINKAGE")
    wallet_volume_reference: float = Field(default=100000.0, alias="WALLET_VOLUME_REFERENCE")
    wallet_roi_winsor_lower: float = Field(default=-1.0, alias="WALLET_ROI_WINSOR_LOWER")
    wallet_roi_winsor_upper: float = Field(default=3.0, alias="WALLET_ROI_WINSOR_UPPER")

    elite_wallet_threshold: float = Field(default=0.7, alias="ELITE_WALLET_THRESHOLD")
    quality_gap_threshold: float = Field(default=0.1, alias="QUALITY_GAP_THRESHOLD")
    max_entry_slippage: float = Field(default=0.03, alias="MAX_ENTRY_SLIPPAGE")
    max_acceptable_spread: float = Field(default=0.02, alias="MAX_ACCEPTABLE_SPREAD")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object for process-wide reuse."""

    return Settings()
