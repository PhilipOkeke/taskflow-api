"""Tests for service metadata and health endpoints."""


def test_service_info(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "TaskFlow API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
    }


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
