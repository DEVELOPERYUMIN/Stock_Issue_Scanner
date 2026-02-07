## 어떤 모델들을 기준으로 migration 만들지 정함 / DB 연결/metadata 지정

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
target_metadata = Base.metadata  # alembic 보고 테이블 설계도는 base.metadata 기준으로 보고, models 를 import 해서 설계도 내용을 채움 

def get_url():
    url = os.getenv("DATABASE_URL") # env에서 db 주소 읽음 // 로컬에서만 3307 클라우드에선 3306 나중에 변경 
    if not url:
        raise RuntimeError("DATABASE_URL is not set in .env")
    return url

def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # 타입변경 (int->bigint) 감지 
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
