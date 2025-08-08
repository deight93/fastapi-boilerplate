from fastapi import Query
from pydantic import BaseModel, Field


class LimitOffsetPagination(BaseModel):
    offset: int = Field(Query(0, title="시작 개수", description="시작 개수"))
    limit: int | None = Field(
        Query(None, title="가져올 개수", description="가져올 개수")
    )
