# from datetime import date, datetime
# from typing import Literal, Optional

# from pydantic import BaseModel, ConfigDict, EmailStr, Field


# # =========================================================
# # Shared schema configuration
# # =========================================================

# class ORMBaseModel(BaseModel):
#     """
#     Base schema that allows Pydantic to read data directly
#     from SQLAlchemy model objects.
#     """

#     model_config = ConfigDict(from_attributes=True)


# # =========================================================
# # Authentication schemas
# # =========================================================

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str = Field(
#         min_length=6,
#         max_length=100,
#     )


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"


# class LoginUserResponse(ORMBaseModel):
#     id: int
#     full_name: str
#     email: EmailStr
#     role: Literal["admin", "manager", "employee"]
#     job_title: Optional[str] = None
#     department: Optional[str] = None
#     leave_balance: int


# class LoginResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user: LoginUserResponse


# # =========================================================
# # User and employee schemas
# # =========================================================

# class UserCreate(BaseModel):
#     full_name: str = Field(
#         min_length=2,
#         max_length=100,
#     )

#     email: EmailStr

#     password: str = Field(
#         min_length=6,
#         max_length=100,
#     )

#     role: Literal[
#         "admin",
#         "manager",
#         "employee",
#     ] = "employee"

#     job_title: Optional[str] = Field(
#         default=None,
#         max_length=100,
#     )

#     department: Optional[str] = Field(
#         default=None,
#         max_length=100,
#     )

#     phone: Optional[str] = Field(
#         default=None,
#         max_length=30,
#     )

#     address: Optional[str] = None

#     manager_id: Optional[int] = None

#     leave_balance: int = Field(
#         default=20,
#         ge=0,
#         le=365,
#     )


# class UserUpdate(BaseModel):
#     full_name: Optional[str] = Field(
#         default=None,
#         min_length=2,
#         max_length=100,
#     )

#     email: Optional[EmailStr] = None

#     role: Optional[
#         Literal["admin", "manager", "employee"]
#     ] = None

#     job_title: Optional[str] = Field(
#         default=None,
#         max_length=100,
#     )

#     department: Optional[str] = Field(
#         default=None,
#         max_length=100,
#     )

#     phone: Optional[str] = Field(
#         default=None,
#         max_length=30,
#     )

#     address: Optional[str] = None

#     profile_image: Optional[str] = None

#     manager_id: Optional[int] = None

#     leave_balance: Optional[int] = Field(
#         default=None,
#         ge=0,
#         le=365,
#     )

#     is_active: Optional[bool] = None


# class PasswordUpdate(BaseModel):
#     current_password: str = Field(
#         min_length=6,
#         max_length=100,
#     )

#     new_password: str = Field(
#         min_length=6,
#         max_length=100,
#     )


# class AdminPasswordReset(BaseModel):
#     new_password: str = Field(
#         min_length=6,
#         max_length=100,
#     )


# class UserResponse(ORMBaseModel):
#     id: int
#     full_name: str
#     email: EmailStr

#     role: Literal[
#         "admin",
#         "manager",
#         "employee",
#     ]

#     job_title: Optional[str] = None
#     department: Optional[str] = None
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     profile_image: Optional[str] = None

#     leave_balance: int
#     is_active: bool
#     manager_id: Optional[int] = None

#     created_at: datetime
#     updated_at: datetime


# class EmployeeListResponse(ORMBaseModel):
#     id: int
#     full_name: str
#     email: EmailStr

#     role: Literal[
#         "admin",
#         "manager",
#         "employee",
#     ]

#     job_title: Optional[str] = None
#     department: Optional[str] = None
#     manager_id: Optional[int] = None
#     leave_balance: int
#     is_active: bool


# class ManagerInformation(BaseModel):
#     id: int
#     full_name: str
#     email: EmailStr
#     job_title: Optional[str] = None


# class UserProfileResponse(UserResponse):
#     manager: Optional[ManagerInformation] = None


# # =========================================================
# # Attendance schemas
# # =========================================================

# class AttendanceClockInRequest(BaseModel):
#     notes: Optional[str] = Field(
#         default=None,
#         max_length=500,
#     )


# class AttendanceClockOutRequest(BaseModel):
#     notes: Optional[str] = Field(
#         default=None,
#         max_length=500,
#     )


# class AttendanceResponse(ORMBaseModel):
#     id: int
#     employee_id: int
#     attendance_date: date
#     clock_in: datetime
#     clock_out: Optional[datetime] = None

#     status: Literal[
#         "present",
#         "late",
#         "absent",
#         "half_day",
#     ]

#     total_work_minutes: int
#     notes: Optional[str] = None
#     created_at: datetime


# class AttendanceStatusResponse(BaseModel):
#     is_clocked_in: bool
#     active_attendance_id: Optional[int] = None
#     clock_in: Optional[datetime] = None
#     message: str


# class AttendanceSummaryResponse(BaseModel):
#     total_records: int
#     total_work_minutes: int
#     total_work_hours: float
#     present_days: int
#     late_days: int
#     half_days: int


# # =========================================================
# # Leave schemas
# # =========================================================

# class LeaveRequestCreate(BaseModel):
#     leave_type: str = Field(
#         min_length=2,
#         max_length=50,
#     )

#     start_date: date
#     end_date: date

#     reason: str = Field(
#         min_length=3,
#         max_length=1000,
#     )


# class LeaveReviewRequest(BaseModel):
#     status: Literal[
#         "approved",
#         "denied",
#     ]

#     reviewer_comment: Optional[str] = Field(
#         default=None,
#         max_length=1000,
#     )


# class LeaveCancelRequest(BaseModel):
#     cancellation_reason: Optional[str] = Field(
#         default=None,
#         max_length=500,
#     )


# class LeaveEmployeeInformation(BaseModel):
#     id: int
#     full_name: str
#     email: EmailStr
#     job_title: Optional[str] = None
#     department: Optional[str] = None


# class LeaveReviewerInformation(BaseModel):
#     id: int
#     full_name: str
#     email: EmailStr


# class LeaveRequestResponse(ORMBaseModel):
#     id: int
#     employee_id: int
#     leave_type: str
#     start_date: date
#     end_date: date
#     total_days: int
#     reason: str

#     status: Literal[
#         "pending",
#         "approved",
#         "denied",
#         "cancelled",
#     ]

#     reviewer_id: Optional[int] = None
#     reviewer_comment: Optional[str] = None
#     reviewed_at: Optional[datetime] = None
#     created_at: datetime
#     updated_at: datetime


# class LeaveRequestDetailResponse(LeaveRequestResponse):
#     employee: Optional[LeaveEmployeeInformation] = None
#     reviewer: Optional[LeaveReviewerInformation] = None


# # =========================================================
# # Onboarding schemas
# # =========================================================

# class OnboardingTaskCreate(BaseModel):
#     employee_id: int

#     title: str = Field(
#         min_length=2,
#         max_length=200,
#     )

#     description: Optional[str] = Field(
#         default=None,
#         max_length=1000,
#     )

#     due_date: Optional[date] = None


# class OnboardingTaskUpdate(BaseModel):
#     title: Optional[str] = Field(
#         default=None,
#         min_length=2,
#         max_length=200,
#     )

#     description: Optional[str] = Field(
#         default=None,
#         max_length=1000,
#     )

#     due_date: Optional[date] = None
#     is_completed: Optional[bool] = None


# class OnboardingTaskStatusUpdate(BaseModel):
#     is_completed: bool


# class OnboardingTaskResponse(ORMBaseModel):
#     id: int
#     employee_id: int
#     title: str
#     description: Optional[str] = None
#     due_date: Optional[date] = None
#     is_completed: bool
#     completed_at: Optional[datetime] = None
#     created_at: datetime


# class OnboardingProgressResponse(BaseModel):
#     total_tasks: int
#     completed_tasks: int
#     pending_tasks: int
#     progress_percentage: float


# # =========================================================
# # OKR schemas
# # =========================================================

# class OKRCreate(BaseModel):
#     objective: str = Field(
#         min_length=3,
#         max_length=250,
#     )

#     key_result: str = Field(
#         min_length=3,
#         max_length=1000,
#     )

#     quarter: str = Field(
#         min_length=2,
#         max_length=30,
#     )

#     progress: int = Field(
#         default=0,
#         ge=0,
#         le=100,
#     )

#     status: Literal[
#         "not_started",
#         "in_progress",
#         "completed",
#         "cancelled",
#     ] = "not_started"


# class OKRUpdate(BaseModel):
#     objective: Optional[str] = Field(
#         default=None,
#         min_length=3,
#         max_length=250,
#     )

#     key_result: Optional[str] = Field(
#         default=None,
#         min_length=3,
#         max_length=1000,
#     )

#     quarter: Optional[str] = Field(
#         default=None,
#         min_length=2,
#         max_length=30,
#     )

#     progress: Optional[int] = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     status: Optional[
#         Literal[
#             "not_started",
#             "in_progress",
#             "completed",
#             "cancelled",
#         ]
#     ] = None


# class OKRProgressUpdate(BaseModel):
#     progress: int = Field(
#         ge=0,
#         le=100,
#     )


# class OKRResponse(ORMBaseModel):
#     id: int
#     employee_id: int
#     objective: str
#     key_result: str
#     quarter: str
#     progress: int

#     status: Literal[
#         "not_started",
#         "in_progress",
#         "completed",
#         "cancelled",
#     ]

#     created_at: datetime
#     updated_at: datetime


# # =========================================================
# # Audit log schemas
# # =========================================================

# class AuditLogCreate(BaseModel):
#     user_id: Optional[int] = None

#     action: str = Field(
#         min_length=2,
#         max_length=100,
#     )

#     entity_type: str = Field(
#         min_length=2,
#         max_length=100,
#     )

#     entity_id: Optional[int] = None

#     description: Optional[str] = Field(
#         default=None,
#         max_length=2000,
#     )

#     ip_address: Optional[str] = Field(
#         default=None,
#         max_length=50,
#     )


# class AuditUserInformation(BaseModel):
#     id: int
#     full_name: str
#     email: EmailStr
#     role: str


# class AuditLogResponse(ORMBaseModel):
#     id: int
#     user_id: Optional[int] = None
#     action: str
#     entity_type: str
#     entity_id: Optional[int] = None
#     description: Optional[str] = None
#     ip_address: Optional[str] = None
#     created_at: datetime


# class AuditLogDetailResponse(AuditLogResponse):
#     user: Optional[AuditUserInformation] = None


# # =========================================================
# # Dashboard schemas
# # =========================================================

# class DashboardAttendanceData(BaseModel):
#     is_clocked_in: bool
#     clock_in: Optional[datetime] = None


# class DashboardOnboardingData(BaseModel):
#     total: int
#     completed: int
#     pending: int
#     progress_percentage: float


# class EmployeeDashboardResponse(BaseModel):
#     employee: UserResponse
#     attendance: DashboardAttendanceData
#     pending_leave_requests: int
#     approved_leave_requests: int
#     onboarding: DashboardOnboardingData
#     total_okrs: int
#     completed_okrs: int


# class ManagerDashboardResponse(BaseModel):
#     manager: UserResponse
#     total_team_members: int
#     pending_leave_requests: int
#     employees_clocked_in: int
#     employees_clocked_out: int
#     total_team_okrs: int


# class AdminDashboardResponse(BaseModel):
#     admin: UserResponse
#     total_users: int
#     total_employees: int
#     total_managers: int
#     active_users: int
#     pending_leave_requests: int
#     employees_clocked_in: int


# # =========================================================
# # General response schema
# # =========================================================

# class MessageResponse(BaseModel):
#     message: str


# class DeleteResponse(BaseModel):
#     message: str
#     deleted_id: int




from datetime import date, datetime
from typing import Dict, List, Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


# =========================================================
# Shared configuration
# =========================================================

class ORMBaseModel(BaseModel):
    """
    Allows Pydantic schemas to read SQLAlchemy objects.
    """

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# General response
# =========================================================

class MessageResponse(BaseModel):
    message: str


class DeleteResponse(BaseModel):
    message: str
    deleted_id: int


# =========================================================
# Admin authentication schemas
# =========================================================

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6,
        max_length=100,
    )


class AdminCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100,
    )

    role: Optional[str] = Field(
        default="employee",
        max_length=20,
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )


class AdminUpdate(BaseModel):
    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: Optional[EmailStr] = None

    role: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    profile_image: Optional[str] = Field(
        default=None,
        max_length=255,
    )


class AdminPasswordUpdate(BaseModel):
    current_password: str = Field(
        min_length=6,
        max_length=100,
    )

    new_password: str = Field(
        min_length=6,
        max_length=100,
    )


class AdminResponse(ORMBaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str = "employee"
    job_title: Optional[str] = "Administrator"
    department: Optional[str] = "Administration"
    leave_balance: int = 20
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: AdminResponse


# =========================================================
# Employee schemas
# =========================================================

class EmployeeCreate(BaseModel):
    employee_code: str = Field(
        min_length=2,
        max_length=30,
    )

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    job_title: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    department: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    employment_type: Literal[
        "full_time",
        "part_time",
        "contract",
        "intern",
    ] = "full_time"

    joining_date: Optional[date] = None

    address: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    profile_image: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    leave_balance: int = Field(
        default=20,
        ge=0,
        le=365,
    )


class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30,
    )

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    job_title: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    department: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    employment_type: Optional[
        Literal[
            "full_time",
            "part_time",
            "contract",
            "intern",
        ]
    ] = None

    joining_date: Optional[date] = None

    address: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    profile_image: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    leave_balance: Optional[int] = Field(
        default=None,
        ge=0,
        le=365,
    )

    is_active: Optional[bool] = None


class EmployeeResponse(ORMBaseModel):
    id: int
    employee_code: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None

    employment_type: Literal[
        "full_time",
        "part_time",
        "contract",
        "intern",
    ]

    joining_date: Optional[date] = None
    address: Optional[str] = None
    profile_image: Optional[str] = None
    leave_balance: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class EmployeeListResponse(ORMBaseModel):
    id: int
    employee_code: str
    full_name: str
    email: EmailStr
    job_title: Optional[str] = None
    department: Optional[str] = None
    employment_type: str
    leave_balance: int
    is_active: bool


# =========================================================
# Attendance schemas
# =========================================================

class AttendanceCreate(BaseModel):
    employee_id: int

    attendance_date: date

    clock_in: datetime

    clock_out: Optional[datetime] = None

    status: Literal[
        "present",
        "late",
        "absent",
        "half_day",
    ] = "present"

    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    @model_validator(mode="after")
    def validate_clock_times(self):
        if (
            self.clock_out is not None
            and self.clock_out < self.clock_in
        ):
            raise ValueError(
                "Clock-out time cannot be earlier than clock-in time."
            )

        return self


class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None

    clock_in: Optional[datetime] = None

    clock_out: Optional[datetime] = None

    status: Optional[
        Literal[
            "present",
            "late",
            "absent",
            "half_day",
        ]
    ] = None

    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class AttendanceResponse(ORMBaseModel):
    id: int
    employee_id: int
    attendance_date: date
    clock_in: datetime
    clock_out: Optional[datetime] = None
    total_work_minutes: int

    status: Literal[
        "present",
        "late",
        "absent",
        "half_day",
    ]

    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AttendanceDetailResponse(AttendanceResponse):
    employee: Optional[EmployeeListResponse] = None


class AttendanceSummaryResponse(BaseModel):
    employee_id: int
    total_records: int
    present_days: int
    late_days: int
    absent_days: int
    half_days: int
    total_work_minutes: int
    total_work_hours: float


# =========================================================
# Leave request schemas
# =========================================================

class LeaveRequestCreate(BaseModel):
    employee_id: int

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
    def validate_leave_dates(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "End date cannot be earlier than start date."
            )

        return self


class LeaveRequestUpdate(BaseModel):
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


class LeaveReviewRequest(BaseModel):
    status: Literal[
        "approved",
        "denied",
    ]

    admin_comment: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class LeaveCancelRequest(BaseModel):
    admin_comment: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class LeaveRequestResponse(ORMBaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    reason: str

    status: Literal[
        "pending",
        "approved",
        "denied",
        "cancelled",
    ]

    admin_comment: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class LeaveRequestDetailResponse(
    LeaveRequestResponse
):
    employee: Optional[EmployeeListResponse] = None


# =========================================================
# Onboarding task schemas
# =========================================================

class OnboardingTaskCreate(BaseModel):
    employee_id: int

    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    due_date: Optional[date] = None


class OnboardingTaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    due_date: Optional[date] = None

    is_completed: Optional[bool] = None


class OnboardingStatusUpdate(BaseModel):
    is_completed: bool


class OnboardingTaskResponse(ORMBaseModel):
    id: int
    employee_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class OnboardingTaskDetailResponse(
    OnboardingTaskResponse
):
    employee: Optional[EmployeeListResponse] = None


class OnboardingProgressResponse(BaseModel):
    employee_id: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    progress_percentage: float


# =========================================================
# Performance goal schemas
# =========================================================

class PerformanceGoalCreate(BaseModel):
    employee_id: int

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


class PerformanceGoalUpdate(BaseModel):
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


class PerformanceProgressUpdate(BaseModel):
    progress: int = Field(
        ge=0,
        le=100,
    )


class PerformanceGoalResponse(ORMBaseModel):
    id: int
    employee_id: int
    objective: str
    key_result: str
    quarter: str
    progress: int

    status: Literal[
        "not_started",
        "in_progress",
        "completed",
        "cancelled",
    ]

    created_at: datetime
    updated_at: datetime


class PerformanceGoalDetailResponse(
    PerformanceGoalResponse
):
    employee: Optional[EmployeeListResponse] = None


# =========================================================
# Audit log schemas
# =========================================================

class AuditLogResponse(ORMBaseModel):
    id: int
    admin_id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime


# =========================================================
# Admin dashboard schema
# =========================================================

class AdminDashboardResponse(BaseModel):
    total_employees: int
    active_employees: int
    inactive_employees: int
    pending_leave_requests: int
    approved_leave_requests: int
    attendance_records_today: int
    employees_present_today: int
    incomplete_onboarding_tasks: int
    active_performance_goals: int


# =========================================================
# Task Schemas
# =========================================================

class TaskCreate(BaseModel):
    admin_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    status: Literal["todo", "in_progress", "review", "completed"] = "todo"
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None
    status: Optional[Literal["todo", "in_progress", "review", "completed"]] = None
    due_date: Optional[date] = None


class TaskResponse(ORMBaseModel):
    id: int
    admin_id: int
    title: str
    description: Optional[str] = None
    priority: Literal["low", "medium", "high", "urgent"]
    status: Literal["todo", "in_progress", "review", "completed"]
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


# =========================================================
# Announcement Schemas
# =========================================================

class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field("General", max_length=50)
    is_pinned: bool = False
    author: Optional[str] = "HR Operations"


class AnnouncementResponse(ORMBaseModel):
    id: int
    title: str
    content: str
    category: str
    is_pinned: bool
    author: str
    created_at: datetime


# =========================================================
# Expense Claim Schemas
# =========================================================

class ExpenseClaimCreate(BaseModel):
    category: str = Field("General", max_length=50)
    amount: int = Field(..., gt=0)
    merchant: str = Field(..., min_length=1, max_length=150)
    expense_date: date
    description: Optional[str] = None


class ExpenseClaimUpdate(BaseModel):
    status: Literal["pending", "approved", "rejected"]


class ExpenseClaimResponse(ORMBaseModel):
    id: int
    admin_id: int
    category: str
    amount: int
    merchant: str
    expense_date: date
    description: Optional[str] = None
    status: Literal["pending", "approved", "rejected"]
    created_at: datetime
    updated_at: datetime


# =========================================================
# Employee Schemas
# =========================================================

class AdminCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Optional[str] = Field("employee", max_length=20)
    job_title: Optional[str] = Field("Team Member", max_length=100)
    department: Optional[str] = Field("Engineering", max_length=100)
    phone: Optional[str] = Field(None, max_length=30)
    leave_balance: int = Field(20, ge=0)


class AdminUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, max_length=20)
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=30)
    leave_balance: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


# =========================================================
# Performance Review & Kudos Schemas
# =========================================================

class PerformanceReviewCreate(BaseModel):
    employee_id: int
    review_cycle: str = Field("Q3 2026", max_length=50)
    rating: int = Field(5, ge=1, le=5)
    strengths: Optional[str] = None
    growth_areas: Optional[str] = None
    status: Literal["draft", "pending", "completed"] = "completed"


class PerformanceReviewUpdate(BaseModel):
    review_cycle: Optional[str] = Field(None, max_length=50)
    rating: Optional[int] = Field(None, ge=1, le=5)
    strengths: Optional[str] = None
    growth_areas: Optional[str] = None
    status: Optional[Literal["draft", "pending", "completed"]] = None


class PerformanceReviewResponse(ORMBaseModel):
    id: int
    reviewer_id: int
    employee_id: int
    review_cycle: str
    rating: int
    strengths: Optional[str] = None
    growth_areas: Optional[str] = None
    status: Literal["draft", "pending", "completed"]
    created_at: datetime
    updated_at: datetime


class KudosCreate(BaseModel):
    receiver_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field("Teamwork", max_length=50)
    message: str = Field(..., min_length=1)


class KudosResponse(ORMBaseModel):
    id: int
    sender_name: str
    receiver_name: str
    category: str
    message: str
    created_at: datetime


# =========================================================
# Company Document Schemas
# =========================================================

class CompanyDocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field("Policy", max_length=50)
    summary: str = Field(..., min_length=1)
    file_url: Optional[str] = None
    version: str = Field("v1.0", max_length=20)
    requires_acknowledgment: bool = True


class CompanyDocumentResponse(ORMBaseModel):
    id: int
    title: str
    category: str
    summary: str
    file_url: Optional[str] = None
    version: str
    requires_acknowledgment: bool
    created_at: datetime
    is_acknowledged: bool = False


# =========================================================
# Work Shift Schedule Schemas
# =========================================================

class ShiftScheduleCreate(BaseModel):
    admin_id: int
    shift_name: str = Field("Standard Morning Shift", max_length=100)
    shift_type: str = Field("Morning", max_length=50)
    start_time: str = Field("09:00 AM", max_length=20)
    end_time: str = Field("05:00 PM", max_length=20)
    work_days: str = Field("Mon, Tue, Wed, Thu, Fri", max_length=100)
    location: str = Field("Remote Flexible", max_length=50)


class ShiftScheduleResponse(ORMBaseModel):
    id: int
    admin_id: int
    shift_name: str
    shift_type: str
    start_time: str
    end_time: str
    work_days: str
    location: str
    created_at: datetime


# =========================================================
# IT Hardware & Asset Schemas
# =========================================================

class ITAssetCreate(BaseModel):
    asset_name: str = Field(..., min_length=1, max_length=150)
    asset_tag: str = Field(..., min_length=1, max_length=50)
    category: str = Field("Laptop", max_length=50)
    serial_number: Optional[str] = Field(None, max_length=100)
    admin_id: Optional[int] = None
    status: str = Field("assigned", max_length=30)
    assigned_date: Optional[date] = None


class ITAssetUpdate(BaseModel):
    asset_name: Optional[str] = Field(None, max_length=150)
    category: Optional[str] = Field(None, max_length=50)
    serial_number: Optional[str] = Field(None, max_length=100)
    admin_id: Optional[int] = None
    status: Optional[str] = Field(None, max_length=30)
    assigned_date: Optional[date] = None


class ITAssetResponse(ORMBaseModel):
    id: int
    asset_name: str
    asset_tag: str
    category: str
    serial_number: Optional[str] = None
    admin_id: Optional[int] = None
    status: str
    assigned_date: Optional[date] = None
    created_at: datetime


# =========================================================
# Company Event Schemas
# =========================================================

class CompanyEventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    event_type: str = Field("Company Holiday", max_length=50)
    event_date: date
    description: Optional[str] = None
    location: str = Field("Company-Wide", max_length=100)


class CompanyEventResponse(ORMBaseModel):
    id: int
    title: str
    event_type: str
    event_date: date
    description: Optional[str] = None
    location: str
    created_at: datetime


# =========================================================
# Training Course Schemas
# =========================================================

class TrainingCourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field("Security", max_length=50)
    description: Optional[str] = None
    duration_hours: int = Field(2, ge=1)
    due_date: Optional[date] = None
    admin_id: int


class TrainingCourseUpdate(BaseModel):
    status: Literal["assigned", "in_progress", "completed"]


class TrainingCourseResponse(ORMBaseModel):
    id: int
    title: str
    category: str
    description: Optional[str] = None
    duration_hours: int
    due_date: Optional[date] = None
    admin_id: int
    status: Literal["assigned", "in_progress", "completed"]
    completed_at: Optional[datetime] = None
    created_at: datetime


# =========================================================
# Salary & Payslip Schemas
# =========================================================

class PayslipCreate(BaseModel):
    admin_id: int
    month: str = Field(..., max_length=20)
    year: int = Field(..., ge=2000, le=2100)
    basic_salary: float = Field(..., ge=0)
    allowances: float = Field(0.0, ge=0)
    bonus: float = Field(0.0, ge=0)
    tax_deduction: float = Field(0.0, ge=0)
    insurance_deduction: float = Field(0.0, ge=0)
    provident_fund_deduction: float = Field(0.0, ge=0)
    payment_status: Literal["pending", "paid"] = "pending"
    payment_date: Optional[date] = None
    payment_method: str = Field("Direct Bank Deposit", max_length=50)
    notes: Optional[str] = None


class PayslipStatusUpdate(BaseModel):
    payment_status: Literal["pending", "paid"]
    payment_date: Optional[date] = None


class PayslipResponse(ORMBaseModel):
    id: int
    admin_id: int
    month: str
    year: int
    basic_salary: float
    allowances: float
    bonus: float
    tax_deduction: float
    insurance_deduction: float
    provident_fund_deduction: float
    net_salary: float
    payment_status: str
    payment_date: Optional[date] = None
    payment_method: str
    notes: Optional[str] = None
    created_at: datetime
    employee_name: Optional[str] = None
    employee_email: Optional[str] = None
    employee_job_title: Optional[str] = None
    employee_department: Optional[str] = None


# =========================================================
# Recruitment & ATS Schemas
# =========================================================

class JobPostingCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    department: str = Field(..., max_length=100)
    job_type: str = Field("Full-time", max_length=50)
    experience_level: str = Field("Mid-Level", max_length=50)
    salary_range: str = Field("$80,000 - $110,000", max_length=100)
    location: str = Field("Remote Flexible", max_length=100)
    status: Literal["active", "draft", "closed"] = "active"
    description: Optional[str] = None
    requirements: Optional[str] = None


class JobPostingUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Literal["active", "draft", "closed"]] = None
    description: Optional[str] = None
    requirements: Optional[str] = None


class JobPostingResponse(ORMBaseModel):
    id: int
    title: str
    department: str
    job_type: str
    experience_level: str
    salary_range: str
    location: str
    status: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    created_at: datetime
    candidates_count: Optional[int] = 0


class JobCandidateCreate(BaseModel):
    job_id: int
    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    stage: Literal["applied", "screening", "interview", "offered", "hired", "rejected"] = "applied"
    resume_link: Optional[str] = Field(None, max_length=255)
    rating: int = Field(4, ge=1, le=5)
    notes: Optional[str] = None
    applied_date: Optional[date] = None


class CandidateStageUpdate(BaseModel):
    stage: Literal["applied", "screening", "interview", "offered", "hired", "rejected"]
    notes: Optional[str] = None


class JobCandidateResponse(ORMBaseModel):
    id: int
    job_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    stage: str
    resume_link: Optional[str] = None
    rating: int
    notes: Optional[str] = None
    applied_date: Optional[date] = None
    created_at: datetime
    job_title: Optional[str] = None
    job_department: Optional[str] = None


# =========================================================
# Team Messenger Schemas
# =========================================================

class ChatMessageCreate(BaseModel):
    channel: str = Field("general", max_length=50)
    message: str = Field(..., min_length=1, max_length=4000)
    receiver_id: Optional[int] = None
    message_type: Literal["channel", "direct"] = "channel"


class ChatMessageResponse(ORMBaseModel):
    id: int
    channel: str
    sender_id: int
    sender_name: str
    receiver_id: Optional[int] = None
    message: str
    message_type: str
    created_at: datetime


class ChatChannelResponse(BaseModel):
    name: str
    label: str
    description: str
    participant_count: int
    icon: str


# =========================================================
# Pulse Surveys & Ideas Schemas
# =========================================================

class PulseSurveyCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    question: str = Field(..., min_length=5)
    category: str = Field("Workplace Culture", max_length=50)
    options: List[str] = Field(..., min_items=2, max_items=8)


class PulseSurveyResponse(ORMBaseModel):
    id: int
    title: str
    question: str
    category: str
    options: List[str]
    is_active: bool
    created_at: datetime
    total_votes: int
    vote_breakdown: dict
    user_voted_option: Optional[str] = None


class SurveyVotePayload(BaseModel):
    selected_option: str


class EmployeeIdeaCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=5)
    category: str = Field("Culture & Wellness", max_length=50)


class IdeaStatusUpdate(BaseModel):
    status: Literal["under_review", "planned", "in_progress", "implemented"]


class EmployeeIdeaResponse(ORMBaseModel):
    id: int
    admin_id: int
    author_name: str
    title: str
    description: str
    category: str
    upvotes_count: int
    status: str
    created_at: datetime


