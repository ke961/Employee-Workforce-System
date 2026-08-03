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
from models import Admin, Attendance


router = APIRouter()


# =========================================================
# Pydantic response schemas
# These are kept inside this file temporarily so that
# the one-user prototype can work independently.
# =========================================================

class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    admin_id: int
    attendance_date: date
    clock_in: datetime
    clock_out: Optional[datetime] = None
    total_work_minutes: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AttendanceStatusResponse(BaseModel):
    is_clocked_in: bool
    attendance_id: Optional[int] = None
    clock_in: Optional[datetime] = None
    message: str


class AttendanceSummaryResponse(BaseModel):
    total_records: int
    completed_records: int
    active_records: int
    total_work_minutes: int
    total_work_hours: float


class AttendanceNoteRequest(BaseModel):
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
    )


class MessageResponse(BaseModel):
    message: str


# =========================================================
# Helper functions
# =========================================================

def utc_now() -> datetime:
    """
    Return the current UTC date and time.
    """

    return datetime.now(timezone.utc)


def make_timezone_aware(value: datetime) -> datetime:
    """
    SQLite may return a datetime without timezone information.

    This function ensures that calculations use UTC.
    """

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def calculate_work_minutes(
    clock_in: datetime,
    clock_out: datetime,
) -> int:
    """
    Calculate total work duration in minutes.
    """

    start_time = make_timezone_aware(clock_in)
    end_time = make_timezone_aware(clock_out)

    if end_time < start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Clock-out time cannot be earlier than clock-in time.",
        )

    duration = end_time - start_time

    return max(
        0,
        int(duration.total_seconds() // 60),
    )


def get_active_attendance(
    database: Session,
    admin_id: int,
) -> Optional[Attendance]:
    """
    Return the currently active attendance record.
    """

    return (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == admin_id,
            Attendance.clock_out.is_(None),
        )
        .order_by(Attendance.id.desc())
        .first()
    )


# =========================================================
# Check current clock status
# GET /api/attendance/status
# =========================================================

@router.get(
    "/status",
    response_model=AttendanceStatusResponse,
)
def get_clock_status(
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Check whether the Admin is currently clocked in.
    """

    active_record = get_active_attendance(
        database=database,
        admin_id=current_admin.id,
    )

    if active_record is None:
        return AttendanceStatusResponse(
            is_clocked_in=False,
            attendance_id=None,
            clock_in=None,
            message="You are currently clocked out.",
        )

    return AttendanceStatusResponse(
        is_clocked_in=True,
        attendance_id=active_record.id,
        clock_in=active_record.clock_in,
        message="You are currently clocked in.",
    )


# =========================================================
# Clock in
# POST /api/attendance/clock-in
# =========================================================

@router.post(
    "/clock-in",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def clock_in(
    attendance_data: AttendanceNoteRequest,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Clock in the single Admin user using server time.
    """

    active_record = get_active_attendance(
        database=database,
        admin_id=current_admin.id,
    )

    if active_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already clocked in.",
        )

    current_time = utc_now()
    current_date = current_time.date()

    today_record = (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == current_admin.id,
            Attendance.attendance_date == current_date,
        )
        .first()
    )

    if today_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An attendance record already exists for today.",
        )

    attendance = Attendance(
        admin_id=current_admin.id,
        attendance_date=current_date,
        clock_in=current_time,
        clock_out=None,
        total_work_minutes=0,
        status="present",
        notes=attendance_data.notes,
    )

    database.add(attendance)
    database.commit()
    database.refresh(attendance)

    return attendance


# =========================================================
# Clock out
# PATCH /api/attendance/clock-out
# =========================================================

@router.patch(
    "/clock-out",
    response_model=AttendanceResponse,
)
def clock_out(
    attendance_data: AttendanceNoteRequest,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Clock out the Admin using the current server time.
    """

    attendance = get_active_attendance(
        database=database,
        admin_id=current_admin.id,
    )

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active clock-in record was found.",
        )

    current_time = utc_now()

    attendance.clock_out = current_time

    attendance.total_work_minutes = calculate_work_minutes(
        clock_in=attendance.clock_in,
        clock_out=current_time,
    )

    if attendance_data.notes:
        if attendance.notes:
            attendance.notes = (
                f"{attendance.notes}\n"
                f"Clock-out note: {attendance_data.notes}"
            )
        else:
            attendance.notes = attendance_data.notes

    database.commit()
    database.refresh(attendance)

    return attendance


# =========================================================
# Get today's attendance
# GET /api/attendance/today
# =========================================================

@router.get(
    "/today",
    response_model=Optional[AttendanceResponse],
)
def get_today_attendance(
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return today's attendance record.
    """

    current_date = utc_now().date()

    attendance = (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == current_admin.id,
            Attendance.attendance_date == current_date,
        )
        .first()
    )

    return attendance


# =========================================================
# Attendance summary
# GET /api/attendance/summary
# =========================================================

@router.get(
    "/summary",
    response_model=AttendanceSummaryResponse,
)
def get_attendance_summary(
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return the Admin's complete attendance summary.
    """

    records = (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == current_admin.id
        )
        .all()
    )

    total_work_minutes = sum(
        record.total_work_minutes
        for record in records
    )

    completed_records = sum(
        1
        for record in records
        if record.clock_out is not None
    )

    active_records = sum(
        1
        for record in records
        if record.clock_out is None
    )

    return AttendanceSummaryResponse(
        total_records=len(records),
        completed_records=completed_records,
        active_records=active_records,
        total_work_minutes=total_work_minutes,
        total_work_hours=round(
            total_work_minutes / 60,
            2,
        ),
    )


# =========================================================
# Get attendance history
# GET /api/attendance
# =========================================================

@router.get(
    "",
    response_model=list[AttendanceResponse],
)
def get_attendance_history(
    limit: int = Query(
        default=30,
        ge=1,
        le=365,
    ),
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return recent attendance history.
    """

    records = (
        database.query(Attendance)
        .filter(
            Attendance.admin_id == current_admin.id
        )
        .order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
        .limit(limit)
        .all()
    )

    return records


# =========================================================
# Get one attendance record
# GET /api/attendance/{attendance_id}
# =========================================================

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance_record(
    attendance_id: int,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return one attendance record belonging to the Admin.
    """

    attendance = (
        database.query(Attendance)
        .filter(
            Attendance.id == attendance_id,
            Attendance.admin_id == current_admin.id,
        )
        .first()
    )

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )

    return attendance


# =========================================================
# Delete attendance record
# DELETE /api/attendance/{attendance_id}
# =========================================================

@router.delete(
    "/{attendance_id}",
    response_model=MessageResponse,
)
def delete_attendance_record(
    attendance_id: int,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Delete one attendance record belonging to the Admin.
    """

    attendance = (
        database.query(Attendance)
        .filter(
            Attendance.id == attendance_id,
            Attendance.admin_id == current_admin.id,
        )
        .first()
    )

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )

    database.delete(attendance)
    database.commit()

    return MessageResponse(
        message="Attendance record deleted successfully.",
    )