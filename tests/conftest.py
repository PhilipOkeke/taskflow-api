"""Shared test fixtures."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def unauthenticated_client(tmp_path) -> Generator[TestClient, None, None]:
    """Create an isolated API client backed by a temporary SQLite database."""

    database_file = tmp_path / "test-taskflow.db"
    settings = Settings(
        database_url=f"sqlite:///{database_file}",
        secret_key="test-secret-key-that-is-not-used-in-production",
    )
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def client(unauthenticated_client) -> TestClient:
    """Return a client authenticated as the default test user."""

    registration = {
        "email": "philip@example.com",
        "full_name": "Philip Okeke",
        "password": "secure-password-123",
    }
    response = unauthenticated_client.post("/api/v1/auth/register", json=registration)
    assert response.status_code == 201

    response = unauthenticated_client.post(
        "/api/v1/auth/token",
        data={"username": registration["email"], "password": registration["password"]},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    unauthenticated_client.headers.update({"Authorization": f"Bearer {token}"})
    return unauthenticated_client


@pytest.fixture
def sample_task() -> dict[str, str]:
    """Return a valid task request payload."""

    return {
        "title": "Document the API",
        "description": "Add endpoint examples to the project README.",
        "status": "todo",
        "priority": "high",
    }
