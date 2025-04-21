from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from tests.utils.utils import get_admin_token_headers


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def admin_token_headers(client: TestClient) -> dict[str, str]:
    return get_admin_token_headers(client)
