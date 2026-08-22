"""End-to-end API tests for task operations."""


def create_task(client, payload):
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_and_read_task(client, sample_task):
    created = create_task(client, sample_task)

    assert created["id"] == 1
    assert created["title"] == sample_task["title"]
    assert created["priority"] == "high"
    assert created["created_at"]

    response = client.get(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_list_filter_search_and_pagination(client, sample_task):
    first = create_task(client, sample_task)
    second = create_task(
        client,
        {
            "title": "Build Docker image",
            "description": "Package the service for deployment.",
            "status": "in_progress",
            "priority": "medium",
        },
    )

    response = client.get("/api/v1/tasks", params={"status": "todo", "priority": "high"})
    body = response.json()

    assert response.status_code == 200
    assert body["total"] == 1
    assert body["items"][0]["id"] == first["id"]

    response = client.get("/api/v1/tasks", params={"search": "docker", "limit": 1})
    body = response.json()

    assert response.status_code == 200
    assert body["total"] == 1
    assert body["limit"] == 1
    assert body["items"][0]["id"] == second["id"]


def test_update_task(client, sample_task):
    created = create_task(client, sample_task)

    response = client.patch(
        f"/api/v1/tasks/{created['id']}",
        json={"status": "done", "priority": "low"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["priority"] == "low"
    assert response.json()["updated_at"] >= created["updated_at"]


def test_delete_task(client, sample_task):
    created = create_task(client, sample_task)

    response = client.delete(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/v1/tasks/{created['id']}").status_code == 404


def test_not_found_response(client):
    response = client.get("/api/v1/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_input_validation(client):
    response = client.post(
        "/api/v1/tasks",
        json={"title": "x", "status": "unknown", "priority": "urgent"},
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 3


def test_required_update_field_cannot_be_null(client, sample_task):
    created = create_task(client, sample_task)

    response = client.patch(f"/api/v1/tasks/{created['id']}", json={"title": None})

    assert response.status_code == 422
    assert response.json() == {"detail": "title cannot be null"}
