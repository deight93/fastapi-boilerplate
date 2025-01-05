from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token
from app.models.users import Users


def login_user(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
    stmt = select(Users).where(Users.user_id == form_data.username)
    user = db.execute(stmt).scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id, expires_delta=timedelta(minutes=30))
    tokens = {
        "access_token" : access_token,
        "token_type" : "bearer",
        "expires_in": 60 * 30
    }

    return tokens
