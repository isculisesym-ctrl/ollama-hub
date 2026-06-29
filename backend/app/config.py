"""Application Configuration"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings from environment variables"""

    # App
    APP_NAME: str = "OllamaHub"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./database.db"

    # Ollama
    OLLAMA_HOST: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "neural-chat"
    OLLAMA_TIMEOUT: int = 120

    # Claude
    CLAUDE_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-opus-4-8"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Auth
    API_KEY: str = ""
    AUTH_ENABLED: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = {"env_file": ".env", "case_sensitive": True}

# Load settings
settings = Settings()
