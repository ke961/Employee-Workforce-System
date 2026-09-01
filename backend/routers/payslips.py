from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, Payslip
from schemas import PayslipCreate, PayslipResponse, PayslipStatusUpdate

router = APIRouter()


def _format_payslip_response(p: Payslip, admin: Optional[Admin] = None) -> dict:
    emp = admin or p.admin
    return {
        "id": p.id,
        "admin_id": p.admin_id,
        "month": p.month,
        "year": p.year,
        "basic_salary": p.basic_salary,
        "allowances": p.allowances,
        "bonus": p.bonus,
        "tax_deduction": p.tax_deduction,
        "insurance_deduction": p.insurance_deduction,
        "provident_fund_deduction": p.provident_fund_deduction,
        "net_salary": p.net_salary,
        "payment_status": p.payment_status,
        "payment_date": p.payment_date,
        "payment_method": p.payment_method,
        "notes": p.notes,
        "created_at": p.created_at,
        "employee_name": emp.full_name if emp else "Unknown Staff",
        "employee_email": emp.email if emp else "",
        "employee_job_title": emp.job_title if emp else "Employee",
        "employee_department": emp.department if emp else "General",
    }


@router.get("", response_model=List[PayslipResponse])
def get_payslips(
    employee_id: Optional[int] = Query(None, alias="admin_id"),
    month: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List employee payslips with optional filtering."""
    query = db.query(Payslip)
    if employee_id:
        query = query.filter(Payslip.admin_id == employee_id)
    if month and month != "All":
        query = query.filter(Payslip.month == month)
    if year:
        query = query.filter(Payslip.year == year)
    if status_filter and status_filter != "All":
        query = query.filter(Payslip.payment_status == status_filter)

    payslips = query.order_by(Payslip.year.desc(), Payslip.created_at.desc()).all()
    return [_format_payslip_response(p) for p in payslips]


@router.get("/{payslip_id}", response_model=PayslipResponse)
def get_payslip_detail(
    payslip_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Get single payslip details."""
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip not found.",
        )
    return _format_payslip_response(payslip)


@router.post("", response_model=PayslipResponse, status_code=status.HTTP_201_CREATED)
def issue_payslip(
    payload: PayslipCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Generate and issue a new monthly payslip for an employee."""
    emp = db.query(Admin).filter(Admin.id == payload.admin_id).first()
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target employee not found.",
        )

    # Auto-calculate net pay
    total_earnings = payload.basic_salary + payload.allowances + payload.bonus
    total_deductions = payload.tax_deduction + payload.insurance_deduction + payload.provident_fund_deduction
    net_salary = round(max(0.0, total_earnings - total_deductions), 2)

    payment_date = payload.payment_date
    if payload.payment_status == "paid" and not payment_date:
        payment_date = date.today()

    payslip = Payslip(
        admin_id=payload.admin_id,
        month=payload.month,
        year=payload.year,
        basic_salary=payload.basic_salary,
        allowances=payload.allowances,
        bonus=payload.bonus,
        tax_deduction=payload.tax_deduction,
        insurance_deduction=payload.insurance_deduction,
        provident_fund_deduction=payload.provident_fund_deduction,
        net_salary=net_salary,
        payment_status=payload.payment_status,
        payment_date=payment_date,
        payment_method=payload.payment_method,
        notes=payload.notes,
    )

    db.add(payslip)
    db.commit()
    db.refresh(payslip)
    return _format_payslip_response(payslip, emp)


@router.patch("/{payslip_id}/status", response_model=PayslipResponse)
def update_payslip_status(
    payslip_id: int,
    payload: PayslipStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Mark a payslip as Paid or Pending."""
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip not found.",
        )

    payslip.payment_status = payload.payment_status
    if payload.payment_status == "paid":
        payslip.payment_date = payload.payment_date or date.today()
    else:
        payslip.payment_date = None

    db.commit()
    db.refresh(payslip)
    return _format_payslip_response(payslip)


@router.delete("/{payslip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payslip(
    payslip_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a payslip record."""
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip not found.",
        )

    db.delete(payslip)
    db.commit()
    return None
