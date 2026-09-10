from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin, require_manager_or_admin
from database import get_db
from models import Admin, ExpenseClaim
from schemas import (
    ExpenseClaimCreate,
    ExpenseClaimResponse,
    ExpenseClaimUpdate,
)

router = APIRouter()


@router.get("", response_model=List[ExpenseClaimResponse])
def get_expense_claims(
    status_filter: Optional[str] = Query(None, alias="status"),
    employee_id: Optional[int] = Query(None, alias="employee_id"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """
    Retrieve expense claims. Managers/Admins can view all team claims;
    employees view their own submissions.
    """
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = db.query(ExpenseClaim)

    if user_role in ["admin", "manager", "hr"]:
        if employee_id is not None:
            query = query.filter(ExpenseClaim.admin_id == employee_id)
    else:
        query = query.filter(ExpenseClaim.admin_id == current_admin.id)

    if status_filter:
        query = query.filter(ExpenseClaim.status == status_filter)

    return query.order_by(ExpenseClaim.created_at.desc()).all()


@router.post("", response_model=ExpenseClaimResponse, status_code=status.HTTP_201_CREATED)
def create_expense_claim(
    payload: ExpenseClaimCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Submit a new expense reimbursement claim."""
    claim = ExpenseClaim(
        admin_id=current_admin.id,
        category=payload.category,
        amount=payload.amount,
        merchant=payload.merchant,
        expense_date=payload.expense_date,
        description=payload.description,
        status="pending",
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


@router.patch("/{claim_id}/status", response_model=ExpenseClaimResponse)
def update_expense_status(
    claim_id: int,
    payload: ExpenseClaimUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_manager_or_admin),
):
    """
    Update status of an expense claim (approved, rejected).
    Requires Manager, HR, or Admin role.
    """
    claim = db.query(ExpenseClaim).filter(ExpenseClaim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense claim not found",
        )

    claim.status = payload.status
    db.commit()
    db.refresh(claim)
    return claim


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete an expense claim. Employees can cancel own claims; admins can delete any."""
    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = db.query(ExpenseClaim).filter(ExpenseClaim.id == claim_id)
    if user_role not in ["admin", "manager"]:
        query = query.filter(ExpenseClaim.admin_id == current_admin.id)

    claim = query.first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense claim not found",
        )

    db.delete(claim)
    db.commit()
    return None
