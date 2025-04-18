from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.setting import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(
    subject: str | int, expire_minutes: int, role: str | None = None
) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=expire_minutes)
    to_encode = {"exp": expire, "sub": str(subject)}
    if role:
        to_encode.update(role=role)
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
