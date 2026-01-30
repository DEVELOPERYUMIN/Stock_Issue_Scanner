## 어떤 모델들을 기준으로 migration 만들지 정함 
'''  
표준 흐름 : 모델 작성 → 마이그레이션 생성 → DB 반영

ORM(SQLAlchemy) : 파이썬 클래스 <-> DB테이블을 연결하는 도구 
테이블을 sql 로 만드는대신 파이썬으로 코드를 만들 수 있음 

migration 마이그레이션 : db 구조 변경 이력을 코드로 관리하는 시스템 
                      적용 : upgrade / 되돌리기 : downgrade 
'''
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from dotenv import load_dotenv
import os

load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 모델 메타데이터 연결
from backend.db.base import Base
import backend.db.models  # noqa: F401  (모델 import로 metadata 채움)

target_metadata = Base.metadata

def get_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set in .env")
    return url

def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
