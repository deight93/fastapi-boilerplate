from pydantic import BaseModel, Field

from app.schemas.response.base import BaseResponse


class TokenData(BaseModel):
    token_type: str = Field(
        default="bearer", title="토큰 타입", description="토큰 타입 (예: bearer)"
    )
    access_token: str = Field(title="액세스 토큰", description="JWT 액세스 토큰")
    refresh_token: str | None = Field(
        None, title="리프레시 토큰", description="JWT 리프레시 토큰"
    )
    access_expires_in: int = Field(
        title="엑세스 만료 시간", description="토큰 만료 시간 (초)"
    )
    refresh_expires_in: int = Field(
        title="리프레시 만료 시간", description="토큰 만료 시간 (초)"
    )


class PostAuthLogin(BaseResponse, TokenData): ...


class PostAuthRefresh(BaseResponse):
    data: TokenData
