from sqlalchemy import Column, Integer, String

from app.core.database import Base
from app.models.base import Timestamp


class Users(Timestamp, Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "회원"}

    id = Column(Integer, primary_key=True, index=True, comment="PK")
    user_id = Column(String(256), nullable=False, comment="사용자입력ID")
    name = Column(String(256), nullable=False, comment="이름")
    email = Column(String(256), nullable=False, comment="이메일")
    password = Column(String(256), nullable=False, comment="비밀번호")
