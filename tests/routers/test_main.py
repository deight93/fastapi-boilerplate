import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_api_health_check(client):
    response = await client.get("/api-health-check")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "api_health_check": "api-server is Ok",
        "debug-mode": True,
    }


@pytest.mark.asyncio
async def test_file_logging_test(client):
    response = await client.get("/file-logging-test")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {"logging_check": "logging success"}
