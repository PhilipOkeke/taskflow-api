# TaskFlow API

[![CI](https://github.com/philip-okeke/taskflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/philip-okeke/taskflow-api/actions/workflows/ci.yml)

A production-minded task management REST API built with Python, FastAPI, SQLModel, and SQLite. The project demonstrates backend development, database persistence, input validation, filtering, pagination, automated testing, containerization, and continuous integration.

## Why This Project

TaskFlow was created as a focused backend portfolio project. It shows how a small API can still use professional engineering practices: a clear project structure, typed models, request-scoped database sessions, consistent HTTP responses, automated quality checks, and documentation that lets another developer run the service quickly.

## Features

- Create, read, update, and delete tasks
- Track task status and priority
- Search task titles and descriptions
- Filter by status and priority
- Paginate task collections
- Validate request bodies and query parameters
- Persist data in SQLite through SQLModel
- Generate interactive OpenAPI documentation automatically
- Run API tests and coverage checks with PyTest
- Enforce linting and formatting with Ruff
- Build and run the service with Docker
- Test every push and pull request with GitHub Actions

## Technology Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.12 |
| API framework | FastAPI |
| Data validation | Pydantic through SQLModel |
| Database and ORM | SQLite and SQLModel/SQLAlchemy |
| Testing | PyTest, FastAPI TestClient, pytest-cov |
| Code quality | Ruff |
| Containerization | Docker and Docker Compose |
| CI/CD | GitHub Actions |

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service information |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/tasks` | Create a task |
| `GET` | `/api/v1/tasks` | List, filter, search, and paginate tasks |
| `GET` | `/api/v1/tasks/{task_id}` | Retrieve one task |
| `PATCH` | `/api/v1/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/api/v1/tasks/{task_id}` | Delete a task |

## Run Locally on Windows

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Then open:

- Interactive API documentation: <http://127.0.0.1:8000/docs>
- Alternative documentation: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/health>

If PowerShell blocks activation, run this once in the current PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run Locally on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Try the API

The easiest option is to open <http://127.0.0.1:8000/docs>, expand an endpoint, click **Try it out**, enter the request data, and click **Execute**.

Example request body for `POST /api/v1/tasks`:

```json
{
  "title": "Prepare portfolio project",
  "description": "Document and publish the TaskFlow API.",
  "status": "in_progress",
  "priority": "high"
}
```

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"Prepare portfolio project","status":"in_progress","priority":"high"}'
```

Filtering and pagination example:

```text
GET /api/v1/tasks?status=todo&priority=high&search=portfolio&limit=10&offset=0
```

## Run Automated Checks

```bash
ruff check .
ruff format --check .
pytest
```

The test configuration requires at least 90% application-code coverage.

## Run With Docker

```bash
docker compose up --build
```

The API will be available at <http://127.0.0.1:8000/docs>. Docker Compose stores the SQLite database in a named volume so the data survives container restarts.

## Project Structure

```text
taskflow-api/
├── .github/workflows/ci.yml   # Automated linting, formatting, and tests
├── app/
│   ├── config.py              # Environment-based configuration
│   ├── crud.py                # Database operations
│   ├── database.py            # Engine and session management
│   ├── main.py                # Application factory and service endpoints
│   ├── models.py              # Database and request/response models
│   └── routes.py              # Versioned task endpoints
├── tests/                     # End-to-end API tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Engineering Decisions

- **Application factory:** tests can create isolated application instances with temporary databases.
- **Request-scoped sessions:** every request receives its own database session, keeping transaction boundaries clear.
- **Separate API models:** create, update, database, and public response models have distinct responsibilities.
- **Partial updates:** `PATCH` changes only fields supplied by the client.
- **Versioned routes:** `/api/v1` leaves room for future API versions.
- **Automated quality gate:** CI rejects lint, formatting, test, or coverage failures.

## Possible Next Improvements

- PostgreSQL support and database migrations with Alembic
- User registration and JWT authentication
- Task ownership and role-based permissions
- Structured application logging
- Rate limiting and production monitoring
- Cloud deployment with a managed database

## Author

**Philip Okeke**  
[Engr.philipokeke@gmail.com](mailto:Engr.philipokeke@gmail.com)  
[LinkedIn](https://www.linkedin.com/in/philip-okeke-8148a42a4)

## License

This project is available under the MIT License.

