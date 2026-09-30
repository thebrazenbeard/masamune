from __future__ import annotations

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MASAMUNE_", case_sensitive=False)

    github_app_id: str = ""
    github_private_key: str = ""
    github_webhook_secret: str = ""
    github_api_url: str = "https://api.github.com"

    masa_base_url: str = "https://api.openai.com/v1"
    masa_api_key: str = ""
    masa_provider_id: str = "openai-compatible"
    masa_model: str = ""

    mune_base_url: str = "https://api.openai.com/v1"
    mune_api_key: str = ""
    mune_provider_id: str = "openai-compatible"
    mune_model: str = ""

    require_independence: bool = True
    allow_private_repositories: bool = False
    max_context_bytes: int = Field(default=180_000, ge=10_000, le=1_000_000)
    max_file_bytes: int = Field(default=30_000, ge=2_000, le=200_000)
    max_files: int = Field(default=40, ge=1, le=200)
    max_webhook_bytes: int = Field(default=2_000_000, ge=1_024, le=20_000_000)
    request_timeout_seconds: float = Field(default=90, ge=5, le=600)
    model_max_output_tokens: int = Field(default=5_000, ge=500, le=20_000)
    public_base_url: str = "http://localhost:8000"
    host: str = "127.0.0.1"
    port: int = Field(default=8_000, ge=1, le=65_535)
    state_db_path: str = "masamune.sqlite3"
    review_protocol_version: str = "masamune-v0.1"

    @model_validator(mode="after")
    def validate_independence(self) -> Settings:
        if self.require_independence and self.masa_model and self.mune_model:
            same_provider = self.masa_provider_id == self.mune_provider_id
            same_model = self.masa_model == self.mune_model
            if same_provider or same_model:
                raise ValueError(
                    "Masa and Mune must use distinct providers and distinct models when "
                    "MASAMUNE_REQUIRE_INDEPENDENCE=true"
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
