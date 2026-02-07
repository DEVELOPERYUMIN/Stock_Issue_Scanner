'''
테마 ↔ 종목 매핑 테이블
포함 정보 : 테마명 (예: 반도체, 방산) / 종목코드
                / 종목명  / 시장(KOSPI/KOSDAQ)) 

거래량, 뉴스는 “종목” 단위
해석은 “테마” 단위
'''

from sqlalchemy import String, Integer, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class ThemeUniverse(Base):
    __tablename__ = "theme_universe" # db 만들어질 테이블 이름 지정 
    # mapped_column : 컬럼 정의 함수 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) #id > 기본키 
    theme: Mapped[str] = mapped_column(String(50), nullable=False)       # 테마명 
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)      # 종목코드 
    stock_name: Mapped[str] = mapped_column(String(50), nullable=False)  # 종목명
    market: Mapped[str] = mapped_column(String(10), nullable=True)       # KOSPI/KOSDAQ (선택)

    
    # 빠른검색을 위하여 인덱스 삽입 
    __table_args__ = (
        UniqueConstraint("theme", "ticker", name="uq_theme_ticker"), # 중복 방지용으로 유니크키 추가 
        Index("ix_theme_universe_theme", "theme"),
        Index("ix_theme_universe_ticker", "ticker"),
    )
