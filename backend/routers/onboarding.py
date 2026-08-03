from datetime import date, datetime, timezone
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, OnboardingTask


router = APIRouter()


# =========================================================
# Request and response schemas
# =========================================================

class OnboardingCreateRequest(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    due_date: Optional[date] = None


class OnboardingUpdateRequest(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    due_date: Optional[date] = None

    is_completed: Optional[bool] = None


class OnboardingStatusRequest(BaseModel):
    is_completed: bool


class OnboardingResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    admin_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class OnboardingSummaryResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    progress_percentage: float


class MessageResponse(BaseModel):
    message: str


# =========================================================
# Helper functions
# =========================================================

def utc_now() -> datetime:
    """Return the current UTC date and time."""

    return datetime.now(timezone.utc)


def get_task_or_404(
    database: Session,
    admin_id: int,
    task_id: int,
) -> OnboardingTask:
    """
    Return one onboarding task belonging to the
    currently logged-in Admin.
    """

    task = (
        database.query(OnboardingTask)
        .filter(
            OnboardingTask.id == task_id,
            OnboardingTask.admin_id == admin_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding task not found.",
        )

    return task


def update_completion_status(
    task: OnboardingTask,
    is_completed: bool,
) -> None:
    """
    Update the completion status and completion time.
    """

    task.is_completed = is_completed

    if is_completed:
        task.completed_at = utc_now()
    else:
        task.completed_at = None


# =========================================================
# Create onboarding task
# POST /api/onboarding
# =========================================================

@router.post(
    "",
    response_model=OnboardingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_onboarding_task(
    task_data: OnboardingCreateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Create a personal onboarding task.
    """

    duplicate_task = (
        database.query(OnboardingTask)
        .filter(
            OnboardingTask.admin_id
            == current_admin.id,
            OnboardingTask.title
            == task_data.title.strip(),
        )
        .first()
    )

    if duplicate_task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "An onboarding task with this title "
                "already exists."
            ),
        )

    task = OnboardingTask(
        admin_id=current_admin.id,
        title=task_data.title.strip(),
        description=(
            task_data.description.strip()
            if task_data.description
            else None
        ),
        due_date=task_data.due_date,
        is_completed=False,
        completed_at=None,
    )

    database.add(task)
    database.commit()
    database.refresh(task)

    return task


# =========================================================
# Create default onboarding tasks
# POST /api/onboarding/defaults
# =========================================================

@router.post(
    "/defaults",
    response_model=list[OnboardingResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_default_onboarding_tasks(
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Create several default onboarding tasks.

    Existing tasks with the same titles are not duplicated.
    """

    default_tasks = [
        {
            "title": "Complete personal profile",
            "description": (
                "Add your phone number, department, "
                "job title and other profile details."
            ),
        },
        {
            "title": "Read remote work policy",
            "description": (
                "Review the organization's remote "
                "working rules and responsibilities."
            ),
        },
        {
            "title": "Set up work environment",
            "description": (
                "Prepare the required software, tools "
                "and workplace access."
            ),
        },
        {
            "title": "Review attendance procedure",
            "description": (
                "Understand the clock-in and clock-out "
                "process."
            ),
        },
        {
            "title": "Create first quarterly OKR",
            "description": (
                "Add your first objective and measurable "
                "key result."
            ),
        },
    ]

    created_tasks = []

    for default_task in default_tasks:
        existing_task = (
            database.query(OnboardingTask)
            .filter(
                OnboardingTask.admin_id
                == current_admin.id,
                OnboardingTask.title
                == default_task["title"],
            )
            .first()
        )

        if existing_task:
            continue

        task = OnboardingTask(
            admin_id=current_admin.id,
            title=default_task["title"],
            description=default_task["description"],
            due_date=None,
            is_completed=False,
            completed_at=None,
        )

        database.add(task)
        created_tasks.append(task)

    database.commit()

    for task in created_tasks:
        database.refresh(task)

    return created_tasks


# =========================================================
# Get onboarding summary
# GET /api/onboarding/summary
# =========================================================

@router.get(
    "/summary",
    response_model=OnboardingSummaryResponse,
)
def get_onboarding_summary(
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return onboarding progress information.
    """

    tasks = (
        database.query(OnboardingTask)
        .filter(
            OnboardingTask.admin_id
            == current_admin.id
        )
        .all()
    )

    total_tasks = len(tasks)

    completed_tasks = sum(
        1
        for task in tasks
        if task.is_completed
    )

    pending_tasks = (
        total_tasks - completed_tasks
    )

    current_date = utc_now().date()

    overdue_tasks = sum(
        1
        for task in tasks
        if (
            not task.is_completed
            and task.due_date is not None
            and task.due_date < current_date
        )
    )

    progress_percentage = (
        round(
            completed_tasks / total_tasks * 100,
            2,
        )
        if total_tasks > 0
        else 0.0
    )

    return OnboardingSummaryResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        progress_percentage=progress_percentage,
    )


# =========================================================
# Get all onboarding tasks
# GET /api/onboarding
# =========================================================

@router.get(
    "",
    response_model=list[OnboardingResponse],
)
def get_onboarding_tasks(
    is_completed: Optional[bool] = Query(
        default=None,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return onboarding tasks belonging to the Admin.
    """

    query = (
        database.query(OnboardingTask)
        .filter(
            OnboardingTask.admin_id
            == current_admin.id
        )
    )

    if is_completed is not None:
        query = query.filter(
            OnboardingTask.is_completed
            == is_completed
        )

    tasks = (
        query
        .order_by(
            OnboardingTask.is_completed.asc(),
            OnboardingTask.due_date.asc(),
            OnboardingTask.id.asc(),
        )
        .limit(limit)
        .all()
    )

    return tasks


# =========================================================
# Get one onboarding task
# GET /api/onboarding/{task_id}
# =========================================================

@router.get(
    "/{task_id}",
    response_model=OnboardingResponse,
)
def get_onboarding_task(
    task_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return one onboarding task.
    """

    return get_task_or_404(
        database=database,
        admin_id=current_admin.id,
        task_id=task_id,
    )


# =========================================================
# Update onboarding task
# PATCH /api/onboarding/{task_id}
# =========================================================

@router.patch(
    "/{task_id}",
    response_model=OnboardingResponse,
)
def update_onboarding_task(
    task_id: int,
    task_data: OnboardingUpdateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Update the title, description, due date,
    or completion status of a task.
    """

    task = get_task_or_404(
        database=database,
        admin_id=current_admin.id,
        task_id=task_id,
    )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    if "title" in update_data:
        normalized_title = (
            update_data["title"].strip()
        )

        duplicate_task = (
            database.query(OnboardingTask)
            .filter(
                OnboardingTask.admin_id
                == current_admin.id,
                OnboardingTask.title
                == normalized_title,
                OnboardingTask.id != task_id,
            )
            .first()
        )

        if duplicate_task:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Another onboarding task already "
                    "uses this title."
                ),
            )

        update_data["title"] = normalized_title

    if (
        "description" in update_data
        and update_data["description"] is not None
    ):
        update_data["description"] = (
            update_data["description"].strip()
        )

    new_completion_status = (
        update_data.pop(
            "is_completed",
            None,
        )
    )

    for field_name, field_value in (
        update_data.items()
    ):
        setattr(
            task,
            field_name,
            field_value,
        )

    if new_completion_status is not None:
        update_completion_status(
            task=task,
            is_completed=new_completion_status,
        )

    database.commit()
    database.refresh(task)

    return task


# =========================================================
# Change completion status
# PATCH /api/onboarding/{task_id}/status
# =========================================================

@router.patch(
    "/{task_id}/status",
    response_model=OnboardingResponse,
)
def change_onboarding_status(
    task_id: int,
    status_data: OnboardingStatusRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Mark a task as completed or pending.
    """

    task = get_task_or_404(
        database=database,
        admin_id=current_admin.id,
        task_id=task_id,
    )

    update_completion_status(
        task=task,
        is_completed=status_data.is_completed,
    )

    database.commit()
    database.refresh(task)

    return task


# =========================================================
# Toggle completion status
# PATCH /api/onboarding/{task_id}/toggle
# =========================================================

@router.patch(
    "/{task_id}/toggle",
    response_model=OnboardingResponse,
)
def toggle_onboarding_task(
    task_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Toggle a task between completed and pending.
    """

    task = get_task_or_404(
        database=database,
        admin_id=current_admin.id,
        task_id=task_id,
    )

    update_completion_status(
        task=task,
        is_completed=not task.is_completed,
    )

    database.commit()
    database.refresh(task)

    return task


# =========================================================
# Delete onboarding task
# DELETE /api/onboarding/{task_id}
# =========================================================

@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
)
def delete_onboarding_task(
    task_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Delete one onboarding task.
    """

    task = get_task_or_404(
        database=database,
        admin_id=current_admin.id,
        task_id=task_id,
    )

    database.delete(task)
    database.commit()

    return MessageResponse(
        message="Onboarding task deleted successfully."
    )