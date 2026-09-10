from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, Task
from schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    employee_id: Optional[int] = Query(None, alias="employee_id"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Retrieve tasks. Managers/Admins can inspect team tasks; employees view their assigned tasks."""
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = db.query(Task)

    if user_role in ["admin", "manager"]:
        if employee_id is not None:
            query = query.filter(Task.admin_id == employee_id)
    else:
        query = query.filter(Task.admin_id == current_admin.id)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    return query.order_by(Task.created_at.desc()).all()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Create a new task. Managers/Admins can assign to any employee."""
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    target_admin_id = current_admin.id
    if payload.admin_id is not None and user_role in ["admin", "manager"]:
        target_admin_id = payload.admin_id

    task = Task(
        admin_id=target_admin_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=payload.status,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update task status, priority, title, description, or due date."""
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = db.query(Task).filter(Task.id == task_id)
    if user_role not in ["admin", "manager"]:
        query = query.filter(Task.admin_id == current_admin.id)

    task = query.first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.priority is not None:
        task.priority = payload.priority
    if payload.status is not None:
        task.status = payload.status
    if payload.due_date is not None:
        task.due_date = payload.due_date

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a task by ID."""
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = db.query(Task).filter(Task.id == task_id)
    if user_role not in ["admin", "manager"]:
        query = query.filter(Task.admin_id == current_admin.id)

    task = query.first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()
    return None
