from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin, require_manager_or_admin
from database import get_db
from models import Admin, ShiftSchedule
from schemas import ShiftScheduleCreate, ShiftScheduleResponse

router = APIRouter()


@router.get("", response_model=List[ShiftScheduleResponse])
def get_shift_schedules(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List assigned work shift schedules."""
    return db.query(ShiftSchedule).order_by(ShiftSchedule.created_at.desc()).all()


@router.post("", response_model=ShiftScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_shift_schedule(
    payload: ShiftScheduleCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """Assign work shift schedule to employee (Requires Manager or Admin role)."""
    target_emp = db.query(Admin).filter(Admin.id == payload.admin_id).first()
    if not target_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    shift = ShiftSchedule(
        admin_id=payload.admin_id,
        shift_name=payload.shift_name,
        shift_type=payload.shift_type,
        start_time=payload.start_time,
        end_time=payload.end_time,
        work_days=payload.work_days,
        location=payload.location,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_schedule(
    shift_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """Delete a shift schedule assignment (Requires Manager or Admin role)."""
    shift = db.query(ShiftSchedule).filter(ShiftSchedule.id == shift_id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift schedule not found.",
        )

    db.delete(shift)
    db.commit()
    return None
