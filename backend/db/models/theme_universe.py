from sqlalchemy import String, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class ThemeUniverse(Base):
    __tablename__ = "theme_universe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    theme: Mapped[str] = mapped_column(String(50), nullable=False)       # 테마명 (예: 반도체)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)      # 종목코드 (예: 005930)
    stock_name: Mapped[str] = mapped_column(String(50), nullable=False)  # 종목명
    market: Mapped[str] = mapped_column(String(10), nullable=True)       # KOSPI/KOSDAQ (선택)

    __table_args__ = (
        Index("ix_theme_universe_theme", "theme"),
        Index("ix_theme_universe_ticker", "ticker"),
    )
