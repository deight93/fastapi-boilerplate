import uuid
from collections.abc import Generator

import pytest
import redis.asyncio as redis
from fastapi import status
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.core.dependency import get_db, get_redis
from app.main import app
from app.models.base import Base
from app.schemas.request.user import UserRegister


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# 모든 fixture를 function scope로 설정
@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture(scope="function")
def async_engine(postgres_container):
    url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    return create_async_engine(url)


@pytest.fixture(scope="function", autouse=True)
async def setup_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def db_session(async_engine):
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        tx = await session.begin()
        try:
            yield session
        finally:
            if tx.is_active:
                await tx.rollback()


@pytest.fixture(scope="function")
def redis_container():
    with RedisContainer("redis:7.2") as r:
        yield r


@pytest.fixture(scope="function")
async def redis_client(redis_container):
    client = redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=int(redis_container.get_exposed_port(6379)),
        decode_responses=True,
    )
    await client.flushall()
    yield client
    await client.flushall()


@pytest.fixture(scope="function", autouse=True)
def override_dependencies(db_session, redis_client):
    async def _get_db_override():
        yield db_session

    async def _get_redis_override():
        yield redis_client

    app.dependency_overrides[get_db] = _get_db_override
    app.dependency_overrides[get_redis] = _get_redis_override


@pytest.fixture(scope="function")
async def user_data():
    unique_id = uuid.uuid4()
    user_data = {
        "user_id": f"me_user_{unique_id}",
        "email": f"me_{unique_id}@example.com",
        "password": "testpassword123",
        "name": "Me User",
    }
    return user_data


@pytest.fixture(scope="function")
async def jwt_tokens(user_data):
    """Tests successfully retrieving current user info."""
    # 1. Register user first
    register_payload = UserRegister(**user_data).model_dump()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        reg_response = await client.post("/user/register", json=register_payload)
    assert reg_response.status_code == status.HTTP_200_OK
    assert reg_response.json()["success"] is True

    # 2. Login to get token
    login_data = {
        "username": user_data["user_id"],
        "password": user_data["password"],
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        login_response = await client.post(
            "/auth/login", data=login_data
        )  # Use data for form encoding
    assert login_response.status_code == status.HTTP_200_OK
    tokens = login_response.json()
    assert tokens is not None, "토큰을 받아오지 못했습니다"

    return tokens
