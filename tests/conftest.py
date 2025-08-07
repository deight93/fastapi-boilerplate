from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine

from app.core.dependency import get_db, get_redis
from app.core.setting import settings
from app.main import app

engine = create_async_engine(
    settings.asyncpg_url.unicode_string(), future=True, echo=False
)


@pytest_asyncio.fixture(scope="function")
async def connection() -> AsyncConnection:
    async with engine.connect() as conn:
        yield conn


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(
        settings.asyncpg_url.unicode_string(), future=True, echo=False
    )
    async with async_engine.begin() as conn:
        async_session = AsyncSession(bind=conn, expire_on_commit=False)
        yield async_session
        await async_session.close()
        # rollback은 자동


@pytest_asyncio.fixture(scope="function")
async def redis_client():
    pool = ConnectionPool.from_url(
        settings.redis_url.unicode_string(),
        encoding="utf-8",
        decode_responses=True,
    )
    redis = Redis(connection_pool=pool)
    await redis.flushdb()
    yield redis
    await redis.aclose()
    await pool.disconnect()


@pytest_asyncio.fixture
async def client(redis_client):
    async_engine = create_async_engine(
        settings.asyncpg_url.unicode_string(),
        future=True,
    )

    async def override_get_redis():
        yield redis_client

    app.dependency_overrides[get_redis] = override_get_redis

    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        async def override_get_db():
            yield session

        async def override_get_redis():
            yield redis_client

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_redis] = override_get_redis

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac

        await session.close()
        await transaction.rollback()
        app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def user_token(client):
    register_user = {
        "user_id": "testuser",
        "name": "테스트유저",
        "email": "testuser@example.com",
        "password": "testpassword",
    }

    await client.post("/user/register", json=register_user)
    login_data = {
        "username": register_user["user_id"],
        "password": register_user["password"],
    }
    resp = await client.post("/auth/login", data=login_data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return token
