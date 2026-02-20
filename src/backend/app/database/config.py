from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"

    model_config = {"env_file": ".env", "extra": "allow"}


settings = Settings()
