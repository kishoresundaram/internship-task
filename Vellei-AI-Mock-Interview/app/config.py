from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Vellei AI Mock Interview Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./vellei_interview.db"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    JWT_SECRET_KEY: str = "vellei-mock-interview-development-secret"
    JWT_ALGORITHM: str = "HS256"

    MAX_ANSWER_LENGTH: int = 10000
    MAX_QUESTION_COUNT: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()