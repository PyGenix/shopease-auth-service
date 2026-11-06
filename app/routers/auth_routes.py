from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    MessageResponse,
    TokenVerificationResponse,
    ChangePasswordRequest,
)
from app.services.auth_service import (
    register_user,
    authenticate_user,
    change_user_password,
)
from app.core.security import decode_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    """Reusable dependency for protected endpoints."""

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise unauthorized

    user_id = payload.get("user_id")

    if user_id is None:
        raise unauthorized

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise unauthorized

    user = db.query(User).filter(User.id == user_id).first()

    if user is None or not user.is_active:
        raise unauthorized

    return user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """Register a new customer account."""

    user = register_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """Authenticate a user and issue a JWT access token."""

    user, access_token = authenticate_user(
        db,
        email=str(credentials.email),
        password=credentials.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """Return the authenticated user's profile."""

    return current_user


@router.post(
    "/verify-token",
    response_model=TokenVerificationResponse,
)
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    """Validate a supplied Bearer access token."""

    if credentials is None:
        return TokenVerificationResponse(
            valid=False,
            message="Bearer token is required",
        )

    payload = decode_access_token(credentials.credentials)

    if not payload:
        return TokenVerificationResponse(
            valid=False,
            message="Token is invalid or expired",
        )

    try:
        user_id = int(payload.get("user_id"))
    except (TypeError, ValueError):
        return TokenVerificationResponse(
            valid=False,
            message="Token payload is invalid",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None or not user.is_active:
        return TokenVerificationResponse(
            valid=False,
            message="User does not exist or account is inactive",
        )

    return TokenVerificationResponse(
        valid=True,
        message="Token is valid",
        user_id=user.id,
        role=user.role,
    )


@router.post("/change-password", response_model=MessageResponse)
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change the authenticated user's password."""

    result = change_user_password(
        db=db,
        user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password,
    )

    return MessageResponse(**result)
