from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin, require_admin, require_manager_or_admin
from database import get_db
from models import Admin, Kudos, PerformanceReview
from schemas import (
    KudosCreate,
    KudosResponse,
    PerformanceReviewCreate,
    PerformanceReviewResponse,
    PerformanceReviewUpdate,
)

router = APIRouter()


# =========================================================
# Performance Reviews
# =========================================================

@router.get("/performance", response_model=List[PerformanceReviewResponse])
def get_performance_reviews(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """
    List performance reviews.
    Managers/Admins can see all reviews; employees only see reviews
    where they are the subject or the reviewer.
    """
    query = db.query(PerformanceReview)
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    
    if user_role not in ["admin", "manager", "hr"]:
        query = query.filter(
            (PerformanceReview.employee_id == current_admin.id)
            | (PerformanceReview.reviewer_id == current_admin.id)
        )

    return query.order_by(PerformanceReview.created_at.desc()).all()


@router.post("/performance", response_model=PerformanceReviewResponse, status_code=status.HTTP_201_CREATED)
def create_performance_review(
    payload: PerformanceReviewCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """Create a new performance review (Requires Manager, HR, or Admin role)."""
    target_emp = db.query(Admin).filter(Admin.id == payload.employee_id).first()
    if not target_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target employee not found.",
        )

    review = PerformanceReview(
        reviewer_id=current_admin.id,
        employee_id=payload.employee_id,
        review_cycle=payload.review_cycle,
        rating=payload.rating,
        strengths=payload.strengths,
        growth_areas=payload.growth_areas,
        status=payload.status,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.patch("/performance/{review_id}", response_model=PerformanceReviewResponse)
def update_performance_review(
    review_id: int,
    payload: PerformanceReviewUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """Update an existing performance review (Requires Manager, HR, or Admin role)."""
    review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance review not found.",
        )

    if payload.review_cycle is not None:
        review.review_cycle = payload.review_cycle
    if payload.rating is not None:
        review.rating = payload.rating
    if payload.strengths is not None:
        review.strengths = payload.strengths
    if payload.growth_areas is not None:
        review.growth_areas = payload.growth_areas
    if payload.status is not None:
        review.status = payload.status

    db.commit()
    db.refresh(review)
    return review


@router.delete("/performance/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_performance_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_admin),
):
    """Delete a performance review (Requires Admin role)."""
    review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance review not found.",
        )

    db.delete(review)
    db.commit()
    return None


# =========================================================
# Peer Recognition & Kudos Feed
# =========================================================

@router.get("/kudos", response_model=List[KudosResponse])
def get_kudos(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List peer recognition shoutouts."""
    return db.query(Kudos).order_by(Kudos.created_at.desc()).all()


@router.post("/kudos", response_model=KudosResponse, status_code=status.HTTP_201_CREATED)
def create_kudos(
    payload: KudosCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Post a peer recognition shoutout."""
    kudos = Kudos(
        sender_name=current_admin.full_name,
        receiver_name=payload.receiver_name,
        category=payload.category,
        message=payload.message,
    )
    db.add(kudos)
    db.commit()
    db.refresh(kudos)
    return kudos
