from datetime import date, datetime
from typing import Literal, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from sqlalchemy.orm import Session

from auth import get_current_admin, require_manager_or_admin
from database import get_db
from models import Admin, LeaveRequest


router = APIRouter()


# =========================================================
# Request and response schemas
# =========================================================

class LeaveCreateRequest(BaseModel):
    leave_type: str = Field(
        min_length=2,
        max_length=50,
    )

    start_date: date
    end_date: date

    reason: str = Field(
        min_length=3,
        max_length=1000,
    )

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "End date cannot be earlier than start date."
            )

        return self


class LeaveUpdateRequest(BaseModel):
    leave_type: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    reason: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=1000,
    )


class LeaveStatusRequest(BaseModel):
    status: Literal[
        "pending",
        "approved",
        "cancelled",
    ]


class LeaveResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    admin_id: int
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    reason: str
    status: str
    created_at: datetime
    updated_at: datetime


class LeaveSummaryResponse(BaseModel):
    total_requests: int
    pending_requests: int
    approved_requests: int
    cancelled_requests: int
    approved_leave_days: int
    available_leave_balance: int


class MessageResponse(BaseModel):
    message: str


# =========================================================
# Helper functions
# =========================================================

def calculate_leave_days(
    start_date: date,
    end_date: date,
) -> int:
    """
    Calculate inclusive leave duration.

    Example:
    10 August to 12 August = 3 days.
    """

    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "End date cannot be earlier than "
                "start date."
            ),
        )

    return (end_date - start_date).days + 1


def get_leave_or_404(
    database: Session,
    admin_id: int,
    leave_id: int,
) -> LeaveRequest:
    """
    Return one leave request belonging to the
    currently logged-in Admin.
    """

    leave_request = (
        database.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_id,
            LeaveRequest.admin_id == admin_id,
        )
        .first()
    )

    if leave_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found.",
        )

    return leave_request


def update_leave_balance(
    admin: Admin,
    previous_status: str,
    new_status: str,
    total_days: int,
) -> None:
    """
    Adjust leave balance when a request becomes
    approved or when an approved request is changed.
    """

    if (
        previous_status != "approved"
        and new_status == "approved"
    ):
        if admin.leave_balance < total_days:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "You do not have enough leave balance "
                    "to approve this request."
                ),
            )

        admin.leave_balance -= total_days

    elif (
        previous_status == "approved"
        and new_status != "approved"
    ):
        admin.leave_balance += total_days


# =========================================================
# Create leave request
# POST /api/leave
# =========================================================

@router.post(
    "",
    response_model=LeaveResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    leave_data: LeaveCreateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Submit a new personal leave request.
    """

    total_days = calculate_leave_days(
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
    )

    overlapping_request = (
        database.query(LeaveRequest)
        .filter(
            LeaveRequest.admin_id
            == current_admin.id,
            LeaveRequest.status.in_(
                ["pending", "approved"]
            ),
            LeaveRequest.start_date
            <= leave_data.end_date,
            LeaveRequest.end_date
            >= leave_data.start_date,
        )
        .first()
    )

    if overlapping_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Another pending or approved leave request "
                "already covers these dates."
            ),
        )

    leave_request = LeaveRequest(
        admin_id=current_admin.id,
        leave_type=leave_data.leave_type.strip(),
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        total_days=total_days,
        reason=leave_data.reason.strip(),
        status="pending",
    )

    database.add(leave_request)
    database.commit()
    database.refresh(leave_request)

    return leave_request


# =========================================================
# Leave summary
# GET /api/leave/summary
# =========================================================

@router.get(
    "/summary",
    response_model=LeaveSummaryResponse,
)
def get_leave_summary(
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return leave statistics for the Admin.
    """

    requests = (
        database.query(LeaveRequest)
        .filter(
            LeaveRequest.admin_id
            == current_admin.id
        )
        .all()
    )

    approved_leave_days = sum(
        request.total_days
        for request in requests
        if request.status == "approved"
    )

    return LeaveSummaryResponse(
        total_requests=len(requests),
        pending_requests=sum(
            1
            for request in requests
            if request.status == "pending"
        ),
        approved_requests=sum(
            1
            for request in requests
            if request.status == "approved"
        ),
        cancelled_requests=sum(
            1
            for request in requests
            if request.status == "cancelled"
        ),
        approved_leave_days=approved_leave_days,
        available_leave_balance=(
            current_admin.leave_balance
        ),
    )


# =========================================================
# Get all leave requests
# GET /api/leave
# =========================================================

@router.get(
    "",
    response_model=list[LeaveResponse],
)
def get_leave_requests(
    leave_status: Optional[str] = Query(
        default=None,
        alias="status",
    ),
    employee_id: Optional[int] = Query(
        default=None,
        alias="employee_id",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return leave request history. Managers/Admins can view team submissions;
    employees view their own submissions.
    """

    user_role = (getattr(current_admin, "role", "employee") or "employee").lower()
    query = database.query(LeaveRequest)

    if user_role in ["admin", "manager", "hr"]:
        if employee_id is not None:
            query = query.filter(LeaveRequest.admin_id == employee_id)
    else:
        query = query.filter(LeaveRequest.admin_id == current_admin.id)

    if leave_status is not None:
        allowed_statuses = {
            "pending",
            "approved",
            "cancelled",
        }

        if leave_status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid leave status.",
            )

        query = query.filter(
            LeaveRequest.status == leave_status
        )

    requests = (
        query
        .order_by(
            LeaveRequest.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return requests


# =========================================================
# Get one leave request
# GET /api/leave/{leave_id}
# =========================================================

@router.get(
    "/{leave_id}",
    response_model=LeaveResponse,
)
def get_leave_request(
    leave_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return one personal leave request.
    """

    return get_leave_or_404(
        database=database,
        admin_id=current_admin.id,
        leave_id=leave_id,
    )


# =========================================================
# Update pending leave request
# PATCH /api/leave/{leave_id}
# =========================================================

@router.patch(
    "/{leave_id}",
    response_model=LeaveResponse,
)
def update_leave_request(
    leave_id: int,
    leave_data: LeaveUpdateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Update a pending leave request.
    """

    leave_request = get_leave_or_404(
        database=database,
        admin_id=current_admin.id,
        leave_id=leave_id,
    )

    if leave_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Only pending leave requests "
                "can be edited."
            ),
        )

    update_data = leave_data.model_dump(
        exclude_unset=True
    )

    updated_start_date = update_data.get(
        "start_date",
        leave_request.start_date,
    )

    updated_end_date = update_data.get(
        "end_date",
        leave_request.end_date,
    )

    total_days = calculate_leave_days(
        start_date=updated_start_date,
        end_date=updated_end_date,
    )

    overlapping_request = (
        database.query(LeaveRequest)
        .filter(
            LeaveRequest.admin_id
            == current_admin.id,
            LeaveRequest.id != leave_id,
            LeaveRequest.status.in_(
                ["pending", "approved"]
            ),
            LeaveRequest.start_date
            <= updated_end_date,
            LeaveRequest.end_date
            >= updated_start_date,
        )
        .first()
    )

    if overlapping_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Another leave request already "
                "covers these dates."
            ),
        )

    for field_name, field_value in (
        update_data.items()
    ):
        if (
            isinstance(field_value, str)
            and field_value is not None
        ):
            field_value = field_value.strip()

        setattr(
            leave_request,
            field_name,
            field_value,
        )

    leave_request.total_days = total_days

    database.commit()
    database.refresh(leave_request)

    return leave_request


# =========================================================
# Change leave status
# PATCH /api/leave/{leave_id}/status
# =========================================================

@router.patch(
    "/{leave_id}/status",
    response_model=LeaveResponse,
)
def update_leave_status(
    leave_id: int,
    status_data: LeaveStatusRequest,
    current_admin: Admin = Depends(
        require_manager_or_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Approve, return to pending, or cancel a request.
    Requires Manager, HR, or Admin role.
    """

    leave_request = (
        database.query(LeaveRequest)
        .filter(LeaveRequest.id == leave_id)
        .first()
    )
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request was not found.",
        )

    target_admin = (
        database.query(Admin)
        .filter(Admin.id == leave_request.admin_id)
        .first()
    ) or current_admin

    previous_status = leave_request.status
    new_status = status_data.status

    if previous_status == new_status:
        return leave_request

    update_leave_balance(
        admin=target_admin,
        previous_status=previous_status,
        new_status=new_status,
        total_days=leave_request.total_days,
    )

    leave_request.status = new_status

    database.commit()
    database.refresh(leave_request)

    return leave_request


# =========================================================
# Cancel leave request
# PATCH /api/leave/{leave_id}/cancel
# =========================================================

@router.patch(
    "/{leave_id}/cancel",
    response_model=LeaveResponse,
)
def cancel_leave_request(
    leave_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Cancel a pending or approved leave request.
    """

    leave_request = get_leave_or_404(
        database=database,
        admin_id=current_admin.id,
        leave_id=leave_id,
    )

    if leave_request.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This leave request has already "
                "been cancelled."
            ),
        )

    update_leave_balance(
        admin=current_admin,
        previous_status=leave_request.status,
        new_status="cancelled",
        total_days=leave_request.total_days,
    )

    leave_request.status = "cancelled"

    database.commit()
    database.refresh(leave_request)

    return leave_request


# =========================================================
# Delete leave request
# DELETE /api/leave/{leave_id}
# =========================================================

@router.delete(
    "/{leave_id}",
    response_model=MessageResponse,
)
def delete_leave_request(
    leave_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Delete a pending or cancelled leave request.
    """

    leave_request = get_leave_or_404(
        database=database,
        admin_id=current_admin.id,
        leave_id=leave_id,
    )

    if leave_request.status == "approved":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Cancel an approved request before "
                "deleting it."
            ),
        )

    database.delete(leave_request)
    database.commit()

    return MessageResponse(
        message="Leave request deleted successfully."
    )