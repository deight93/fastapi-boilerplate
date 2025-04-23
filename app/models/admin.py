import enum

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, Timestamp


class AdminRole(enum.Enum):
    SUPER = "SUPER"  # 최고 관리자
    NORMAL = "NORMAL"


class Admin(Timestamp, Base):
    __tablename__ = "admin"
    __table_args__ = {"comment": "관리자"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="PK")
    admin_id: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="관리자 ID"
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False, comment="이름")
    email: Mapped[str] = mapped_column(String(256), nullable=False, comment="이메일")
    role: Mapped[enum] = mapped_column(
        Enum(AdminRole, name="admin_role_enum"), nullable=False, comment="관리자 권한"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="해시된 비밀번호"
    )
