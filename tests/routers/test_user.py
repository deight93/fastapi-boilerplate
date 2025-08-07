import pytest

REGISTER_USER = {
    "user_id": "testuser",
    "name": "테스트유저",
    "email": "testuser@example.com",
    "password": "testpassword",
}


@pytest.mark.asyncio
async def test_register(client):
    resp = await client.post("/user/register", json=REGISTER_USER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_register_duplicate(client):
    # 이미 가입된 계정으로 재가입 시도
    await client.post("/user/register", json=REGISTER_USER)
    resp = await client.post("/user/register", json=REGISTER_USER)
    assert resp.status_code == 400
    assert "already exists" in resp.text or resp.json().get("message")


@pytest.mark.asyncio
async def test_user_me(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await client.get("/user/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == "testuser"
