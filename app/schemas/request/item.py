from pydantic import BaseModel, Field

from app.schemas.request.base import LimitOffsetPagination


class ItemListRequest(LimitOffsetPagination):
    title: str | None = Field(None, title="제목", description="제목")
    content: str | None = Field(None, title="내용", description="내용")


class ItemInsertRequest(BaseModel):
    title: str = Field(title="제목", description="제목")
    content: str = Field(title="내용", description="내용")


class ItemUpdateRequest(BaseModel):
    title: str | None = Field(None, title="제목", description="제목")
    content: str | None = Field(None, title="내용", description="내용")
