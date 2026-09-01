import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, EmployeeIdea, PulseSurvey, SurveyVote
from schemas import (
    EmployeeIdeaCreate,
    EmployeeIdeaResponse,
    IdeaStatusUpdate,
    PulseSurveyCreate,
    PulseSurveyResponse,
    SurveyVotePayload,
)

router = APIRouter()


def _format_survey_response(s: PulseSurvey, current_user_id: int) -> dict:
    try:
        options = json.loads(s.options_json)
    except Exception:
        options = []

    votes = s.votes or []
    total_votes = len(votes)

    breakdown = {opt: 0 for opt in options}
    user_voted_option = None

    for v in votes:
        if v.selected_option in breakdown:
            breakdown[v.selected_option] += 1
        if v.admin_id == current_user_id:
            user_voted_option = v.selected_option

    return {
        "id": s.id,
        "title": s.title,
        "question": s.question,
        "category": s.category,
        "options": options,
        "is_active": s.is_active,
        "created_at": s.created_at,
        "total_votes": total_votes,
        "vote_breakdown": breakdown,
        "user_voted_option": user_voted_option,
    }


# =========================================================
# Pulse Surveys Endpoints
# =========================================================

@router.get("", response_model=List[PulseSurveyResponse])
def get_pulse_surveys(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List all pulse surveys with aggregated vote statistics."""
    surveys = db.query(PulseSurvey).order_by(PulseSurvey.created_at.desc()).all()
    return [_format_survey_response(s, current_admin.id) for s in surveys]


@router.post("", response_model=PulseSurveyResponse, status_code=status.HTTP_201_CREATED)
def create_pulse_survey(
    payload: PulseSurveyCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Launch a new company pulse poll."""
    survey = PulseSurvey(
        title=payload.title,
        question=payload.question,
        category=payload.category,
        options_json=json.dumps(payload.options),
        is_active=True,
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return _format_survey_response(survey, current_admin.id)


@router.post("/{survey_id}/vote", response_model=PulseSurveyResponse)
def vote_on_survey(
    survey_id: int,
    payload: SurveyVotePayload,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Cast or update vote on a pulse survey."""
    survey = db.query(PulseSurvey).filter(PulseSurvey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pulse survey not found.")

    try:
        options = json.loads(survey.options_json)
    except Exception:
        options = []

    if payload.selected_option not in options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid option. Available options: {', '.join(options)}",
        )

    # Check if user already voted
    existing_vote = (
        db.query(SurveyVote)
        .filter(SurveyVote.survey_id == survey_id, SurveyVote.admin_id == current_admin.id)
        .first()
    )

    if existing_vote:
        existing_vote.selected_option = payload.selected_option
    else:
        vote = SurveyVote(
            survey_id=survey_id,
            admin_id=current_admin.id,
            selected_option=payload.selected_option,
        )
        db.add(vote)

    db.commit()
    db.refresh(survey)
    return _format_survey_response(survey, current_admin.id)


# =========================================================
# Employee Ideas & Suggestion Box Endpoints
# =========================================================

@router.get("/ideas", response_model=List[EmployeeIdeaResponse])
def get_ideas(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List employee innovation ideas ranked by upvotes."""
    ideas = db.query(EmployeeIdea).order_by(EmployeeIdea.upvotes_count.desc(), EmployeeIdea.created_at.desc()).all()
    return ideas


@router.post("/ideas", response_model=EmployeeIdeaResponse, status_code=status.HTTP_201_CREATED)
def submit_idea(
    payload: EmployeeIdeaCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Submit a new employee innovation or improvement idea."""
    idea = EmployeeIdea(
        admin_id=current_admin.id,
        author_name=current_admin.full_name,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        upvotes_count=1,
        status="under_review",
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea


@router.post("/ideas/{idea_id}/upvote", response_model=EmployeeIdeaResponse)
def upvote_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Upvote an idea."""
    idea = db.query(EmployeeIdea).filter(EmployeeIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found.")

    idea.upvotes_count += 1
    db.commit()
    db.refresh(idea)
    return idea


@router.patch("/ideas/{idea_id}/status", response_model=EmployeeIdeaResponse)
def update_idea_status(
    idea_id: int,
    payload: IdeaStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update review status of an idea."""
    idea = db.query(EmployeeIdea).filter(EmployeeIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found.")

    idea.status = payload.status
    db.commit()
    db.refresh(idea)
    return idea


@router.delete("/ideas/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete an idea."""
    idea = db.query(EmployeeIdea).filter(EmployeeIdea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found.")

    db.delete(idea)
    db.commit()
    return None
