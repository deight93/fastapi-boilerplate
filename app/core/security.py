from datetime import UTC, datetime, timedelta
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext

from app.core.setting import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(subject: str, expire_minutes: int, role: str | None = None) -> str:
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,  # 발급 시각 (issued at)
        "jti": str(uuid4()),  # 고유 토큰 ID
    }
    if role:
        to_encode.update(role=role)
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
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
