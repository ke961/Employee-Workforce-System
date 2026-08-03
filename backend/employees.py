from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    status,
)
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, AuditLog, Employee
from schemas import (
    DeleteResponse,
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)


router = APIRouter()


# =========================================================
# Audit log helper
# =========================================================

def create_audit_log(
    database: Session,
    admin_id: int,
    action: str,
    entity_type: str,
    description: str,
    request: Request,
    entity_id: Optional[int] = None,
) -> None:
    """
    Save an Admin action in the audit log.
    """

    ip_address = None

    if request.client:
        ip_address = request.client.host

    audit_log = AuditLog(
        admin_id=admin_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        ip_address=ip_address,
    )

    database.add(audit_log)


# =========================================================
# Create employee
# URL: POST /api/employees
# =========================================================

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee_data: EmployeeCreate,
    request: Request,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Create a new employee record.

    Employees do not receive login accounts.
    Only the Admin can manage employee records.
    """

    normalized_email = str(
        employee_data.email
    ).strip().lower()

    normalized_employee_code = (
        employee_data.employee_code
        .strip()
        .upper()
    )

    existing_email = (
        database.query(Employee)
        .filter(Employee.email == normalized_email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee with this email already exists.",
        )

    existing_code = (
        database.query(Employee)
        .filter(
            Employee.employee_code
            == normalized_employee_code
        )
        .first()
    )

    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This employee code is already in use.",
        )

    employee = Employee(
        employee_code=normalized_employee_code,
        full_name=employee_data.full_name.strip(),
        email=normalized_email,
        phone=employee_data.phone,
        job_title=employee_data.job_title,
        department=employee_data.department,
        employment_type=employee_data.employment_type,
        joining_date=employee_data.joining_date,
        address=employee_data.address,
        profile_image=employee_data.profile_image,
        leave_balance=employee_data.leave_balance,
        is_active=True,
    )

    database.add(employee)

    try:
        database.flush()

        create_audit_log(
            database=database,
            admin_id=current_admin.id,
            action="CREATE_EMPLOYEE",
            entity_type="employee",
            entity_id=employee.id,
            description=(
                f"Employee {employee.full_name} "
                f"({employee.employee_code}) was created."
            ),
            request=request,
        )

        database.commit()
        database.refresh(employee)

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The employee could not be created because "
                "the email or employee code already exists."
            ),
        ) from error

    return employee


# =========================================================
# Get all employees
# URL: GET /api/employees
# =========================================================

@router.get(
    "",
    response_model=list[EmployeeListResponse],
)
def get_all_employees(
    search: Optional[str] = Query(
        default=None,
        description=(
            "Search by employee name, employee code, "
            "email, department or job title."
        ),
    ),
    department: Optional[str] = Query(
        default=None,
    ),
    employment_type: Optional[str] = Query(
        default=None,
    ),
    is_active: Optional[bool] = Query(
        default=None,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return employee records with optional filtering.
    """

    query = database.query(Employee)

    if search:
        search_value = f"%{search.strip()}%"

        query = query.filter(
            or_(
                Employee.full_name.ilike(search_value),
                Employee.employee_code.ilike(search_value),
                Employee.email.ilike(search_value),
                Employee.department.ilike(search_value),
                Employee.job_title.ilike(search_value),
            )
        )

    if department:
        query = query.filter(
            Employee.department.ilike(
                department.strip()
            )
        )

    if employment_type:
        allowed_types = {
            "full_time",
            "part_time",
            "contract",
            "intern",
        }

        if employment_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid employment type.",
            )

        query = query.filter(
            Employee.employment_type
            == employment_type
        )

    if is_active is not None:
        query = query.filter(
            Employee.is_active == is_active
        )

    employees = (
        query
        .order_by(Employee.full_name.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return employees


# =========================================================
# Get one employee
# URL: GET /api/employees/{employee_id}
# =========================================================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Return the complete information of one employee.
    """

    employee = (
        database.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return employee


# =========================================================
# Update employee
# URL: PATCH /api/employees/{employee_id}
# =========================================================

@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    request: Request,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Update an existing employee record.
    """

    employee = (
        database.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        normalized_email = str(
            update_data["email"]
        ).strip().lower()

        duplicate_email = (
            database.query(Employee)
            .filter(
                Employee.email == normalized_email,
                Employee.id != employee_id,
            )
            .first()
        )

        if duplicate_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Another employee is already using "
                    "this email address."
                ),
            )

        update_data["email"] = normalized_email

    if "employee_code" in update_data:
        normalized_code = (
            update_data["employee_code"]
            .strip()
            .upper()
        )

        duplicate_code = (
            database.query(Employee)
            .filter(
                Employee.employee_code
                == normalized_code,
                Employee.id != employee_id,
            )
            .first()
        )

        if duplicate_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Another employee is already using "
                    "this employee code."
                ),
            )

        update_data["employee_code"] = (
            normalized_code
        )

    if (
        "full_name" in update_data
        and update_data["full_name"] is not None
    ):
        update_data["full_name"] = (
            update_data["full_name"].strip()
        )

    for field_name, field_value in update_data.items():
        setattr(
            employee,
            field_name,
            field_value,
        )

    create_audit_log(
        database=database,
        admin_id=current_admin.id,
        action="UPDATE_EMPLOYEE",
        entity_type="employee",
        entity_id=employee.id,
        description=(
            f"Employee {employee.full_name} "
            f"({employee.employee_code}) was updated."
        ),
        request=request,
    )

    try:
        database.commit()
        database.refresh(employee)

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The employee could not be updated because "
                "some information conflicts with another record."
            ),
        ) from error

    return employee


# =========================================================
# Activate employee
# URL: PATCH /api/employees/{employee_id}/activate
# =========================================================

@router.patch(
    "/{employee_id}/activate",
    response_model=EmployeeResponse,
)
def activate_employee(
    employee_id: int,
    request: Request,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Activate an inactive employee record.
    """

    employee = (
        database.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    employee.is_active = True

    create_audit_log(
        database=database,
        admin_id=current_admin.id,
        action="ACTIVATE_EMPLOYEE",
        entity_type="employee",
        entity_id=employee.id,
        description=(
            f"Employee {employee.full_name} "
            "was activated."
        ),
        request=request,
    )

    database.commit()
    database.refresh(employee)

    return employee


# =========================================================
# Deactivate employee
# URL: PATCH /api/employees/{employee_id}/deactivate
# =========================================================

@router.patch(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponse,
)
def deactivate_employee(
    employee_id: int,
    request: Request,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Deactivate an employee without permanently deleting data.
    """

    employee = (
        database.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    employee.is_active = False

    create_audit_log(
        database=database,
        admin_id=current_admin.id,
        action="DEACTIVATE_EMPLOYEE",
        entity_type="employee",
        entity_id=employee.id,
        description=(
            f"Employee {employee.full_name} "
            "was deactivated."
        ),
        request=request,
    )

    database.commit()
    database.refresh(employee)

    return employee


# =========================================================
# Delete employee permanently
# URL: DELETE /api/employees/{employee_id}
# =========================================================

@router.delete(
    "/{employee_id}",
    response_model=DeleteResponse,
)
def delete_employee(
    employee_id: int,
    request: Request,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Permanently delete an employee and related records.

    Deactivation is recommended when employee history
    should be preserved.
    """

    employee = (
        database.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    employee_name = employee.full_name
    employee_code = employee.employee_code

    database.delete(employee)

    create_audit_log(
        database=database,
        admin_id=current_admin.id,
        action="DELETE_EMPLOYEE",
        entity_type="employee",
        entity_id=employee_id,
        description=(
            f"Employee {employee_name} "
            f"({employee_code}) was permanently deleted."
        ),
        request=request,
    )

    database.commit()

    return DeleteResponse(
        message="Employee deleted successfully.",
        deleted_id=employee_id,
    )