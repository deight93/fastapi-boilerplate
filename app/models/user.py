from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, Timestamp


class User(Timestamp, Base):
    __tablename__ = "user"
    __table_args__ = {"comment": "회원"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="PK")
    user_id: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="사용자입력ID"
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False, comment="이름")
    email: Mapped[str] = mapped_column(String(256), nullable=False, comment="이메일")
    hashed_password: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="해시된 비밀번호"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="탈퇴여부")
