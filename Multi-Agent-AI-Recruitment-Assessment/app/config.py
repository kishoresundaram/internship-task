from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent AI Recruitment Assessment System"
    app_env: str = "development"
    debug: bool = True

    database_url: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/"
        "recruitment_assessment"
    )

    qdrant_url: str = ""
    qdrant_api_key: str = ""

    redis_url: str = "redis://localhost:6379/0"

    e2b_api_key: str = ""

    llm_model: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()