from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, CompanyEvent
from schemas import CompanyEventCreate, CompanyEventResponse

router = APIRouter()


@router.get("/events", response_model=List[CompanyEventResponse])
def get_calendar_events(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List company events and holidays."""
    return db.query(CompanyEvent).order_by(CompanyEvent.event_date.asc()).all()


@router.post("/events", response_model=CompanyEventResponse, status_code=status.HTTP_201_CREATED)
def create_calendar_event(
    payload: CompanyEventCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Add new company event or holiday."""
    event = CompanyEvent(
        title=payload.title,
        event_type=payload.event_type,
        event_date=payload.event_date,
        description=payload.description,
        location=payload.location,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calendar_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a calendar event."""
    event = db.query(CompanyEvent).filter(CompanyEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar event not found.",
        )

    db.delete(event)
    db.commit()
    return None
