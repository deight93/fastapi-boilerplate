from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.request.user import UserRegister


def create_user(db: Session, user: UserRegister):
    stmt = select(User).where(
        or_(User.user_id == user.user_id, User.email == user.email)
    )
    existing_user = db.execute(stmt).scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    db_user = User(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
