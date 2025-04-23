from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.schemas.request.user import UserRegister


async def test_login_success(user_data):
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


async def test_refresh_token(jwt_tokens):
    refresh_token = jwt_tokens["refresh_token"]
    original_access_token = jwt_tokens["access_token"]
    payload = {"refresh_token": refresh_token}

    # 2. 얻은 리프레시 토큰으로 재발급 요청 (쿼리 파라미터로 전달 가정)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        refresh_response = await client.post("/auth/refresh-token", json=payload)

    assert refresh_response.status_code == status.HTTP_200_OK
    refresh_data = refresh_response.json()

    assert refresh_data["success"] is True
    assert "data" in refresh_data
    new_tokens = refresh_data["data"]
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["token_type"] == "bearer"
    assert new_tokens["access_token"] != original_access_token
    assert (
        new_tokens["refresh_token"] != refresh_token
    )  # 리프레시 토큰도 새로 발급되는지 확인
