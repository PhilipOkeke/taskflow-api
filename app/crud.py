"""Task persistence operations."""

from sqlalchemy import func, or_
from sqlmodel import Session, select

from app.models import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate, utc_now


def create_task(session: Session, task_input: TaskCreate) -> Task:
    """Persist and return a new task."""

    task = Task.model_validate(task_input)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(
    session: Session,
    *,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    search: str | None,
    limit: int,
    offset: int,
) -> tuple[list[Task], int]:
    """Return filtered, paginated tasks and the full match count."""

    conditions = []
    if status is not None:
        conditions.append(Task.status == status)
    if priority is not None:
        conditions.append(Task.priority == priority)
    if search:
        pattern = f"%{search.strip()}%"
        conditions.append(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))

    task_statement = select(Task)
    count_statement = select(func.count()).select_from(Task)
    for condition in conditions:
        task_statement = task_statement.where(condition)
        count_statement = count_statement.where(condition)

    task_statement = task_statement.order_by(Task.created_at.desc()).offset(offset).limit(limit)
    tasks = list(session.exec(task_statement).all())
    total = session.exec(count_statement).one()
    return tasks, total


def get_task(session: Session, task_id: int) -> Task | None:
    """Return a task by ID when it exists."""

    return session.get(Task, task_id)


def update_task(session: Session, task: Task, task_input: TaskUpdate) -> Task:
    """Apply a partial update and return the refreshed task."""

    update_data = task_input.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    task.updated_at = utc_now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    """Delete an existing task."""

    session.delete(task)
    session.commit()
