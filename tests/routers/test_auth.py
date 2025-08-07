import pytest

REGISTER_USER = {
    "user_id": "testuser",
    "name": "테스트유저",
    "email": "testuser@example.com",
    "password": "testpassword",
}


@pytest.mark.asyncio
async def test_login(client):
    await client.post("/user/register", json=REGISTER_USER)
    login_data = {
        "username": REGISTER_USER["user_id"],
        "password": REGISTER_USER["password"],
    }
    resp = await client.post("/auth/login", data=login_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["success"] is True


@pytest.mark.asyncio
async def test_login_fail(client):
    login_data = {"username": "not_exist_user", "password": "wrongpw"}
    resp = await client.post("/auth/login", data=login_data)
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    # 회원가입 및 로그인
    await client.post("/user/register", json=REGISTER_USER)
    login_data = {
        "username": REGISTER_USER["user_id"],
        "password": REGISTER_USER["password"],
    }
    resp = await client.post("/auth/login", data=login_data)
    refresh_token = resp.json()["refresh_token"]
    refresh_data = {"refresh_token": refresh_token}
    resp2 = await client.post("/auth/refresh-token", json=refresh_data)
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["success"] is True
    assert data["data"]["access_token"]
    assert data["data"]["refresh_token"]
