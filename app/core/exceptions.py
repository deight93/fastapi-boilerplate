from enum import Enum

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schemas.response.base import BaseResponse


class ErrorCode(str, Enum):
    NOT_FOUND_404 = "NOT_FOUND"
    UNAUTHORIZED_401 = "UNAUTHORIZED"
    JWT_ERROR_401 = "JWT_ERROR"
    EXIST_USER_ID_OR_EMAIL_400 = "EXIST_USER_ID_OR_EMAIL"


# =========================
# 📂 Exception class
# =========================
class AppError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


# =========================
# 📂 Exception Handlers
# =========================
async def app_exception_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse[None](
            success=False, message=exc.message, data=None
        ).model_dump(),
    )
