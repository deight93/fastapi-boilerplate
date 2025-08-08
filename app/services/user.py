from fastapi import status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError, ErrorCode
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.request.user import UserRegister


async def create_user(db: AsyncSession, user: UserRegister):
    stmt = select(User).where(
        or_(User.user_id == user.user_id, User.email == user.email)
    )
    _result = await db.execute(stmt)
    existing_user = _result.scalars().first()

    if existing_user:
        raise AppError(
            ErrorCode.EXIST_USER_ID_OR_EMAIL_400, status.HTTP_400_BAD_REQUEST
        )

    db_user: User = User(
        user_id=user.user_id,
        name=user.name,
        email=str(user.email),
        hashed_password=get_password_hash(user.password),
    )

    await db_user.save(db)
    return db_user
