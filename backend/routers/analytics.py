import csv
import io
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from auth import get_current_admin
from database import get_db
from models import Admin, Attendance, ExpenseClaim, LeaveRequest, PerformanceReview, Task

router = APIRouter()


@router.get("/metrics")
def get_analytics_metrics(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Aggregate executive workforce metrics and distribution stats."""
    total_staff = db.query(Admin).count()
    active_staff = db.query(Admin).filter(Admin.is_active == True).count()

    total_attendance = db.query(Attendance).count()
    clocked_in_count = db.query(Attendance).filter(Attendance.clock_out == None).count()

    pending_leaves = db.query(LeaveRequest).filter(LeaveRequest.status == "pending").count()
    approved_leaves = db.query(LeaveRequest).filter(LeaveRequest.status == "approved").count()
    total_leaves = db.query(LeaveRequest).count()

    total_expenses = db.query(ExpenseClaim).count()
    total_expense_amount = db.query(func.sum(ExpenseClaim.amount)).scalar() or 0
    approved_expense_amount = (
        db.query(func.sum(ExpenseClaim.amount)).filter(ExpenseClaim.status == "approved").scalar() or 0
    )

    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()

    reviews = db.query(PerformanceReview).all()
    avg_rating = (sum(r.rating for r in reviews) / len(reviews)) if reviews else 4.8

    # Category breakdown for expenses
    expense_categories = (
        db.query(ExpenseClaim.category, func.sum(ExpenseClaim.amount))
        .group_by(ExpenseClaim.category)
        .all()
    )
    expense_breakdown = [
        {"category": cat or "General", "total": amount or 0} for cat, amount in expense_categories
    ]

    # Department breakdown for staff
    dept_counts = (
        db.query(Admin.department, func.count(Admin.id))
        .group_by(Admin.department)
        .all()
    )
    department_breakdown = [
        {"department": dept or "General", "count": count} for dept, count in dept_counts
    ]

    return {
        "summary": {
            "total_staff": total_staff,
            "active_staff": active_staff,
            "clocked_in_now": clocked_in_count,
            "total_attendance_shifts": total_attendance,
            "pending_leave_requests": pending_leaves,
            "approved_leave_requests": approved_leaves,
            "leave_utilization_rate": round((approved_leaves / (total_leaves or 1)) * 100, 1),
            "total_expenses_claimed": total_expense_amount,
            "approved_expenses_amount": approved_expense_amount,
            "task_completion_rate": round((completed_tasks / (total_tasks or 1)) * 100, 1),
            "average_performance_rating": round(avg_rating, 2),
        },
        "expense_breakdown": expense_breakdown,
        "department_breakdown": department_breakdown,
    }


@router.get("/export/attendance")
def export_attendance_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Export attendance records as CSV."""
    records = db.query(Attendance).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Shift ID", "Employee ID", "Attendance Date", "Clock In", "Clock Out", "Total Work Minutes", "Status"])

    for rec in records:
        writer.writerow([
            rec.id,
            rec.admin_id,
            str(rec.attendance_date),
            rec.clock_in.isoformat() if rec.clock_in else "",
            rec.clock_out.isoformat() if rec.clock_out else "",
            rec.total_work_minutes or 0,
            rec.status or "present",
        ])

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_report.csv"},
    )


@router.get("/export/leave")
def export_leave_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Export leave requests as CSV."""
    requests = db.query(LeaveRequest).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Request ID", "Employee ID", "Leave Type", "Start Date", "End Date", "Total Days", "Reason", "Status"])

    for req in requests:
        writer.writerow([
            req.id,
            req.admin_id,
            req.leave_type,
            str(req.start_date),
            str(req.end_date),
            req.total_days or 1,
            req.reason or "",
            req.status,
        ])

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leave_requests_report.csv"},
    )


@router.get("/export/expenses")
def export_expenses_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Export expense claims as CSV."""
    claims = db.query(ExpenseClaim).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Claim ID", "Employee ID", "Category", "Amount ($)", "Merchant", "Expense Date", "Description", "Status"])

    for cl in claims:
        writer.writerow([
            cl.id,
            cl.admin_id,
            cl.category,
            cl.amount,
            cl.merchant,
            str(cl.expense_date),
            cl.description or "",
            cl.status,
        ])

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expense_claims_report.csv"},
    )
