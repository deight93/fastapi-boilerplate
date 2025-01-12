from pydantic import BaseModel, EmailStr, Field

from app.schemas.response.base import BaseResponse


class PostUserRegister(BaseResponse): ...


class PostAuthLoginData(BaseModel):
    user_id: str = Field(title="사용자입력 ID", description="사용자입력 ID")
    name: str = Field(title="이름", description="이름")
    email: EmailStr = Field(title="이메일", description="이메일")


class GetUserMe(BaseResponse):
    data: PostAuthLoginData | None = Field(
        None, title="로그인 사용자 데이터", description="로그인 사용자 데이터"
    )
