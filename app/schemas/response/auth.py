from pydantic import Field

from app.schemas.response.base import BaseResponse

# class PostAuthLoginData(BaseModel):
#     access_token: str = Field(title="액세스 토큰", description="JWT 액세스 토큰")
#     token_type: str = Field(default="bearer", title="토큰 타입", description="토큰 타입 (예: bearer)")
#     refresh_token: str | None = Field(None, title="리프레시 토큰", description="JWT 리프레시 토큰")
#     expires_in: int = Field(title="만료 시간", description="토큰 만료 시간 (초)")


class PostAuthLogin(BaseResponse):
    access_token: str = Field(title="액세스 토큰", description="JWT 액세스 토큰")
    token_type: str = Field(
        default="bearer", title="토큰 타입", description="토큰 타입 (예: bearer)"
    )
    refresh_token: str | None = Field(
        None, title="리프레시 토큰", description="JWT 리프레시 토큰"
    )
    expires_in: int = Field(title="만료 시간", description="토큰 만료 시간 (초)")
