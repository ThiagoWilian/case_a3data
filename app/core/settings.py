# app/core/settings.py
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
    APP_PORT: int = 3000


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        use_enum_values=True,
        extra='ignore'
    )

settings = Settings()
