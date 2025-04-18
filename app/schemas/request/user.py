from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    user_id: str = Field(title="사용자입력 ID", description="사용자 입력 ID")
    name: str = Field(title="이름", description="이름")
    email: EmailStr = Field(title="이메일", description="이메일")
    password: str = Field(
        title="사용자 입력 비밀번호", description="사용자 입력 비밀번호"
    )
