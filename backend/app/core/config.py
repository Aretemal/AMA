from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AMA-API"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Настройки для загрузки файлов
    UPLOAD_DIR: str = "uploads/songs"  # Директория для сохранения файлов песен
    UPLOAD_DIR_NAME: str = "uploads/songs"  # Имя директории для URL
    
    # CORS настройки
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:5174",  # Альтернативный порт Vite
        "http://127.0.0.1:5174",
    ]
    
    # JWT настройки
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-env-variable"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Cookie настройки
    COOKIE_ACCESS_TOKEN_NAME: str = "access_token"
    COOKIE_REFRESH_TOKEN_NAME: str = "refresh_token"
    COOKIE_DOMAIN: str | None = None
    COOKIE_PATH: str = "/"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

