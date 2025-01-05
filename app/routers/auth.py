from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.schemas.response.auth import PostAuthLogin
from app.services.auth import login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=PostAuthLogin,
    summary="✅ 로그인",
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    tokens = login_user(db, form_data)
    tokens.update({"success": True, "message": None})
    return tokens
