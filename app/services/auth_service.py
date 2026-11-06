
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.core.config import settings


def register_user(db: Session, user_data: UserRegister):
    existing_user = db.query(User).filter(
        User.email == str(user_data.email).lower()
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user_data.full_name.strip(),
        email=str(user_data.email).lower(),
        password_hash=hash_password(user_data.password),
        role=settings.DEFAULT_USER_ROLE,
        is_active=True
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user"
        )


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(
        User.email == email.lower()
    ).first()

    if not user or not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    return user, token


def change_user_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str
):
    if not verify_password(
        current_password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    user.password_hash = hash_password(new_password)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update password"
        )

    return {"message": "Password changed successfully"}
