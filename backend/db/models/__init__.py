
'''
Python이 파일을 “자동으로 다 읽어주지” 않음 
Alembic은 Base.metadata를 보려면,
모델 클래스가 실제로 import되어 실행되어야 metadata에 등록됨

ThemeUniverse를 import하지 않으면 SQLAlchemy는 “테이블이 있는지 모름”

그러면 migration에 아무 변화도 감지되지 않음

그래서 models/__init__.py에 한 번에 import를 모아두면:
Alembic이 import backend.db.models만 해도 모든 모델이 로딩됨
metadata가 채워짐
 '''
 
 
 

from backend.db.models.theme_universe import ThemeUniverse  # noqa: F401
