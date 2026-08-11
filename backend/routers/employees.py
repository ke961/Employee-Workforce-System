from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin, hash_password
from database import get_db
from models import Admin
from schemas import AdminCreate, AdminUpdate

router = APIRouter()


@router.get("")
def list_employees(
    search: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Retrieve all staff members with optional search and department filtering."""
    query = db.query(Admin)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            (Admin.full_name.ilike(term)) | (Admin.email.ilike(term)) | (Admin.job_title.ilike(term))
        )
    
    if department and department != "All":
        query = query.filter(Admin.department == department)

    employees = query.order_by(Admin.full_name.asc()).all()

    return [
        {
            "id": emp.id,
            "full_name": emp.full_name,
            "email": emp.email,
            "job_title": emp.job_title or "Team Member",
            "department": emp.department or "General",
            "phone": emp.phone or "N/A",
            "leave_balance": emp.leave_balance,
            "is_active": emp.is_active,
            "created_at": emp.created_at,
        }
        for emp in employees
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: AdminCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Create a new staff member profile."""
    existing = db.query(Admin).filter(Admin.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An employee account with this email address already exists.",
        )

    new_emp = Admin(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        job_title=payload.job_title,
        department=payload.department,
        phone=payload.phone,
        leave_balance=payload.leave_balance,
        is_active=True,
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {
        "id": new_emp.id,
        "full_name": new_emp.full_name,
        "email": new_emp.email,
        "job_title": new_emp.job_title,
        "department": new_emp.department,
        "leave_balance": new_emp.leave_balance,
        "is_active": new_emp.is_active,
    }


@router.patch("/{employee_id}")
def update_employee(
    employee_id: int,
    payload: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update employee profile details."""
    emp = db.query(Admin).filter(Admin.id == employee_id).first()
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    if payload.full_name is not None:
        emp.full_name = payload.full_name
    if payload.email is not None:
        emp.email = payload.email
    if payload.job_title is not None:
        emp.job_title = payload.job_title
    if payload.department is not None:
        emp.department = payload.department
    if payload.phone is not None:
        emp.phone = payload.phone
    if payload.leave_balance is not None:
        emp.leave_balance = payload.leave_balance
    if payload.is_active is not None:
        emp.is_active = payload.is_active

    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete employee profile."""
    if employee_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own logged-in account.",
        )

    emp = db.query(Admin).filter(Admin.id == employee_id).first()
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    db.delete(emp)
    db.commit()
    return None
