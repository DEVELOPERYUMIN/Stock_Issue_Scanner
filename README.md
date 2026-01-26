# Stock_Issue_Scanner

> KOSPI/KOSDAQ stock scanner that classifies theme-based stocks using issue(news) and volume flow signals

```text
issue-flow-scanner/
├─ README.md
├─ .env.example
├─ docker-compose.yml
├─ docs/
│  ├─ erd.png
│  ├─ api.md
│  └─ rules.md
├─ data/
│  └─ seed/
│     ├─ theme_universe.csv
│     └─ issue_rules.yaml
├─ backend/
│  ├─ api/
│  │  ├─ main.py
│  │  ├─ deps.py
│  │  ├─ routers/
│  │  │  ├─ scan.py
│  │  │  ├─ themes.py
│  │  │  └─ health.py
│  │  └─ schemas/
│  │     ├─ scan.py
│  │     ├─ theme.py
│  │     └─ news.py
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ cors.py
│  │  └─ constants.py
│  ├─ db/
│  │  ├─ session.py
│  │  ├─ base.py
│  │  └─ models/
│  │     ├─ theme_universe.py
│  │     ├─ market_daily.py
│  │     ├─ news_raw.py
│  │     ├─ news_stock_map.py
│  │     └─ scan_result_daily.py
│  ├─ collector/
│  ├─ issue/
│  ├─ scanner/
│  └─ utils/
├─ frontend/
│  ├─ pubspec.yaml
│  └─ lib/
└─ tests/
   ├─ test_volume_filter.py
   ├─ test_issue_classifier.py
   └─ test_scanner.py
