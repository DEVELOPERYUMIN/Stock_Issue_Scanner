## main.py 에 다 넣을 수도 있지만 api 많아질때를 고려. 확장성 위해서 생성 
## 서버 잘 뜨는지 확인용


from fastapi import APIRouter
from sqlalchemy import text
from backend.db.session import SessionLocal

router = APIRouter(tags=["health"])

@router.get("/health") # 부르면 
def health():
    return {"status": "ok"} # 대답 

@router.get("/health/db")
def health_db():
    # DB 연결 확인용 (SELECT 1)
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    finally:
        db.close()
