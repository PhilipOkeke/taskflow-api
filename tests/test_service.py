"""Tests for service metadata and health endpoints."""


def test_service_info(unauthenticated_client):
    response = unauthenticated_client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "TaskFlow API",
        "version": "2.0.0",
        "documentation": "/docs",
        "health": "/health",
    }


def test_health_check(unauthenticated_client):
    response = unauthenticated_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
