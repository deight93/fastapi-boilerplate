from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Timestamp


class Item(Timestamp, Base):
    __tablename__ = "item"
    __table_args__ = ({"comment": "아이템"},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="PK")
    title: Mapped[str] = mapped_column(Text, nullable=False, comment="제목")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="내용")
    user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="사용자 ID(논리적 FK)"
    )

    user = relationship(
        "User",
        back_populates="items",
        primaryjoin="foreign(Item.user_id) == User.id",
    )
