import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root = two levels above backend/config/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    OPENROUTER_API_KEY:str
    TAVILY_API_KEY:str
    WEATHERSTACK_API_KEY:str
    
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),  # found no matter which folder you start from
        env_file_encoding="utf-8",
        extra="ignore",
    )
settings = Settings()