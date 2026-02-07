from dotenv import load_dotenv
load_dotenv()

from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    BETTER_AUTH_SECRET: str = 'change-this-secret'
    BETTER_AUTH_URL: str = 'http://localhost:3000'

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: str = "" # Changed to string, default empty

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()