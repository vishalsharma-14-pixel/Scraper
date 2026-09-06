from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://scrapetrack:scrapetrack@postgres:5432/scrapetrack"
    redis_url: str = "redis://redis:6379/0"

    default_user_agent: str = "Mozilla/5.0 (compatible; ScrapeTrackBot/1.0; +local-tool)"
    request_timeout_seconds: float = 15.0
    max_fetch_retries: int = 1
    retry_backoff_seconds: float = 2.0
    playwright_nav_timeout_seconds: float = 20.0

    min_poll_interval_seconds: int = 300
    dispatch_interval_seconds: float = 60.0


settings = Settings()
