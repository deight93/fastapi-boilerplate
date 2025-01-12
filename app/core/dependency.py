from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, redis_config
from app.core.setting import settings
from app.models.admin import Admin
from app.models.users import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
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


def get_redis():
    return redis_config


def get_current_user(
    session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Users:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as e:
        print(f"JWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(Users, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_admin(
    session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Admin:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as e:
        print(f"JWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    admin = session.get(Admin, payload.get("sub"))
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin
