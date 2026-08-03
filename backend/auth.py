import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import Admin


# =========================================================
# JWT configuration
# =========================================================

SECRET_KEY = os.getenv(
    "EMS_SECRET_KEY",
    "change-this-secret-key-before-production",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours


# =========================================================
# Password hashing
# =========================================================

password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


# =========================================================
# OAuth2 token reader
# =========================================================

bearer_scheme = HTTPBearer(
    auto_error=False,
)


# =========================================================
# Password functions
# =========================================================

def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure password hash.
    """

    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Compare a plain-text password with a stored password hash.
    """

    return password_context.verify(
        plain_password,
        hashed_password,
    )


# =========================================================
# JWT token creation
# =========================================================

def create_access_token(
    admin_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token for the Admin.
    """

    current_time = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    expiration_time = current_time + expires_delta

    token_data = {
        "sub": str(admin_id),
        "type": "admin_access",
        "iat": current_time,
        "exp": expiration_time,
    }

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# =========================================================
# JWT token decoding
# =========================================================

def decode_access_token(token: str) -> dict:
    """
    Decode and validate an Admin JWT token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        admin_id = payload.get("sub")
        token_type = payload.get("type")

        if admin_id is None:
            raise credentials_exception

        if token_type != "admin_access":
            raise credentials_exception

        return payload

    except JWTError as error:
        raise credentials_exception from error


# =========================================================
# Admin authentication
# =========================================================

def authenticate_admin(
    database: Session,
    email: str,
    password: str,
) -> Optional[Admin]:
    """
    Check the Admin email and password during login.
    """

    normalized_email = email.strip().lower()

    admin = (
        database.query(Admin)
        .filter(Admin.email == normalized_email)
        .first()
    )

    if admin is None:
        return None

    if not verify_password(
        password,
        admin.password_hash,
    ):
        return None

    if not admin.is_active:
        return None

    return admin


# =========================================================
# Current logged-in Admin dependency
# =========================================================

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    database: Session = Depends(get_db),
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin authentication is required.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    if credentials.scheme.lower() != "bearer":
        raise credentials_exception

    payload = decode_access_token(
        credentials.credentials
    )

    admin_id = payload.get("sub")

    try:
        admin_id = int(admin_id)
    except (TypeError, ValueError) as error:
        raise credentials_exception from error

    admin = (
        database.query(Admin)
        .filter(Admin.id == admin_id)
        .first()
    )

    if admin is None:
        raise credentials_exception

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This Admin account is inactive.",
        )

    return admin