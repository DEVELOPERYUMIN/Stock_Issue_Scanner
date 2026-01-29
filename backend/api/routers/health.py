from fastapi import APIRouter
from sqlalchemy import text
from backend.db.session import SessionLocal

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/health/db")
def health_db():
    # DB 연결 확인용 (SELECT 1)
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    finally:
        db.close()
