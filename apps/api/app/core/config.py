import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # App
    PROJECT_NAME: str = "STAT-SKILL AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"

    # Host & Port
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

    # JWT Security
    JWT_SECRET: str = "stat-skill-ai-super-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    # Uses SQLite by default for standalone portability if PostgreSQL is not active
    DATABASE_URL: str = Field(
        default="sqlite:///./statskill.db",
        description="PostgreSQL URL or SQLite URL"
    )

    # Gemini AI
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Storage
    STORAGE_BACKEND: str = "local"
    STORAGE_DIR: str = "./uploads"
    GCS_BUCKET_NAME: str = ""

    # External Provider Credentials
    IGOT_API_KEY: str = ""
    NSSTA_API_KEY: str = ""


settings = Settings()
