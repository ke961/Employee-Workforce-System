from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import (
    Admin,
    Attendance,
    LeaveRequest,
    OnboardingTask,
    OKR,
)


router = APIRouter()


# =========================================================
# Dashboard response schemas
# =========================================================

class DashboardProfile(BaseModel):
    id: int
    full_name: str
    email: str
    job_title: str
    department: str
    leave_balance: int


class DashboardAttendance(BaseModel):
    is_clocked_in: bool
    attendance_id: Optional[int] = None
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    total_work_minutes: int = 0


class DashboardOnboarding(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    progress_percentage: float


class DashboardOKR(BaseModel):
    total_okrs: int
    not_started_okrs: int
    in_progress_okrs: int
    completed_okrs: int
    average_progress: float


class DashboardLeave(BaseModel):
    pending_requests: int
    approved_requests: int
    cancelled_requests: int
    available_leave_balance: int


class DashboardResponse(BaseModel):
    profile: DashboardProfile
    attendance: DashboardAttendance
    leave: DashboardLeave
    onboarding: DashboardOnboarding
    okrs: DashboardOKR


# =========================================================
# Helper function
# =========================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# =========================================================
# Get complete dashboard
# GET /api/dashboard
# =========================================================

@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return all information required for the single-user
    Admin dashboard.
    """

    current_date = utc_now().date()

    # -----------------------------------------------------
    # Today's attendance
    # -----------------------------------------------------

    today_attendance = (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == current_admin.id,
            Attendance.attendance_date == current_date,
        )
        .order_by(Attendance.id.desc())
        .first()
    )

    attendance_data = DashboardAttendance(
        is_clocked_in=(
            today_attendance is not None
            and today_attendance.clock_out is None
        ),
        attendance_id=(
            today_attendance.id
            if today_attendance
            else None
        ),
        clock_in=(
            today_attendance.clock_in
            if today_attendance
            else None
        ),
        clock_out=(
            today_attendance.clock_out
            if today_attendance
            else None
        ),
        total_work_minutes=(
            today_attendance.total_work_minutes
            if today_attendance
            else 0
        ),
    )

    # -----------------------------------------------------
    # Leave information
    # -----------------------------------------------------

    leave_requests = (
        database.query(LeaveRequest)
        .filter(
            LeaveRequest.admin_id == current_admin.id
        )
        .all()
    )

    leave_data = DashboardLeave(
        pending_requests=sum(
            1
            for request in leave_requests
            if request.status == "pending"
        ),
        approved_requests=sum(
            1
            for request in leave_requests
            if request.status == "approved"
        ),
        cancelled_requests=sum(
            1
            for request in leave_requests
            if request.status == "cancelled"
        ),
        available_leave_balance=current_admin.leave_balance,
    )

    # -----------------------------------------------------
    # Onboarding information
    # -----------------------------------------------------

    onboarding_tasks = (
        database.query(OnboardingTask)
        .filter(
            OnboardingTask.admin_id == current_admin.id
        )
        .all()
    )

    total_tasks = len(onboarding_tasks)

    completed_tasks = sum(
        1
        for task in onboarding_tasks
        if task.is_completed
    )

    pending_tasks = total_tasks - completed_tasks

    onboarding_progress = (
        round(
            completed_tasks / total_tasks * 100,
            2,
        )
        if total_tasks > 0
        else 0.0
    )

    onboarding_data = DashboardOnboarding(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress_percentage=onboarding_progress,
    )

    # -----------------------------------------------------
    # OKR information
    # -----------------------------------------------------

    okrs = (
        database.query(OKR)
        .filter(
            OKR.admin_id == current_admin.id
        )
        .all()
    )

    total_okrs = len(okrs)

    average_progress = (
        round(
            sum(okr.progress for okr in okrs)
            / total_okrs,
            2,
        )
        if total_okrs > 0
        else 0.0
    )

    okr_data = DashboardOKR(
        total_okrs=total_okrs,
        not_started_okrs=sum(
            1
            for okr in okrs
            if okr.status == "not_started"
        ),
        in_progress_okrs=sum(
            1
            for okr in okrs
            if okr.status == "in_progress"
        ),
        completed_okrs=sum(
            1
            for okr in okrs
            if okr.status == "completed"
        ),
        average_progress=average_progress,
    )

    # -----------------------------------------------------
    # Final dashboard response
    # -----------------------------------------------------

    return DashboardResponse(
        profile=DashboardProfile(
            id=current_admin.id,
            full_name=current_admin.full_name,
            email=current_admin.email,
            job_title=current_admin.job_title,
            department=current_admin.department,
            leave_balance=current_admin.leave_balance,
        ),
        attendance=attendance_data,
        leave=leave_data,
        onboarding=onboarding_data,
        okrs=okr_data,
    )