## db 연결 만드는 곳 
##  db 는 앱 전체에서 계속 쓰는 핵심자원 >> 한곳에서 만들고 어디서든 가져다 쓰게 하는 게 정석

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

if not settings.database_url:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True, # 요청 전 연결 살아있는지 한 번 확인 > 실무안전성땜에 거의 넣는다고 함 
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
