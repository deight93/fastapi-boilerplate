from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool = Field(title="response 상태", description="True / False")
    message: str | None = Field(title="response 메시지", description="응답 메시지")
    data: T | None = Field(
        None, title="response 데이터", description="요청 결과 데이터"
    )

    @classmethod
    def success_response(cls, message: str | None, data: T | None = None):
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail_response(cls, message: str | None, data: T | None = None):
        return cls(success=False, message=message, data=data)


class BaseList(BaseModel):
    results: list = Field(
        default_factory=list, title="데이터 목록", description="데이터 목록"
    )
    total_count: int = Field(title="총 항목 수", description="총 항목 수")
