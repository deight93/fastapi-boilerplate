from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import Timestamp


class Post(Timestamp, Base):
    __tablename__ = "posts"
    __table_args__ = {"comment": "게시판"}

    id = Column(Integer, primary_key=True, index=True, comment="PK")
    title = Column(String(256), index=True, comment="제목")
    content = Column(String, comment="내용")

    owner_id = Column(Integer, ForeignKey("users.id"), comment="작성자")
    owner = relationship("Users", back_populates="posts")
