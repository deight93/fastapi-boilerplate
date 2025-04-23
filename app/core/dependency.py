import logging
from collections.abc import AsyncGenerator

import redis.asyncio as redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, SessionLocal
from app.core.security import decode_token
from app.core.setting import settings
from app.models.admin import Admin
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def sync_get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        try:
            yield session
        except Exception as e:
            logging.error(f"Error getting database session: {e}")
            raise


async def get_redis():
    return await redis.from_url(
        settings.redis_url.unicode_string(),
        encoding="utf-8",
        decode_responses=True,
    )


async def get_cache():
    return await redis.from_url(
        settings.redis_url.unicode_string(),
        decode_responses=False,
    )


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = await decode_token(token)
    except JWTError as e:
        logging.error(f"JWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_id = int(payload.get("sub"))
    stmt = select(User).where(User.id == user_id)
    _result = await db.execute(stmt)
    user: User = _result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_admin(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> type[Admin]:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError as e:
        logging.error(f"JWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    admin_id = int(payload.get("sub"))
    stmt = select(Admin).where(Admin.id == admin_id)
    _result = await db.execute(stmt)
    admin = _result.scalars().first()

    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin
