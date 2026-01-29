##  main.py > fastapi 앱 시작점 
## fastapi 는 앱 객체가 있어야 서버 띄움 > 엔트리 필요 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# CORS : 플러터 웹 브라우저에서 api 호출할 떄 브라우저는 보안 때문에 다른 출처 요청막아서 필요. / 출처가 다르니까 필요함 

from backend.core.config import settings
from backend.api.routers.health import router as health_router

def create_app() -> FastAPI:
    app = FastAPI(title="Stock Issue Scanner API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)  # 이 라우터(기능)도 메인에 추가
    return app

app = create_app()
