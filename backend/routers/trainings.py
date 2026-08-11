from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, TrainingCourse
from schemas import (
    TrainingCourseCreate,
    TrainingCourseResponse,
    TrainingCourseUpdate,
)

router = APIRouter()


@router.get("", response_model=List[TrainingCourseResponse])
def get_training_courses(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List assigned training courses."""
    return db.query(TrainingCourse).order_by(TrainingCourse.created_at.desc()).all()


@router.post("", response_model=TrainingCourseResponse, status_code=status.HTTP_201_CREATED)
def create_training_course(
    payload: TrainingCourseCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Assign training course to employee."""
    target_emp = db.query(Admin).filter(Admin.id == payload.admin_id).first()
    if not target_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    course = TrainingCourse(
        title=payload.title,
        category=payload.category,
        description=payload.description,
        duration_hours=payload.duration_hours,
        due_date=payload.due_date,
        admin_id=payload.admin_id,
        status="assigned",
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.patch("/{course_id}/status", response_model=TrainingCourseResponse)
def update_training_status(
    course_id: int,
    payload: TrainingCourseUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update training course completion status."""
    course = db.query(TrainingCourse).filter(TrainingCourse.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training course assignment not found.",
        )

    course.status = payload.status
    if payload.status == "completed":
        course.completed_at = datetime.now(timezone.utc)
    else:
        course.completed_at = None

    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a training course assignment."""
    course = db.query(TrainingCourse).filter(TrainingCourse.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training course assignment not found.",
        )

    db.delete(course)
    db.commit()
    return None
