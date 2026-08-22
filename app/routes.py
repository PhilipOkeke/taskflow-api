"""HTTP routes for the TaskFlow API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from app import crud
from app.database import get_session
from app.models import (
    TaskCreate,
    TaskList,
    TaskPriority,
    TaskPublic,
    TaskStatus,
    TaskUpdate,
)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
SessionDependency = Annotated[Session, Depends(get_session)]


def require_task(session: Session, task_id: int):
    """Return a task or raise a consistent 404 response."""

    task = crud.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate, session: SessionDependency):
    """Create a task."""

    return crud.create_task(session, task_input)


@router.get("", response_model=TaskList)
def read_tasks(
    session: SessionDependency,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    priority: TaskPriority | None = None,
    search: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """List tasks with optional filters, search, and pagination."""

    tasks, total = crud.list_tasks(
        session,
        status=task_status,
        priority=priority,
        search=search,
        limit=limit,
        offset=offset,
    )
    return TaskList(items=tasks, total=total, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(task_id: int, session: SessionDependency):
    """Return a task by ID."""

    return require_task(session, task_id)


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, task_input: TaskUpdate, session: SessionDependency):
    """Partially update a task."""

    task = require_task(session, task_id)
    update_data = task_input.model_dump(exclude_unset=True)
    for required_field in ("title", "status", "priority"):
        if required_field in update_data and update_data[required_field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{required_field} cannot be null",
            )
    return crud.update_task(session, task, task_input)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDependency) -> Response:
    """Delete a task."""

    task = require_task(session, task_id)
    crud.delete_task(session, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
