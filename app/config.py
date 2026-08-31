from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Platform Reliability Control Plane"
    environment: str = "development"
    log_level: str = "INFO"
    api_key: str = "change-me"
    target_availability: float = 99.9
    target_p95_latency_ms: float = 2000.0
    max_error_rate: float = 0.01
    remediation_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CONTROL_PLANE_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
