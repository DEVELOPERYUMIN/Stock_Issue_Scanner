from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "local")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))

    database_url: str = os.getenv("DATABASE_URL", "")
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
