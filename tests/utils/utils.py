import random
import string

from fastapi.testclient import TestClient

from app.core.setting import settings


async def random_lower_string(k) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


async def random_email() -> str:
    return f"{random_lower_string(32)}@{random_lower_string(32)}.com"


def get_admin_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {"username": settings.ADMIN_ID, "password": settings.ADMIN_PASSWORD}
    response = client.post("/auth/login", data=login_data)
    tokens = response.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
