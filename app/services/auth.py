from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_token, verify_password
from app.core.setting import settings
from app.models.user import User


def login_user(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
    stmt = select(User).where(User.user_id == form_data.username)
    user = db.execute(stmt).scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token(
        subject=user.id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_token(
        subject=user.id, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expires_in": 60 * 30,
        "refresh_expires_in": 60 * 60,
    }

    return tokens


def refresh_tokens(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    id: str = payload.get("sub")
    stmt = select(User).where(User.id == id)
    user = db.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = create_token(
        subject=user.id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_token(
        subject=user.id, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expires_in": 60 * 30,
        "refresh_expires_in": 60 * 60,
    }
    return tokens
