"""Database and API models for tasks."""

from datetime import UTC, datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return a timezone-naive UTC timestamp for SQLite compatibility."""

    return datetime.now(UTC).replace(tzinfo=None)


class TaskStatus(StrEnum):
    """Supported workflow states."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(StrEnum):
    """Supported task priorities."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    """Fields shared by task input and output models."""

    title: str = Field(min_length=3, max_length=120, index=True)
    description: str | None = Field(default=None, max_length=1_000)
    status: TaskStatus = Field(default=TaskStatus.TODO, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, index=True)
    due_date: datetime | None = None


class Task(TaskBase, table=True):
    """Persisted task record."""

    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)


class TaskCreate(TaskBase):
    """Payload accepted when creating a task."""


class TaskUpdate(SQLModel):
    """Payload accepted when partially updating a task."""

    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1_000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskPublic(TaskBase):
    """Task representation returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime


class TaskList(SQLModel):
    """Paginated task collection."""

    items: list[TaskPublic]
    total: int
    limit: int
    offset: int
