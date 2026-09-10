from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import (
    authenticate_admin,
    create_access_token,
    get_current_admin,
    hash_password,
    verify_password,
)
from database import get_db
from models import Admin
from schemas import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminPasswordUpdate,
    AdminResponse,
    AdminUpdate,
    MessageResponse,
)


router = APIRouter()


# =========================================================
# Admin login
# POST /api/auth/login
# =========================================================

@router.post(
    "/login",
    response_model=AdminLoginResponse,
)
def login_admin(
    login_data: AdminLoginRequest,
    database: Session = Depends(get_db),
):
    """
    Authenticate the single Admin account and return
    a JWT access token.
    """

    admin = authenticate_admin(
        database=database,
        email=login_data.email,
        password=login_data.password,
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        admin_id=admin.id,
        role=getattr(admin, "role", "employee") or "employee",
    )

    return AdminLoginResponse(
        access_token=access_token,
        token_type="bearer",
        admin=admin,
    )


# =========================================================
# Get current Admin profile
# GET /api/auth/me
# =========================================================

@router.get(
    "/me",
    response_model=AdminResponse,
)
def get_admin_profile(
    current_admin: Admin = Depends(get_current_admin),
):
    """
    Return the currently logged-in Admin profile.
    """

    return current_admin


# =========================================================
# Update Admin profile
# PATCH /api/auth/me
# =========================================================

@router.patch(
    "/me",
    response_model=AdminResponse,
)
def update_admin_profile(
    profile_data: AdminUpdate,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Update the single Admin profile.
    """

    update_data = profile_data.model_dump(
        exclude_unset=True,
    )

    if "email" in update_data:
        normalized_email = str(
            update_data["email"]
        ).strip().lower()

        existing_admin = (
            database.query(Admin)
            .filter(
                Admin.email == normalized_email,
                Admin.id != current_admin.id,
            )
            .first()
        )

        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="That email address is already in use.",
            )

        update_data["email"] = normalized_email

    if (
        "full_name" in update_data
        and update_data["full_name"] is not None
    ):
        update_data["full_name"] = (
            update_data["full_name"].strip()
        )

    for field_name, field_value in update_data.items():
        setattr(
            current_admin,
            field_name,
            field_value,
        )

    try:
        database.commit()
        database.refresh(current_admin)

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The updated information conflicts with existing data.",
        ) from error

    return current_admin


# =========================================================
# Change Admin password
# PATCH /api/auth/change-password
# =========================================================

@router.patch(
    "/change-password",
    response_model=MessageResponse,
)
def change_admin_password(
    password_data: AdminPasswordUpdate,
    current_admin: Admin = Depends(get_current_admin),
    database: Session = Depends(get_db),
):
    """
    Change the password of the single Admin account.
    """

    password_is_correct = verify_password(
        plain_password=password_data.current_password,
        hashed_password=current_admin.password_hash,
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The current password is incorrect.",
        )

    if (
        password_data.current_password
        == password_data.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "The new password must be different "
                "from the current password."
            ),
        )

    current_admin.password_hash = hash_password(
        password_data.new_password
    )

    database.commit()

    return MessageResponse(
        message="Password changed successfully.",
    )


# =========================================================
# Logout
# POST /api/auth/logout
# =========================================================

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout_admin(
    current_admin: Admin = Depends(get_current_admin),
):
    """
    JWT logout is completed by deleting the token
    from localStorage in the frontend.
    """

    return MessageResponse(
        message=(
            "Logged out successfully. "
            "Remove the access token from localStorage."
        ),
    )