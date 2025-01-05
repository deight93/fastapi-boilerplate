from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    success: bool = Field(title="response 상태", description="True / False")
    message: str | None = Field(
        None, title="response 메시지", description="응답 메시지"
    )
    data: Any | None = None
