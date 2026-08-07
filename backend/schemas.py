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
from typing import Literal, Optional

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