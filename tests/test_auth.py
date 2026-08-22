"""Authentication and authorization tests."""


def register(client, email, password="secure-password-123", full_name="Test User"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": full_name},
    )


def login(client, email, password="secure-password-123"):
    return client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )


def test_register_login_and_read_profile(unauthenticated_client):
    response = register(unauthenticated_client, "user@example.com")
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()

    response = login(unauthenticated_client, "user@example.com")
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]
    response = unauthenticated_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_duplicate_registration_is_rejected(unauthenticated_client):
    assert register(unauthenticated_client, "duplicate@example.com").status_code == 201
    response = register(unauthenticated_client, "DUPLICATE@example.com")

    assert response.status_code == 409
    assert response.json() == {"detail": "An account with this email already exists"}


def test_invalid_login_is_rejected(unauthenticated_client):
    register(unauthenticated_client, "user@example.com")
    response = login(unauthenticated_client, "user@example.com", "incorrect-password")

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_tasks_require_authentication(unauthenticated_client, sample_task):
    response = unauthenticated_client.post("/api/v1/tasks", json=sample_task)

    assert response.status_code == 401


def test_users_cannot_access_each_others_tasks(unauthenticated_client, sample_task):
    register(unauthenticated_client, "first@example.com")
    first_token = login(unauthenticated_client, "first@example.com").json()["access_token"]
    response = unauthenticated_client.post(
        "/api/v1/tasks",
        json=sample_task,
        headers={"Authorization": f"Bearer {first_token}"},
    )
    task_id = response.json()["id"]

    register(unauthenticated_client, "second@example.com")
    second_token = login(unauthenticated_client, "second@example.com").json()["access_token"]
    response = unauthenticated_client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {second_token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
