from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.users import Users
from app.schemas.request.user import UserRegister


def create_user(db: Session, user: UserRegister):
    # 유저 중복 체크
    existing_user = (
        db.query(Users)
        .filter((Users.user_id == user.user_id) | (Users.email == user.email))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    db_user = Users(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
