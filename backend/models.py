# from datetime import datetime, timezone

# from sqlalchemy import (
#     Boolean,
#     CheckConstraint,
#     Column,
#     Date,
#     DateTime,
#     ForeignKey,
#     Integer,
#     String,
#     Text,
# )
# from sqlalchemy.orm import relationship

# from database import Base


# def utc_now() -> datetime:
#     """Return the current UTC date and time."""

#     return datetime.now(timezone.utc)


# # =========================================================
# # User model
# # =========================================================

# class User(Base):
#     __tablename__ = "users"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     full_name = Column(
#         String(100),
#         nullable=False,
#     )

#     email = Column(
#         String(150),
#         unique=True,
#         index=True,
#         nullable=False,
#     )

#     password_hash = Column(
#         String(255),
#         nullable=False,
#     )

#     role = Column(
#         String(20),
#         nullable=False,
#         default="employee",
#     )

#     job_title = Column(
#         String(100),
#         nullable=True,
#     )

#     department = Column(
#         String(100),
#         nullable=True,
#     )

#     phone = Column(
#         String(30),
#         nullable=True,
#     )

#     address = Column(
#         Text,
#         nullable=True,
#     )

#     profile_image = Column(
#         String(255),
#         nullable=True,
#     )

#     leave_balance = Column(
#         Integer,
#         nullable=False,
#         default=20,
#     )

#     is_active = Column(
#         Boolean,
#         nullable=False,
#         default=True,
#     )

#     manager_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="SET NULL",
#         ),
#         nullable=True,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#     )

#     updated_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#         onupdate=utc_now,
#     )

#     # Self-referential relationship:
#     # one manager can supervise many employees.
#     manager = relationship(
#         "User",
#         remote_side=[id],
#         back_populates="team_members",
#     )

#     team_members = relationship(
#         "User",
#         back_populates="manager",
#     )

#     attendance_records = relationship(
#         "Attendance",
#         back_populates="employee",
#         cascade="all, delete-orphan",
#         foreign_keys="Attendance.employee_id",
#     )

#     leave_requests = relationship(
#         "LeaveRequest",
#         back_populates="employee",
#         cascade="all, delete-orphan",
#         foreign_keys="LeaveRequest.employee_id",
#     )

#     reviewed_leave_requests = relationship(
#         "LeaveRequest",
#         back_populates="reviewer",
#         foreign_keys="LeaveRequest.reviewer_id",
#     )

#     onboarding_tasks = relationship(
#         "OnboardingTask",
#         back_populates="employee",
#         cascade="all, delete-orphan",
#     )

#     okrs = relationship(
#         "OKR",
#         back_populates="employee",
#         cascade="all, delete-orphan",
#     )

#     audit_logs = relationship(
#         "AuditLog",
#         back_populates="user",
#         foreign_keys="AuditLog.user_id",
#     )

#     __table_args__ = (
#         CheckConstraint(
#             "role IN ('admin', 'manager', 'employee')",
#             name="check_user_role",
#         ),
#         CheckConstraint(
#             "leave_balance >= 0",
#             name="check_leave_balance",
#         ),
#     )


# # =========================================================
# # Attendance model
# # =========================================================

# class Attendance(Base):
#     __tablename__ = "attendance"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     employee_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )

#     attendance_date = Column(
#         Date,
#         nullable=False,
#         index=True,
#     )

#     clock_in = Column(
#         DateTime(timezone=True),
#         nullable=False,
#     )

#     clock_out = Column(
#         DateTime(timezone=True),
#         nullable=True,
#     )

#     status = Column(
#         String(30),
#         nullable=False,
#         default="present",
#     )

#     total_work_minutes = Column(
#         Integer,
#         nullable=False,
#         default=0,
#     )

#     notes = Column(
#         Text,
#         nullable=True,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#     )

#     employee = relationship(
#         "User",
#         back_populates="attendance_records",
#         foreign_keys=[employee_id],
#     )

#     __table_args__ = (
#         CheckConstraint(
#             "status IN ('present', 'late', 'absent', 'half_day')",
#             name="check_attendance_status",
#         ),
#         CheckConstraint(
#             "total_work_minutes >= 0",
#             name="check_work_minutes",
#         ),
#     )


# # =========================================================
# # Leave request model
# # =========================================================

# class LeaveRequest(Base):
#     __tablename__ = "leave_requests"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     employee_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )

#     leave_type = Column(
#         String(50),
#         nullable=False,
#     )

#     start_date = Column(
#         Date,
#         nullable=False,
#     )

#     end_date = Column(
#         Date,
#         nullable=False,
#     )

#     total_days = Column(
#         Integer,
#         nullable=False,
#         default=1,
#     )

#     reason = Column(
#         Text,
#         nullable=False,
#     )

#     status = Column(
#         String(30),
#         nullable=False,
#         default="pending",
#         index=True,
#     )

#     reviewer_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="SET NULL",
#         ),
#         nullable=True,
#     )

#     reviewer_comment = Column(
#         Text,
#         nullable=True,
#     )

#     reviewed_at = Column(
#         DateTime(timezone=True),
#         nullable=True,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#     )

#     updated_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#         onupdate=utc_now,
#     )

#     employee = relationship(
#         "User",
#         back_populates="leave_requests",
#         foreign_keys=[employee_id],
#     )

#     reviewer = relationship(
#         "User",
#         back_populates="reviewed_leave_requests",
#         foreign_keys=[reviewer_id],
#     )

#     __table_args__ = (
#         CheckConstraint(
#             "status IN ('pending', 'approved', 'denied', 'cancelled')",
#             name="check_leave_status",
#         ),
#         CheckConstraint(
#             "total_days > 0",
#             name="check_leave_days",
#         ),
#         CheckConstraint(
#             "end_date >= start_date",
#             name="check_leave_date_range",
#         ),
#     )


# # =========================================================
# # Onboarding task model
# # =========================================================

# class OnboardingTask(Base):
#     __tablename__ = "onboarding_tasks"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     employee_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )

#     title = Column(
#         String(200),
#         nullable=False,
#     )

#     description = Column(
#         Text,
#         nullable=True,
#     )

#     due_date = Column(
#         Date,
#         nullable=True,
#     )

#     is_completed = Column(
#         Boolean,
#         nullable=False,
#         default=False,
#     )

#     completed_at = Column(
#         DateTime(timezone=True),
#         nullable=True,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#     )

#     employee = relationship(
#         "User",
#         back_populates="onboarding_tasks",
#     )


# # =========================================================
# # OKR model
# # =========================================================

# class OKR(Base):
#     __tablename__ = "okrs"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     employee_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )

#     objective = Column(
#         String(250),
#         nullable=False,
#     )

#     key_result = Column(
#         Text,
#         nullable=False,
#     )

#     quarter = Column(
#         String(30),
#         nullable=False,
#     )

#     progress = Column(
#         Integer,
#         nullable=False,
#         default=0,
#     )

#     status = Column(
#         String(30),
#         nullable=False,
#         default="in_progress",
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#     )

#     updated_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#         onupdate=utc_now,
#     )

#     employee = relationship(
#         "User",
#         back_populates="okrs",
#     )

#     __table_args__ = (
#         CheckConstraint(
#             "progress >= 0 AND progress <= 100",
#             name="check_okr_progress",
#         ),
#         CheckConstraint(
#             "status IN ('not_started', 'in_progress', 'completed', 'cancelled')",
#             name="check_okr_status",
#         ),
#     )


# # =========================================================
# # Audit log model
# # =========================================================

# class AuditLog(Base):
#     __tablename__ = "audit_logs"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     user_id = Column(
#         Integer,
#         ForeignKey(
#             "users.id",
#             ondelete="SET NULL",
#         ),
#         nullable=True,
#         index=True,
#     )

#     action = Column(
#         String(100),
#         nullable=False,
#     )

#     entity_type = Column(
#         String(100),
#         nullable=False,
#     )

#     entity_id = Column(
#         Integer,
#         nullable=True,
#     )

#     description = Column(
#         Text,
#         nullable=True,
#     )

#     ip_address = Column(
#         String(50),
#         nullable=True,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         nullable=False,
#         default=utc_now,
#         index=True,
#     )

#     user = relationship(
#         "User",
#         back_populates="audit_logs",
#         foreign_keys=[user_id],
#     )



from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


def utc_now() -> datetime:
    """Return the current UTC date and time."""

    return datetime.now(timezone.utc)


# =========================================================
# Single Admin user
# =========================================================

class Admin(Base):
    __tablename__ = "admins"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name = Column(
        String(100),
        nullable=False,
        default="System Administrator",
    )

    email = Column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    job_title = Column(
        String(100),
        nullable=False,
        default="Administrator",
    )

    department = Column(
        String(100),
        nullable=False,
        default="Administration",
    )

    phone = Column(
        String(30),
        nullable=True,
    )

    profile_image = Column(
        String(255),
        nullable=True,
    )

    leave_balance = Column(
        Integer,
        nullable=False,
        default=20,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    attendance_records = relationship(
        "Attendance",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    leave_requests = relationship(
        "LeaveRequest",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    onboarding_tasks = relationship(
        "OnboardingTask",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    okrs = relationship(
        "OKR",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    tasks = relationship(
        "Task",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    expense_claims = relationship(
        "ExpenseClaim",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    document_acknowledgments = relationship(
        "DocumentAcknowledgment",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "leave_balance >= 0",
            name="check_admin_leave_balance",
        ),
    )


# =========================================================
# Attendance
# =========================================================

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    attendance_date = Column(
        Date,
        nullable=False,
        index=True,
    )

    clock_in = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    clock_out = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    total_work_minutes = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String(20),
        nullable=False,
        default="present",
    )

    notes = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="attendance_records",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('present', 'late', 'half_day')",
            name="check_attendance_status",
        ),
        CheckConstraint(
            "total_work_minutes >= 0",
            name="check_total_work_minutes",
        ),
    )


# =========================================================
# Leave request
# =========================================================

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    leave_type = Column(
        String(50),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    total_days = Column(
        Integer,
        nullable=False,
        default=1,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        default="pending",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="leave_requests",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'cancelled')",
            name="check_leave_status",
        ),
        CheckConstraint(
            "total_days > 0",
            name="check_leave_total_days",
        ),
        CheckConstraint(
            "end_date >= start_date",
            name="check_leave_date_range",
        ),
    )


# =========================================================
# Onboarding task
# =========================================================

class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    due_date = Column(
        Date,
        nullable=True,
    )

    is_completed = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="onboarding_tasks",
    )


# =========================================================
# Personal OKR
# =========================================================

class OKR(Base):
    __tablename__ = "okrs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    objective = Column(
        String(250),
        nullable=False,
    )

    key_result = Column(
        Text,
        nullable=False,
    )

    quarter = Column(
        String(30),
        nullable=False,
    )

    progress = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String(20),
        nullable=False,
        default="not_started",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="okrs",
    )

    __table_args__ = (
        CheckConstraint(
            "progress >= 0 AND progress <= 100",
            name="check_okr_progress",
        ),
        CheckConstraint(
            "status IN "
            "('not_started', 'in_progress', 'completed', 'cancelled')",
            name="check_okr_status",
        ),
    )


# =========================================================
# Task & Project Model
# =========================================================

class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    priority = Column(
        String(20),
        nullable=False,
        default="medium",
    )

    status = Column(
        String(20),
        nullable=False,
        default="todo",
    )

    due_date = Column(
        Date,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="tasks",
    )

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name="check_task_priority",
        ),
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'review', 'completed')",
            name="check_task_status",
        ),
    )


# =========================================================
# Company Announcement Model
# =========================================================

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String(50),
        nullable=False,
        default="General",
    )

    is_pinned = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    author = Column(
        String(100),
        nullable=False,
        default="HR Operations",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


# =========================================================
# Expense Claim Model
# =========================================================

class ExpenseClaim(Base):
    __tablename__ = "expense_claims"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    category = Column(
        String(50),
        nullable=False,
        default="General",
    )

    amount = Column(
        Integer,
        nullable=False,
    )

    merchant = Column(
        String(150),
        nullable=False,
    )

    expense_date = Column(
        Date,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(20),
        nullable=False,
        default="pending",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    admin = relationship(
        "Admin",
        back_populates="expense_claims",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="check_expense_status",
        ),
        CheckConstraint(
            "amount > 0",
            name="check_expense_amount",
        ),
    )


# =========================================================
# Performance Review Model
# =========================================================

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    reviewer_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    employee_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    review_cycle = Column(
        String(50),
        nullable=False,
        default="Q3 2026",
    )

    rating = Column(
        Integer,
        nullable=False,
        default=5,
    )

    strengths = Column(
        Text,
        nullable=True,
    )

    growth_areas = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(20),
        nullable=False,
        default="completed",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    reviewer = relationship(
        "Admin",
        foreign_keys=[reviewer_id],
    )

    employee = relationship(
        "Admin",
        foreign_keys=[employee_id],
    )

    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="check_review_rating",
        ),
        CheckConstraint(
            "status IN ('draft', 'pending', 'completed')",
            name="check_review_status",
        ),
    )


# =========================================================
# Peer Recognition (Kudos) Model
# =========================================================

class Kudos(Base):
    __tablename__ = "kudos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    sender_name = Column(
        String(100),
        nullable=False,
    )

    receiver_name = Column(
        String(100),
        nullable=False,
    )

    category = Column(
        String(50),
        nullable=False,
        default="Teamwork",
    )

    message = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


# =========================================================
# Company Document Model
# =========================================================

class CompanyDocument(Base):
    __tablename__ = "company_documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    category = Column(
        String(50),
        nullable=False,
        default="Policy",
    )

    summary = Column(
        Text,
        nullable=False,
    )

    file_url = Column(
        String(255),
        nullable=True,
    )

    version = Column(
        String(20),
        nullable=False,
        default="v1.0",
    )

    requires_acknowledgment = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    acknowledgments = relationship(
        "DocumentAcknowledgment",
        back_populates="document",
        cascade="all, delete-orphan",
    )


# =========================================================
# Document Acknowledgment Model
# =========================================================

class DocumentAcknowledgment(Base):
    __tablename__ = "document_acknowledgments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey(
            "company_documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    acknowledged_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    document = relationship(
        "CompanyDocument",
        back_populates="acknowledgments",
    )

    admin = relationship(
        "Admin",
        back_populates="document_acknowledgments",
    )


# =========================================================
# Work Shift Schedule Model
# =========================================================

class ShiftSchedule(Base):
    __tablename__ = "shift_schedules"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    shift_name = Column(
        String(100),
        nullable=False,
        default="Standard Morning Shift",
    )

    shift_type = Column(
        String(50),
        nullable=False,
        default="Morning",
    )

    start_time = Column(
        String(20),
        nullable=False,
        default="09:00 AM",
    )

    end_time = Column(
        String(20),
        nullable=False,
        default="05:00 PM",
    )

    work_days = Column(
        String(100),
        nullable=False,
        default="Mon, Tue, Wed, Thu, Fri",
    )

    location = Column(
        String(50),
        nullable=False,
        default="Remote Flexible",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    admin = relationship(
        "Admin",
        foreign_keys=[admin_id],
    )


# =========================================================
# IT Hardware & Asset Model
# =========================================================

class ITAsset(Base):
    __tablename__ = "it_assets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    asset_name = Column(
        String(150),
        nullable=False,
    )

    asset_tag = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    category = Column(
        String(50),
        nullable=False,
        default="Laptop",
    )

    serial_number = Column(
        String(100),
        nullable=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="assigned",
    )

    assigned_date = Column(
        Date,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    assigned_user = relationship(
        "Admin",
        foreign_keys=[admin_id],
    )


# =========================================================
# Company Event & Calendar Model
# =========================================================

class CompanyEvent(Base):
    __tablename__ = "company_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    event_type = Column(
        String(50),
        nullable=False,
        default="Company Holiday",
    )

    event_date = Column(
        Date,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    location = Column(
        String(100),
        nullable=False,
        default="Company-Wide",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


# =========================================================
# Training Course & Certifications Model
# =========================================================

class TrainingCourse(Base):
    __tablename__ = "training_courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    category = Column(
        String(50),
        nullable=False,
        default="Security",
    )

    description = Column(
        Text,
        nullable=True,
    )

    duration_hours = Column(
        Integer,
        nullable=False,
        default=2,
    )

    due_date = Column(
        Date,
        nullable=True,
    )

    admin_id = Column(
        Integer,
        ForeignKey(
            "admins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        default="assigned",
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    admin = relationship(
        "Admin",
        foreign_keys=[admin_id],
    )

