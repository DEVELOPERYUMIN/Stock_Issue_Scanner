
'''
ETL(Extract-Transform-Load)

프로젝트 스캐너 순서 

theme_universe에서 테마-종목 리스트 얻기

market_daily에서 거래량/거래대금 계산

news_raw에서 뉴스 여부 판단

Group A/B 분류

테마 상태 요약 후 API로 반환
'''

import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text # SQLAlchemy로 DB 연결 엔진만들기

# 확인용으로 seed 
CSV_PATH = Path("data/seed/theme_universe.csv")

def main() -> None:
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set in .env")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH.resolve()}")  # 항상 존재하는 지 먼저 보자 / resolve() : 절대경로 출력,디버깅 할 때 좋음 

    # db  연결 엔진 생성 
    engine = create_engine(db_url, future=True) # future : sqlalchemy 최신 스타일 사용 

    # MySQL UPSERT : 없으면 insert / 이미 있으면 update
        # 업서트 조건 : ON DUPLICATE KEY 가 동작하려면 DB 에 UNIQUE키 또는 기본 키 있어야함 
    # UNIQUE(theme,ticker)가 있을 때 가장 깔끔하게 동작
    upsert_sql = text("""
        INSERT INTO theme_universe (theme, ticker, stock_name, market)
        VALUES (:theme, :ticker, :stock_name, :market)
        ON DUPLICATE KEY UPDATE
            stock_name = VALUES(stock_name),
            market = VALUES(market)
    """)

    rows = 0  # ETL 은 로그가 중요하다 확인하고 또 확인하자 
    with engine.begin() as conn, CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:  # db 트랜잭션 시작 / 블럭이 끝나면 자동으로 커밋 에러시 롤백 
        required = {"theme", "ticker", "stock_name", "market"}
        if not required.issubset(set(reader.fieldnames or [])):  # 헤더 검사 
            raise ValueError(f"CSV header must include: {sorted(required)}")

        for r in reader:
            theme = (r.get("theme") or "").strip()
            ticker = (r.get("ticker") or "").strip()
            stock_name = (r.get("stock_name") or "").strip()
            market = (r.get("market") or "").strip()

            if not theme or not ticker or not stock_name:  # 필수 값 누락 행은 스킵 > 실무 etl 에서 많이 씀 
                continue
            
            # db에 실행 / 값을 직접 넣는 게 아니라 파라미터 바인딩함 bc sql injection 방지, 문자열 따옴표 문제 방지, 성능도 더 좋음 
            conn.execute(upsert_sql, {
                "theme": theme, 
                "ticker": ticker,
                "stock_name": stock_name,
                "market": market or None,  # market 빈 문자열이면 공백말고 null 로 저장 / 빈문자열보다는 '값없음'표현이 더 정확함 
            })
            rows += 1

    print(f"Loaded/Upserted rows: {rows}")

if __name__ == "__main__":
    main()
