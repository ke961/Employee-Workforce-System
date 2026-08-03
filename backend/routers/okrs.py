from datetime import datetime
from typing import Literal, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, OKR


router = APIRouter()


# =========================================================
# Request and response schemas
# =========================================================

class OKRCreateRequest(BaseModel):
    objective: str = Field(
        min_length=3,
        max_length=250,
    )

    key_result: str = Field(
        min_length=3,
        max_length=1000,
    )

    quarter: str = Field(
        min_length=2,
        max_length=30,
    )

    progress: int = Field(
        default=0,
        ge=0,
        le=100,
    )

    status: Literal[
        "not_started",
        "in_progress",
        "completed",
        "cancelled",
    ] = "not_started"


class OKRUpdateRequest(BaseModel):
    objective: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=250,
    )

    key_result: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=1000,
    )

    quarter: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30,
    )

    progress: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
    )

    status: Optional[
        Literal[
            "not_started",
            "in_progress",
            "completed",
            "cancelled",
        ]
    ] = None


class OKRProgressRequest(BaseModel):
    progress: int = Field(
        ge=0,
        le=100,
    )


class OKRStatusRequest(BaseModel):
    status: Literal[
        "not_started",
        "in_progress",
        "completed",
        "cancelled",
    ]


class OKRResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    admin_id: int
    objective: str
    key_result: str
    quarter: str
    progress: int
    status: str
    created_at: datetime
    updated_at: datetime


class OKRSummaryResponse(BaseModel):
    total_okrs: int
    not_started_okrs: int
    in_progress_okrs: int
    completed_okrs: int
    cancelled_okrs: int
    average_progress: float


class MessageResponse(BaseModel):
    message: str


# =========================================================
# Helper functions
# =========================================================

def get_okr_or_404(
    database: Session,
    admin_id: int,
    okr_id: int,
) -> OKR:
    """
    Return one OKR belonging to the logged-in Admin.
    """

    okr = (
        database.query(OKR)
        .filter(
            OKR.id == okr_id,
            OKR.admin_id == admin_id,
        )
        .first()
    )

    if okr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OKR not found.",
        )

    return okr


def determine_status_from_progress(
    progress: int,
    current_status: str,
) -> str:
    """
    Automatically update the OKR status from progress.

    0%       = not_started
    1–99%    = in_progress
    100%     = completed

    A cancelled OKR remains cancelled unless its status
    is changed manually.
    """

    if current_status == "cancelled":
        return "cancelled"

    if progress == 0:
        return "not_started"

    if progress == 100:
        return "completed"

    return "in_progress"


# =========================================================
# Create OKR
# POST /api/okrs
# =========================================================

@router.post(
    "",
    response_model=OKRResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_okr(
    okr_data: OKRCreateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Create a personal quarterly objective and key result.
    """

    normalized_objective = (
        okr_data.objective.strip()
    )

    duplicate_okr = (
        database.query(OKR)
        .filter(
            OKR.admin_id == current_admin.id,
            OKR.objective == normalized_objective,
            OKR.quarter == okr_data.quarter.strip(),
            OKR.status != "cancelled",
        )
        .first()
    )

    if duplicate_okr:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "An active OKR with this objective "
                "already exists for the selected quarter."
            ),
        )

    calculated_status = determine_status_from_progress(
        progress=okr_data.progress,
        current_status=okr_data.status,
    )

    if okr_data.status == "cancelled":
        calculated_status = "cancelled"

    okr = OKR(
        admin_id=current_admin.id,
        objective=normalized_objective,
        key_result=okr_data.key_result.strip(),
        quarter=okr_data.quarter.strip(),
        progress=okr_data.progress,
        status=calculated_status,
    )

    database.add(okr)
    database.commit()
    database.refresh(okr)

    return okr


# =========================================================
# OKR summary
# GET /api/okrs/summary
# =========================================================

@router.get(
    "/summary",
    response_model=OKRSummaryResponse,
)
def get_okr_summary(
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return the Admin's OKR statistics.
    """

    okrs = (
        database.query(OKR)
        .filter(
            OKR.admin_id == current_admin.id
        )
        .all()
    )

    total_okrs = len(okrs)

    average_progress = (
        round(
            sum(
                okr.progress
                for okr in okrs
            ) / total_okrs,
            2,
        )
        if total_okrs > 0
        else 0.0
    )

    return OKRSummaryResponse(
        total_okrs=total_okrs,
        not_started_okrs=sum(
            1
            for okr in okrs
            if okr.status == "not_started"
        ),
        in_progress_okrs=sum(
            1
            for okr in okrs
            if okr.status == "in_progress"
        ),
        completed_okrs=sum(
            1
            for okr in okrs
            if okr.status == "completed"
        ),
        cancelled_okrs=sum(
            1
            for okr in okrs
            if okr.status == "cancelled"
        ),
        average_progress=average_progress,
    )


# =========================================================
# Get all OKRs
# GET /api/okrs
# =========================================================

@router.get(
    "",
    response_model=list[OKRResponse],
)
def get_okrs(
    quarter: Optional[str] = Query(
        default=None,
    ),
    okr_status: Optional[str] = Query(
        default=None,
        alias="status",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return personal OKRs with optional quarter
    and status filtering.
    """

    query = (
        database.query(OKR)
        .filter(
            OKR.admin_id == current_admin.id
        )
    )

    if quarter:
        query = query.filter(
            OKR.quarter == quarter.strip()
        )

    if okr_status:
        allowed_statuses = {
            "not_started",
            "in_progress",
            "completed",
            "cancelled",
        }

        if okr_status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OKR status.",
            )

        query = query.filter(
            OKR.status == okr_status
        )

    okrs = (
        query
        .order_by(
            OKR.created_at.desc(),
            OKR.id.desc(),
        )
        .limit(limit)
        .all()
    )

    return okrs


# =========================================================
# Get one OKR
# GET /api/okrs/{okr_id}
# =========================================================

@router.get(
    "/{okr_id}",
    response_model=OKRResponse,
)
def get_okr(
    okr_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Return one OKR belonging to the Admin.
    """

    return get_okr_or_404(
        database=database,
        admin_id=current_admin.id,
        okr_id=okr_id,
    )


# =========================================================
# Update OKR
# PATCH /api/okrs/{okr_id}
# =========================================================

@router.patch(
    "/{okr_id}",
    response_model=OKRResponse,
)
def update_okr(
    okr_id: int,
    okr_data: OKRUpdateRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Update an existing objective, key result,
    quarter, progress, or status.
    """

    okr = get_okr_or_404(
        database=database,
        admin_id=current_admin.id,
        okr_id=okr_id,
    )

    update_data = okr_data.model_dump(
        exclude_unset=True
    )

    if "objective" in update_data:
        update_data["objective"] = (
            update_data["objective"].strip()
        )

    if "key_result" in update_data:
        update_data["key_result"] = (
            update_data["key_result"].strip()
        )

    if "quarter" in update_data:
        update_data["quarter"] = (
            update_data["quarter"].strip()
        )

    for field_name, field_value in (
        update_data.items()
    ):
        setattr(
            okr,
            field_name,
            field_value,
        )

    if (
        "progress" in update_data
        and "status" not in update_data
    ):
        okr.status = determine_status_from_progress(
            progress=okr.progress,
            current_status=okr.status,
        )

    if (
        "status" in update_data
        and okr.status == "completed"
    ):
        okr.progress = 100

    if (
        "status" in update_data
        and okr.status == "not_started"
    ):
        okr.progress = 0

    database.commit()
    database.refresh(okr)

    return okr


# =========================================================
# Update only OKR progress
# PATCH /api/okrs/{okr_id}/progress
# =========================================================

@router.patch(
    "/{okr_id}/progress",
    response_model=OKRResponse,
)
def update_okr_progress(
    okr_id: int,
    progress_data: OKRProgressRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Update the progress percentage of an OKR.
    """

    okr = get_okr_or_404(
        database=database,
        admin_id=current_admin.id,
        okr_id=okr_id,
    )

    if okr.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A cancelled OKR cannot be updated. "
                "Change its status first."
            ),
        )

    okr.progress = progress_data.progress

    okr.status = determine_status_from_progress(
        progress=okr.progress,
        current_status=okr.status,
    )

    database.commit()
    database.refresh(okr)

    return okr


# =========================================================
# Update only OKR status
# PATCH /api/okrs/{okr_id}/status
# =========================================================

@router.patch(
    "/{okr_id}/status",
    response_model=OKRResponse,
)
def update_okr_status(
    okr_id: int,
    status_data: OKRStatusRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Change the status of an OKR.
    """

    okr = get_okr_or_404(
        database=database,
        admin_id=current_admin.id,
        okr_id=okr_id,
    )

    okr.status = status_data.status

    if okr.status == "completed":
        okr.progress = 100

    elif okr.status == "not_started":
        okr.progress = 0

    elif (
        okr.status == "in_progress"
        and okr.progress == 0
    ):
        okr.progress = 1

    database.commit()
    database.refresh(okr)

    return okr


# =========================================================
# Delete OKR
# DELETE /api/okrs/{okr_id}
# =========================================================

@router.delete(
    "/{okr_id}",
    response_model=MessageResponse,
)
def delete_okr(
    okr_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
    database: Session = Depends(get_db),
):
    """
    Permanently delete one OKR.
    """

    okr = get_okr_or_404(
        database=database,
        admin_id=current_admin.id,
        okr_id=okr_id,
    )

    database.delete(okr)
    database.commit()

    return MessageResponse(
        message="OKR deleted successfully."
    )