# frontend/core/settings.py
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class EnvironmentEnum(str, Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TEST = 'test'


class Settings(BaseSettings):
    # App
    ENVIRONMENT: EnvironmentEnum = Field(..., validation_alias='ENVIRONMENT')
    APP_PORT: int = 8501

    @property
    def API_URL(self) -> str:
        """Retorna a URL base da API com base no ambiente"""
        if self.ENVIRONMENT == EnvironmentEnum.TEST:
            return "http://127.0.0.1:3000"
        else:
            # Para development e production
            return "http://fastapi:3000"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        use_enum_values=True,
        extra='ignore'
    )

settings = Settings()
