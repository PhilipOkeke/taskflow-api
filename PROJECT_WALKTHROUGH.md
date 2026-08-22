# TaskFlow API Walkthrough

Read this guide before publishing the project or discussing it in an interview. You should be able to explain each design choice and make at least one personal improvement yourself.

## What the Project Demonstrates

TaskFlow is a CRUD API. CRUD means create, read, update, and delete. The project stores tasks in a relational SQLite database and exposes versioned HTTP endpoints for managing them.

## Request Flow

1. A client sends an HTTP request to FastAPI.
2. `app/routes.py` matches the request to an endpoint.
3. FastAPI validates path parameters, query parameters, and JSON data.
4. `get_session` creates a request-scoped database session.
5. The endpoint calls a function in `app/crud.py`.
6. SQLModel translates the database operation into SQL.
7. The endpoint returns a typed response that FastAPI converts to JSON.

## Files You Should Understand

### `app/main.py`

Creates the FastAPI application, initializes database tables during the application lifespan, includes the task router, and defines the root and health endpoints.

### `app/config.py`

Reads settings from environment variables. This lets the same code use different database URLs in local development, tests, Docker, and future deployments.

### `app/database.py`

Builds the SQLModel engine and gives every HTTP request its own session. The session is closed automatically after the request.

### `app/models.py`

Defines valid task statuses and priorities, the database table, request payloads, response payloads, and pagination response.

### `app/crud.py`

Contains database operations. Separating these functions from the HTTP routes makes the application easier to test and maintain.

### `app/routes.py`

Defines the public API. It handles HTTP status codes, validation, filtering, search, pagination, and not-found errors.

### `tests/`

Uses an isolated temporary SQLite database for every test. Tests exercise the API the same way a real client would.

## Interview Questions to Practise

1. Why did you choose FastAPI?
2. What is dependency injection, and how is it used here?
3. Why is there a separate model for creating, updating, storing, and returning tasks?
4. What happens when a client submits invalid data?
5. How do filtering and pagination work?
6. Why does each test use a temporary database?
7. What does the GitHub Actions workflow check?
8. How would you replace SQLite with PostgreSQL?
9. How would you add authentication and task ownership?
10. What would you monitor after deploying this API?

## Make It Personally Yours

Before applying for jobs, make at least one change and add tests for it. Good first improvements include:

- Add a `category` field to tasks.
- Add a `completed_at` timestamp when a task becomes done.
- Add sorting by due date or priority.
- Add an endpoint that returns task statistics.
- Add PostgreSQL and Alembic migrations.

Commit the improvement separately with a message such as `Add task category filtering`. This gives you a genuine change to explain during an interview.

