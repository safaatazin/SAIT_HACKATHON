from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = "*"

    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_storage_bucket: str = "room-frames"

    ai_provider: str = "openai"
    openai_api_key: str = ""
    openai_vision_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    gemini_vision_model: str = "gemini-2.0-flash"
    anthropic_api_key: str = ""
    anthropic_vision_model: str = "claude-3-5-haiku-latest"

    diff_ignore_threshold: float = 8.0
    diff_save_only_threshold: float = 18.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
