from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError, ErrorCode
from app.core.security import create_token, verify_password
from app.core.setting import settings
from app.models.user import User


async def login_user(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
    stmt = select(User).where(User.user_id == form_data.username)
    _result = await db.execute(stmt)
    user = _result.scalars().first()

    if not user:
        raise AppError(ErrorCode.UNAUTHORIZED_401, status.HTTP_401_UNAUTHORIZED)

    if not verify_password(form_data.password, user.hashed_password):
        raise AppError(ErrorCode.UNAUTHORIZED_401, status.HTTP_401_UNAUTHORIZED)

    user_id = str(user.id)
    access_token = create_token(
        subject=user_id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_token(
        subject=user_id, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expires_in": 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_expires_in": 60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    }

    return tokens


async def refresh_tokens(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise AppError(ErrorCode.JWT_ERROR_401, status.HTTP_401_UNAUTHORIZED)

    user_id = int(payload.get("sub"))
    stmt = select(User).where(User.id == user_id)
    user = (await db.execute(stmt)).scalars().first()

    if not user:
        raise AppError(ErrorCode.UNAUTHORIZED_401, status.HTTP_401_UNAUTHORIZED)

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
        "access_expires_in": 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_expires_in": 60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    }
    return tokens
