 
## SQLAlchemy Base 


## base.metadata : 모든 테이블 정보(스키마) 모아두는 곳

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): # 모든 테이블 클래스가 공통으로 상속받는 부모 클래스
    pass
