from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.setting import settings

async_engine = create_async_engine(
    settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
engine = create_engine(settings.postgres_url.unicode_string())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
