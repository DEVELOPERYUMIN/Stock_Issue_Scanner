# Stock_Issue_Scanner
KOSPI/KOSDAQ stock scanner that classifies theme-based stocks using issue(news) and volume flow signals



issue-flow-scanner/
├─ README.md
├─ .env.example
├─ docker-compose.yml                 # mysql + backend
├─ docs/
│  ├─ erd.png
│  ├─ api.md
│  └─ rules.md                        # 뉴스 유효 이슈 규칙/키워드
├─ data/
│  └─ seed/
│     ├─ theme_universe.csv           # 테마-종목 맵(필수)
│     └─ issue_rules.yaml             # 유효이슈 분류 규칙(정책/실적/기술/규제/산업)
│
├─ backend/
│  ├─ api/
│  │  ├─ main.py                      # FastAPI 엔트리
│  │  ├─ deps.py
│  │  ├─ routers/
│  │  │  ├─ scan.py                   # 핵심: /scan?date=YYYY-MM-DD
│  │  │  ├─ themes.py                 # /themes/{date} (요약 리스트)
│  │  │  └─ health.py
│  │  └─ schemas/
│  │     ├─ scan.py                   # 테마별 그룹A/B 응답 스키마
│  │     ├─ theme.py
│  │     └─ news.py
│  │
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ cors.py                      # Flutter Web 연동
│  │  └─ constants.py                 # VOL_RATIO>=2, VALUE>=50억, lookback 등
│  │
│  ├─ db/
│  │  ├─ session.py
│  │  ├─ base.py
│  │  ├─ models/
│  │  │  ├─ theme_universe.py
│  │  │  ├─ market_daily.py
│  │  │  ├─ news_raw.py
│  │  │  ├─ news_stock_map.py         # 뉴스-종목 매핑
│  │  │  └─ scan_result_daily.py      # 날짜별 스캔 결과 캐시(권장)
│  │  └─ migrations/
│  │
│  ├─ collector/
│  │  ├─ market_daily.py              # 종목 거래량/거래대금 수집
│  │  ├─ news_daily.py                # 뉴스 수집 + 중복 제거
│  │  ├─ loaders.py                   # theme_universe 적재
│  │  └─ sources/
│  │     ├─ market_source.py
│  │     └─ news_source.py
│  │
│  ├─ issue/
│  │  ├─ dedup.py                     # 제목/URL/본문 해시 중복 제거
│  │  ├─ classifier.py                # 유효 이슈 판별(규칙 기반)
│  │  ├─ stock_linker.py              # 뉴스→종목 매칭(종목명/티커/별칭)
│  │  └─ summarizer.py                # 뉴스 요약(룰 기반 1줄 또는 LLM 옵션)
│  │
│  ├─ scanner/
│  │  ├─ run_scan.py                  # 핵심 엔진: date 입력 → 결과 생성
│  │  ├─ volume_filter.py             # AVG_VOL_20, VOL_RATIO, VALUE 조건
│  │  ├─ group_assign.py              # 그룹 A/B 분류
│  │  ├─ theme_state.py               # 테마 상태 한 줄 요약
│  │  └─ cache.py                     # scan_result_daily 저장/조회
│  │
│  └─ utils/
│     ├─ trading_calendar.py          # 거래일/휴장일 처리
│     ├─ formatters.py                # 50억 표시 등
│     └─ dates.py
│
├─ frontend/                           # Flutter Web
│  ├─ pubspec.yaml
│  ├─ web/
│  └─ lib/
│     ├─ main.dart
│     ├─ app.dart
│     ├─ routes/
│     │  └─ app_router.dart            # /, /theme/:name?date=...
│     ├─ pages/
│     │  ├─ scan_page.dart             # 날짜 선택 + 전체 테마 결과
│     │  └─ theme_detail_page.dart     # 테마 상세 (A/B 리스트)
│     ├─ widgets/
│     │  ├─ theme_section.dart         # 테마 블록(상태요약 포함)
│     │  ├─ group_table.dart           # A/B 테이블
│     │  ├─ news_chips.dart            # 뉴스 요약 칩/링크
│     │  └─ date_picker_bar.dart
│     ├─ models/
│     │  ├─ scan_result.dart           # 테마별 A/B 구조
│     │  ├─ stock_item.dart
│     │  └─ news_item.dart
│     ├─ services/
│     │  ├─ api_client.dart
│     │  └─ scan_service.dart          # /scan 호출
│     ├─ state/
│     │  └─ scan_provider.dart         # Riverpod/Provider
│     └─ utils/
│        └─ format.dart
│
└─ tests/
   ├─ test_volume_filter.py
   ├─ test_issue_classifier.py
   └─ test_scanner.py
