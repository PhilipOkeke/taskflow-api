"""Shared test fixtures."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    """Create an isolated API client backed by a temporary SQLite database."""

    database_file = tmp_path / "test-taskflow.db"
    settings = Settings(database_url=f"sqlite:///{database_file}")
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def sample_task() -> dict[str, str]:
    """Return a valid task request payload."""

    return {
        "title": "Document the API",
        "description": "Add endpoint examples to the project README.",
        "status": "todo",
        "priority": "high",
    }
