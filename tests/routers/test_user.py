import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.user import User
from app.schemas.request.user import UserRegister


@pytest.mark.asyncio
async def test_register(db_session: AsyncSession, user_data):
    payload = UserRegister(**user_data).model_dump()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/user/register", json=payload)

    # 1. Check HTTP response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["message"] is None

    # 2. Check if user exists in the database
    stmt = select(User).where(User.user_id == user_data["user_id"])
    result = await db_session.execute(stmt)
    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.user_id == user_data["user_id"]
    assert db_user.email == user_data["email"]
    assert db_user.name == user_data["name"]
    assert db_user.hashed_password is not None  # Check password was hashed
    assert (
        db_user.hashed_password != user_data["password"]
    )  # Ensure it's not plain text


@pytest.mark.asyncio
async def test_read_user_me(db_session: AsyncSession, jwt_tokens):
    access_token = jwt_tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Request /user/me with the token
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/user/me", headers=headers)

    # 4. Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["message"] is None
    assert "data" in data
