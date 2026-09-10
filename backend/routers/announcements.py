from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin, require_admin, require_manager_or_admin
from database import get_db
from models import Admin, Announcement
from schemas import AnnouncementCreate, AnnouncementResponse

router = APIRouter()


@router.get("", response_model=List[AnnouncementResponse])
def get_announcements(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Retrieve company announcements, sorted by pinned status and creation date."""
    query = db.query(Announcement)
    if category:
        query = query.filter(Announcement.category == category)
    
    return (
        query.order_by(
            Announcement.is_pinned.desc(),
            Announcement.created_at.desc(),
        ).all()
    )


@router.post("", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
def create_announcement(
    payload: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """Create a new company announcement (Requires Manager, HR, or Admin role)."""
    announcement = Announcement(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        is_pinned=payload.is_pinned,
        author=payload.author or current_admin.full_name or "HR Operations",
    )
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_admin),
):
    """Delete an announcement by ID (Requires Admin role)."""
    announcement = (
        db.query(Announcement)
        .filter(Announcement.id == announcement_id)
        .first()
    )
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found",
        )

    db.delete(announcement)
    db.commit()
    return None
