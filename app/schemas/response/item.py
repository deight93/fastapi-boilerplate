from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.response.base import BaseList, BaseResponse


class ItemBase(BaseModel):
    title: str = Field(title="제목", description="제목")
    content: str = Field(title="내용", description="내용")

    model_config = ConfigDict(from_attributes=True)


class ItemRead(ItemBase):
    id: int = Field(title="아이템 ID", description="아이템 DB ID")
    created_at: datetime = Field(title="등록 일시", description="등록 일시")
    updated_at: datetime | None = Field(title="수정 일시", description="수정 일시")
    deleted_at: datetime | None = Field(title="삭제 일시", description="삭제 일시")

    model_config = ConfigDict(from_attributes=True)


class ItemList(BaseList):
    results: list[ItemRead]


class ItemListResponse(BaseResponse):
    data: ItemList = Field(title="아이템 목록", description="아이템 목록 데이터")


class ItemDetailResponse(BaseResponse):
    data: ItemRead | None = Field(
        default=None, title="아이템 상세", description="아이템 상세 데이터"
    )
