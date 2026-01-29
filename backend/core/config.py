## 설정값을 한 곳에서 읽어서 앱 전체에서 쓰게 함 
# .env 에있는 설정 매번 os.gentenv 로 불러오면, 여기저기 중복되거나,
# 실수로 이름틀리면 런타임 에러 -> 관리 어려움 

from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()  # .env 읽어서 환경변수로 등록 


## settings 로 설정묶음으로 한번에 관리 
class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "local")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))

    database_url: str = os.getenv("DATABASE_URL", "")
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
