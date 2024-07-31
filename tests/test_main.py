def test_api_health_check(client):
    response = client.get("/api-health-check")
    assert response.status_code == 200
    assert response.json() == {
        "api_health_check": "api-server is Ok",
        "debug-mode": True,
    }
