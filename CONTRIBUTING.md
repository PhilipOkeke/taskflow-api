# Contributing to TaskFlow API

Thank you for considering a contribution. This guide keeps changes easy to review and ensures the API remains reliable.

## Development setup

1. Fork and clone the repository.
2. Create and activate a virtual environment.
3. Install the project and development tools:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

4. Run the service:

```bash
uvicorn app.main:app --reload
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Quality checks

Run every check before opening a pull request:

```bash
ruff check .
ruff format --check .
pytest
```

The test suite enforces at least 90% coverage for application code.

## Making a change

- Create a focused branch such as `feature/task-labels` or `fix/pagination-limit`.
- Keep each commit limited to one logical change.
- Add or update tests whenever behaviour changes.
- Preserve versioned routes and consistent error responses.
- Update the README or API examples when public behaviour changes.
- Never commit secrets, local databases, virtual environments, or generated reports.

## Commit messages

Use short, action-oriented messages:

- `Add task due-date validation`
- `Fix priority filtering for mixed-case input`
- `Document Docker development workflow`

## Pull requests

A pull request should include:

- A concise explanation of the problem and solution
- The tests added or updated
- Any API or database compatibility considerations
- Confirmation that linting, formatting, tests, and coverage pass

Small, well-tested pull requests are easier to review and merge.
