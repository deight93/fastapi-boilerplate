import enum

from sqlalchemy import Column, Enum, Integer, String

from app.core.database import Base
from app.models.base import Timestamp


class AdminRole(enum.Enum):
    SUPER = "SUPER"  # 최고 관리자
    NORMAL = "NORMAL"


class Admin(Timestamp, Base):
    __tablename__ = "admin"
    __table_args__ = {"comment": "관리자"}

    id = Column(Integer, primary_key=True, index=True, comment="PK")
    admin_id = Column(String(256), nullable=False, comment="관리자 ID")
    name = Column(String(256), nullable=False, comment="이름")
    email = Column(String(256), nullable=False, comment="이메일")
    role = Column(
        Enum(AdminRole, name="admin_role_enum"), nullable=False, comment="관리자 권한"
    )
    hashed_password = Column(String(256), nullable=False, comment="해시된 비밀번호")
