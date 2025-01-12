def test_api_health_check(client):
    response = client.get("/api-health-check")
    assert response.status_code == 200
    assert response.json() == {
        "api_health_check": "api-server is Ok",
        "debug-mode": True,
    }


# Test for PostgreSQL Health Check
def test_postgresql_health_check(client):
    response = client.get("/postgresql-health-check")
    assert response.status_code == 200
    assert "postgresql_health_check" in response.json()


# Test for Redis Health Check
def test_redis_health_check(client, monkeypatch):
    response = client.get("/redis-health-check")
    assert response.status_code == 200
    assert response.json()["redis_health_check"] == "redis-server is Ok"


# Test for File Logging Test
def test_file_logging_test(client):
    response = client.get("/file-logging-test")
    assert response.status_code == 200
    assert response.json() == {"logging_check": "logging success"}
