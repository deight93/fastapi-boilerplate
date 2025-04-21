from fastapi.testclient import TestClient

from app.core.setting import settings


def get_admin_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {"username": settings.ADMIN_ID, "password": settings.ADMIN_PASSWORD}
    response = client.post("/auth/login", data=login_data)
    tokens = response.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
