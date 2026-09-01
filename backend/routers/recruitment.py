from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin, hash_password
from database import get_db
from models import Admin, JobCandidate, JobPosting, OnboardingTask
from schemas import (
    CandidateStageUpdate,
    JobCandidateCreate,
    JobCandidateResponse,
    JobPostingCreate,
    JobPostingResponse,
    JobPostingUpdate,
)

router = APIRouter()


def _format_job_response(job: JobPosting) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "department": job.department,
        "job_type": job.job_type,
        "experience_level": job.experience_level,
        "salary_range": job.salary_range,
        "location": job.location,
        "status": job.status,
        "description": job.description,
        "requirements": job.requirements,
        "created_at": job.created_at,
        "candidates_count": len(job.candidates) if job.candidates else 0,
    }


def _format_candidate_response(c: JobCandidate) -> dict:
    job = c.job
    return {
        "id": c.id,
        "job_id": c.job_id,
        "full_name": c.full_name,
        "email": c.email,
        "phone": c.phone,
        "stage": c.stage,
        "resume_link": c.resume_link,
        "rating": c.rating,
        "notes": c.notes,
        "applied_date": c.applied_date,
        "created_at": c.created_at,
        "job_title": job.title if job else "General Requisition",
        "job_department": job.department if job else "General",
    }


# =========================================================
# Job Postings Endpoints
# =========================================================

@router.get("/jobs", response_model=List[JobPostingResponse])
def get_job_postings(
    department: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List all open job requisitions."""
    query = db.query(JobPosting)
    if department and department != "All":
        query = query.filter(JobPosting.department == department)
    if status_filter and status_filter != "All":
        query = query.filter(JobPosting.status == status_filter)

    jobs = query.order_by(JobPosting.created_at.desc()).all()
    return [_format_job_response(j) for j in jobs]


@router.post("/jobs", response_model=JobPostingResponse, status_code=status.HTTP_201_CREATED)
def create_job_posting(
    payload: JobPostingCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Create a new job posting."""
    job = JobPosting(
        title=payload.title,
        department=payload.department,
        job_type=payload.job_type,
        experience_level=payload.experience_level,
        salary_range=payload.salary_range,
        location=payload.location,
        status=payload.status,
        description=payload.description,
        requirements=payload.requirements,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return _format_job_response(job)


@router.patch("/jobs/{job_id}", response_model=JobPostingResponse)
def update_job_posting(
    job_id: int,
    payload: JobPostingUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update job posting details or status."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    for field, val in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, val)

    db.commit()
    db.refresh(job)
    return _format_job_response(job)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_posting(
    job_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a job posting."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    db.delete(job)
    db.commit()
    return None


# =========================================================
# Candidate Pipeline Endpoints
# =========================================================

@router.get("/candidates", response_model=List[JobCandidateResponse])
def get_candidates(
    job_id: Optional[int] = Query(None),
    stage: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List candidate applications with stage and job filtering."""
    query = db.query(JobCandidate)
    if job_id:
        query = query.filter(JobCandidate.job_id == job_id)
    if stage and stage != "All":
        query = query.filter(JobCandidate.stage == stage)

    candidates = query.order_by(JobCandidate.created_at.desc()).all()
    return [_format_candidate_response(c) for c in candidates]


@router.post("/candidates", response_model=JobCandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(
    payload: JobCandidateCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Register a new job candidate in the pipeline."""
    job = db.query(JobPosting).filter(JobPosting.id == payload.job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    candidate = JobCandidate(
        job_id=payload.job_id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        stage=payload.stage,
        resume_link=payload.resume_link,
        rating=payload.rating,
        notes=payload.notes,
        applied_date=payload.applied_date or date.today(),
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return _format_candidate_response(candidate)


@router.patch("/candidates/{candidate_id}/stage", response_model=JobCandidateResponse)
def update_candidate_stage(
    candidate_id: int,
    payload: CandidateStageUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Advance or change candidate pipeline stage."""
    candidate = db.query(JobCandidate).filter(JobCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found.")

    candidate.stage = payload.stage
    if payload.notes:
        candidate.notes = payload.notes

    db.commit()
    db.refresh(candidate)
    return _format_candidate_response(candidate)


@router.post("/candidates/{candidate_id}/convert-to-employee", status_code=status.HTTP_201_CREATED)
def convert_candidate_to_employee(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """
    1-Click Hire & Onboard: Converts a hired candidate into an active Employee profile
    and provisions onboarding tasks.
    """
    candidate = db.query(JobCandidate).filter(JobCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found.")

    existing_user = db.query(Admin).filter(Admin.email == candidate.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An employee with email '{candidate.email}' already exists.",
        )

    job = candidate.job
    job_title = job.title if job else "Software Engineer"
    department = job.department if job else "Engineering"

    # Create new Employee in admins table
    new_employee = Admin(
        full_name=candidate.full_name,
        email=candidate.email,
        password_hash=hash_password("Welcome2026!"),
        job_title=job_title,
        department=department,
        phone=candidate.phone or "+1 (555) 019-0000",
        leave_balance=20,
        is_active=True,
    )
    db.add(new_employee)
    db.flush()

    # Update candidate stage to hired
    candidate.stage = "hired"

    # Provision default onboarding checklist
    default_tasks = [
        "Sign Employment Agreement & Offer Letter",
        "Complete Direct Deposit & Tax Documents",
        "Set Up Work Laptop & 2FA Credentials",
        "Review Company Security & Code of Conduct",
        "Introductory 1-on-1 with Department Lead",
        "Team Welcome & Sprint Planning Alignment",
    ]
    for task_title in default_tasks:
        db.add(
            OnboardingTask(
                admin_id=new_employee.id,
                title=task_title,
                is_completed=False,
            )
        )

    db.commit()
    return {
        "success": True,
        "message": f"Candidate '{candidate.full_name}' successfully hired and converted to staff profile with onboarding tasks!",
        "employee_id": new_employee.id,
        "email": new_employee.email,
        "temp_password": "Welcome2026!",
    }


@router.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a candidate record."""
    candidate = db.query(JobCandidate).filter(JobCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found.")

    db.delete(candidate)
    db.commit()
    return None
